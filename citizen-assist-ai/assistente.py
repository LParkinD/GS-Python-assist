import json
import csv
import time


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        try:
            with open("data/historico.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                if isinstance(dados, list):
                    self.historico = dados
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            self.historico = []

    def ler_numero(self, mensagem, maximo):
        while True:
            valor = input(mensagem).strip()
            if valor.isdigit():
                numero = int(valor)
                if 0 <= numero <= maximo:
                    return numero
            print("Opção inválida. Tente novamente.")

    def ler_sim_nao(self):
        while True:
            resposta = input("Essa orientação respondeu sua dúvida? (s/n): ").lower().strip()
            if resposta in ("s", "n"):
                return resposta == "s"
            print("Digite apenas s ou n.")

    def tem_dados_pessoais(self, pergunta):
        if "@" in pergunta:
            return True
        numeros = 0
        for letra in pergunta:
            if letra.isdigit():
                numeros += 1
        return numeros >= 8

    def registrar(self, origem, pergunta, orientacao, encontrou, ajudou, tentativas, tempo):
        registro = {
            "data": time.strftime("%d/%m/%Y %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao.id if orientacao is not None else None,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo
        }
        self.historico.append(registro)
        try:
            with open("data/historico.json", "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)
        except OSError:
            print("Não foi possível salvar o histórico.")

    def perguntar(self):
        inicio = time.time()
        tentativas = 0
        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if pergunta == "0":
                return
            if pergunta == "":
                print("Digite alguma dúvida.")
                continue
            if self.tem_dados_pessoais(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)
            if len(resultados) == 0 or resultados[0][0] < 3:
                print("Não encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras ou navegue pelas categorias.")
                self.registrar("pergunta", pergunta, None, False, False,
                              tentativas, round(time.time() - inicio, 1))
                continue

            pontos, orientacao = resultados[0]
            if pontos >= 6:
                confianca = "ALTA"
            else:
                confianca = "MÉDIA"

            print("\nConfiança da resposta:", confianca, "(" + str(pontos) + " pontos)")
            orientacao.exibir()

            alternativas = 0
            for pontuacao, outra in resultados[1:]:
                if pontuacao >= 3 and alternativas < 2:
                    print("Alternativa:", outra.titulo, "(" + str(pontuacao) + " pontos)")
                    alternativas += 1

            ajudou = self.ler_sim_nao()
            self.registrar("pergunta", pergunta, orientacao, True, ajudou,
                          tentativas, round(time.time() - inicio, 1))
            return

    def navegar(self):
        inicio = time.time()
        categorias = self.base.categorias()
        if not categorias:
            print("Nenhuma categoria disponível.")
            return
        while True:
            print("\nCategorias:")
            for i in range(len(categorias)):
                print("[" + str(i + 1) + "]", categorias[i])
            print("[0] Voltar")
            numero = self.ler_numero("Qual categoria você deseja selecionar? ", len(categorias))
            if numero == 0:
                return
            categoria = categorias[numero - 1]
            titulos = self.base.por_categoria(categoria)
            while True:
                print("\nOrientações de", categoria)
                for i in range(len(titulos)):
                    print("[" + str(i + 1) + "]", titulos[i].titulo)
                print("[0] Voltar")
                numero_titulo = self.ler_numero("Selecione um título: ", len(titulos))
                if numero_titulo == 0:
                    break
                orientacao = titulos[numero_titulo - 1]
                print()
                orientacao.exibir()
                ajudou = self.ler_sim_nao()
                self.registrar("categoria", "", orientacao, True, ajudou, 1,
                              round(time.time() - inicio, 1))
                inicio = time.time()

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("Nenhum atendimento registrado.")
            return

        encontrados = 0
        ajudaram = 0
        tempo_total = 0
        tentativas = 0
        sem_solucao = []
        for registro in self.historico:
            if registro.get("encontrou"):
                encontrados += 1
                if registro.get("ajudou"):
                    ajudaram += 1
            else:
                if registro.get("pergunta"):
                    sem_solucao.append(registro["pergunta"])
            tempo_total += registro.get("tempo_segundos", 0)
            tentativas += registro.get("tentativas", 0)

        print("\n--- Indicadores ---")
        print("Total de atendimentos:", total)
        print("Resposta encontrada:", round(encontrados / total * 100, 1), "%")
        if encontrados > 0:
            print("Taxa de acerto (ajudou):", round(ajudaram / encontrados * 100, 1), "%")
        else:
            print("Taxa de acerto (ajudou): 0 %")
        print("Tempo médio:", round(tempo_total / total, 1), "segundos")
        print("Tentativas por atendimento:", round(tentativas / total, 1))
        notas = [r["facilidade"] for r in self.historico
                 if isinstance(r.get("facilidade"), int) and 1 <= r["facilidade"] <= 5]
        if notas:
            print("Facilidade de uso:", round(sum(notas) / len(notas), 1), "de 5")
        else:
            print("Facilidade de uso: ainda não avaliada")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for duvida in sem_solucao:
                print(" -", duvida)
        else:
            print("Nenhuma.")

    def avaliar_facilidade(self):
        if not self.historico:
            print("Nenhum atendimento para avaliar.")
            return
        nota = self.ler_numero("Dê uma nota de facilidade de 1 a 5 (0 para pular): ", 5)
        if nota == 0:
            return
        # A nota é associada ao último atendimento feito.
        self.historico[-1]["facilidade"] = nota
        try:
            with open("data/historico.json", "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)
        except OSError:
            print("Não foi possível salvar a nota.")

    def exportar_csv(self):
        campos = ["data", "origem", "pergunta", "id_orientacao",
                  "encontrou", "ajudou", "tentativas", "tempo_segundos", "facilidade"]
        try:
            with open("data/atendimentos.csv", "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos, extrasaction="ignore")
                escritor.writeheader()
                for registro in self.historico:
                    escritor.writerow(registro)
            print("Atendimentos exportados para data/atendimentos.csv")
        except OSError:
            print("Não foi possível exportar o CSV.")
