"""
Fase 1 — Meu primeiro script que chama um LLM pela API.

O que este script ensina:
  1. Como autenticar e chamar a API (Anthropic / Claude).
  2. O que vem na resposta: texto, motivo de parada e uso de tokens.
  3. O efeito dos parâmetros: modelo, temperatura, max_tokens, prompt de sistema.
  4. Que a API NÃO tem memória: no modo chat, quem guarda o histórico é o seu código.

Uso:
  python chamar_llm.py "Explique o que é um token em 3 frases"
  python chamar_llm.py "Crie um slogan" --temperatura 0
  python chamar_llm.py "Resuma: ..." --sistema "Você é um analista de dados objetivo."
  python chamar_llm.py --chat
"""

import argparse
import os
import sys
import time

import anthropic
from dotenv import load_dotenv

MODELO_PADRAO = "claude-haiku-5-5"


def criar_cliente() -> anthropic.Anthropic:
    """Lê a chave do arquivo .env e cria o cliente da API."""
    load_dotenv()
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit(
            "Erro: ANTHROPIC_API_KEY não encontrada.\n"
            "Copie .env.example para .env e coloque sua chave."
        )
    # O cliente lê ANTHROPIC_API_KEY do ambiente automaticamente.
    return anthropic.Anthropic()


def perguntar(cliente, mensagens, modelo, temperatura, max_tokens, sistema=None):
    """
    Envia a conversa inteira para o modelo e devolve a resposta.

    `mensagens` é uma lista no formato:
        [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]
    """
    parametros = {
        "model": modelo,
        "max_tokens": max_tokens,       # limite de tokens da RESPOSTA
        "temperature": temperatura,     # 0 = mais previsível; 1 = mais variado
        "messages": mensagens,
    }
    if sistema:
        parametros["system"] = sistema  # instruções de "papel" e regras gerais

    inicio = time.perf_counter()
    resposta = cliente.messages.create(**parametros)
    duracao = time.perf_counter() - inicio

    # A resposta vem em blocos; juntamos só os blocos de texto.
    texto = "".join(bloco.text for bloco in resposta.content if bloco.type == "text")
    return texto, resposta, duracao


def mostrar_metricas(resposta, duracao):
    """Mostra o que importa para custo e qualidade."""
    uso = resposta.usage
    print("\n--- métricas ---")
    print(f"modelo:          {resposta.model}")
    print(f"tokens entrada:  {uso.input_tokens}")
    print(f"tokens saída:    {uso.output_tokens}")
    print(f"motivo parada:   {resposta.stop_reason}  (max_tokens = a resposta foi cortada)")
    print(f"tempo:           {duracao:.2f} s")


def modo_unico(cliente, args):
    mensagens = [{"role": "user", "content": args.pergunta}]
    texto, resposta, duracao = perguntar(
        cliente, mensagens, args.modelo, args.temperatura, args.max_tokens, args.sistema
    )
    print(texto)
    mostrar_metricas(resposta, duracao)


def modo_chat(cliente, args):
    """
    Chat no terminal. Repare: a cada pergunta reenviamos TODO o histórico.
    Por isso conversas longas gastam cada vez mais tokens de entrada.
    """
    print("Modo chat. Digite 'sair' para encerrar.\n")
    historico = []
    while True:
        pergunta = input("você> ").strip()
        if pergunta.lower() in {"sair", "exit", "quit"}:
            break
        if not pergunta:
            continue

        historico.append({"role": "user", "content": pergunta})
        texto, resposta, duracao = perguntar(
            cliente, historico, args.modelo, args.temperatura, args.max_tokens, args.sistema
        )
        historico.append({"role": "assistant", "content": texto})

        print(f"\nclaude> {texto}")
        print(
            f"[{resposta.usage.input_tokens} tokens entrada | "
            f"{resposta.usage.output_tokens} saída | {duracao:.1f}s]\n"
        )


def main():
    parser = argparse.ArgumentParser(description="Chama um LLM pela API e mostra as métricas.")
    parser.add_argument("pergunta", nargs="?", help="Pergunta a enviar (omita se usar --chat)")
    parser.add_argument("--chat", action="store_true", help="Abre um chat com histórico")
    parser.add_argument("--modelo", default=os.getenv("MODELO", MODELO_PADRAO))
    parser.add_argument("--temperatura", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=500)
    parser.add_argument("--sistema", help="Prompt de sistema (papel e regras)")
    args = parser.parse_args()

    if not args.chat and not args.pergunta:
        parser.error("informe uma pergunta ou use --chat")

    cliente = criar_cliente()
    try:
        if args.chat:
            modo_chat(cliente, args)
        else:
            modo_unico(cliente, args)
    except anthropic.AuthenticationError:
        sys.exit("Erro de autenticação: confira a chave no .env.")
    except anthropic.RateLimitError:
        sys.exit("Limite de uso atingido. Espere um pouco e tente de novo.")
    except anthropic.APIConnectionError:
        sys.exit("Não consegui conectar na API. Confira sua internet ou proxy.")
    except anthropic.APIStatusError as erro:
        sys.exit(f"A API respondeu com erro {erro.status_code}: {erro.message}")


if __name__ == "__main__":
    main()
