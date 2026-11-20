# Citizen Assist AI

Trabalho de Pensamento Computacional e Automação com Python - FIAP.

## Objetivo
Orientar cidadãos sobre serviços e documentos usando uma base de conhecimento em JSON.
O programa não é um canal oficial e não solicita dados pessoais.

## Como executar
Abra o terminal na pasta do projeto e digite:

    python main.py

## Pontuação
- Cada palavra-chave encontrada na pergunta: +3 pontos.
- Cada palavra da pergunta com 4 letras ou mais encontrada no título: +1 ponto.
- 6 pontos ou mais: confiança ALTA.
- 3 a 5 pontos: confiança MÉDIA.
- Menos de 3 pontos: orientação não encontrada.
- O programa mostra a melhor resposta e até duas alternativas.

## Arquivos
- main.py: menu.
- orientacao.py: dados de uma orientação.
- base_conhecimento.py: carrega o JSON, categorias e busca.
- assistente.py: atendimento, histórico, indicadores e CSV.
- data/base_conhecimento.json: orientações e fontes.
- data/historico.json: atendimentos.
- data/atendimentos.csv: exportação.

## Limitações
A busca usa palavras e regras, não inteligência artificial generativa.
As informações devem ser conferidas nos sites oficiais.

## Completar antes da entrega
- Integrantes e RMs:
- Público específico escolhido:
- ODS relacionados:
- Integrações com outras disciplinas (se houver):
- Fontes consultadas: verificar as URLs no JSON.
- Testes com 3 pessoas externas e pelo menos 10 atendimentos:
- Indicadores reais do teste:
- Dúvidas sem solução e melhoria feita após os testes:
- Link do vídeo técnico:
