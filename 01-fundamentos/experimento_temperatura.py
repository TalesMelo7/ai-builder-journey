"""
Experimento: o que a temperatura muda na resposta?

Envia o MESMO prompt 3 vezes em cada temperatura e mostra as respostas lado a lado.
Anote no notas.md o que você observou.

Uso:
  python experimento_temperatura.py
  python experimento_temperatura.py "Dê um nome para uma startup de logística"
"""

import os
import sys

from chamar_llm import MODELO_PADRAO, criar_cliente, perguntar

PROMPT_PADRAO = "Sugira um nome curto e criativo para um sistema de planejamento de produção."
TEMPERATURAS = [0.0, 0.5, 1.0]
REPETICOES = 3


def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else PROMPT_PADRAO
    modelo = os.getenv("MODELO", MODELO_PADRAO)
    cliente = criar_cliente()

    print(f"Prompt: {prompt}\nModelo: {modelo}\n")
    total_tokens = 0

    for temperatura in TEMPERATURAS:
        print(f"=== temperatura {temperatura} ===")
        for i in range(1, REPETICOES + 1):
            mensagens = [{"role": "user", "content": prompt}]
            texto, resposta, _ = perguntar(cliente, mensagens, modelo, temperatura, max_tokens=60)
            total_tokens += resposta.usage.input_tokens + resposta.usage.output_tokens
            print(f"  {i}. {texto.strip()}")
        print()

    print(f"Total de tokens usados no experimento: {total_tokens}")
    print("Pergunta para o notas.md: em qual temperatura as respostas se repetiram?")


if __name__ == "__main__":
    main()
