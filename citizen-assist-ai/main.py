from base_conhecimento import BaseConhecimento
from assistente import Assistente

base = BaseConhecimento("data/base_conhecimento.json")
base.carregar()
assistente = Assistente("Citizen Assist AI", base)

status = -1
while status != 0:
    print("\n===== Citizen Assist AI =====")
    print("[1] Identificar problema (digitar dúvida)")
    print("[2] Precisa de ajuda em alguma categoria?")
    print("[3] Indicadores dos atendimentos")
    print("[4] Exportar atendimentos para CSV")
    print("[0] Sair")

    status = assistente.ler_numero("Selecione a seguinte opção: ", 4)

    if status == 1:
        assistente.perguntar()
    elif status == 2:
        assistente.navegar()
    elif status == 3:
        assistente.indicadores()
    elif status == 4:
        assistente.exportar_csv()
    elif status == 0:
        assistente.avaliar_facilidade()
        print("Obrigado por usar o Citizen Assist AI!")
