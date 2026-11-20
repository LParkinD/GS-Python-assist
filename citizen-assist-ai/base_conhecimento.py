import json
from orientacao import Orientacao

ACENTOS = {
    "á": "a", "à": "a", "ã": "a", "â": "a",
    "é": "e", "ê": "e", "í": "i",
    "ó": "o", "õ": "o", "ô": "o",
    "ú": "u", "ç": "c"
}

def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()-":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                print("A base de conhecimento precisa ser uma lista.")
                return
            for dado in dados:
                try:
                    orientacao = Orientacao(
                        dado["id"], dado["categoria"], dado["titulo"],
                        dado["palavras_chave"], dado["resposta"],
                        dado["documentos"], dado["onde"], dado["fonte"],
                        dado["verificado_em"]
                    )
                    self.orientacoes.append(orientacao)
                except (KeyError, TypeError):
                    print("Uma orientação incompleta foi ignorada.")
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            print("Não foi possível abrir a base de conhecimento.")

    def categorias(self):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                lista.append(orientacao)
        return lista

    def pontuar(self, pergunta, orientacao):
        pergunta = normalizar(pergunta)
        pontos = 0
        for palavra in orientacao.palavras_chave:
            if normalizar(palavra) in pergunta:
                pontos += 3
        titulo = normalizar(orientacao.titulo)
        for palavra in pergunta.split():
            if len(palavra) >= 4 and (" " + palavra + " ") in titulo:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados
