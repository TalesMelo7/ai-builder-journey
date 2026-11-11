# Fase 1 — Fundamentos de LLMs

**Período:** 11/11 – 29/11/2026 · **Meta:** entender como um LLM funciona por dentro e fazer a primeira chamada pela API, medindo tokens e custo.

## Entregáveis

- [ ] `chamar_llm.py` rodando no meu computador (pergunta única e modo chat)
- [ ] `experimento_temperatura.py` rodado e conclusões anotadas
- [ ] `notas.md` preenchido com os conceitos **nas minhas palavras**
- [ ] Certificado de um curso introdutório da [Claude Academy](https://academy.claude.com)
- [ ] Post curto no LinkedIn contando o que aprendi

## Cronograma

### Aquecimento (qua 11/11 – dom 15/11)
- [ ] Criar conta na Claude Academy e escolher o curso introdutório
- [ ] Criar conta no [Console da Anthropic](https://console.anthropic.com), colocar créditos e gerar uma chave de API
- [ ] Fazer o setup abaixo e rodar o primeiro `chamar_llm.py`

### Semana 1 (seg 16/11 – dom 22/11) — como um LLM funciona
| Bloco | O que fazer |
|-------|-------------|
| Teoria 1 (1 h) | Curso da Claude Academy: o que é um LLM, tokens, janela de contexto |
| Teoria 2 (1 h) | Temperatura, alucinação, por que o modelo "não sabe" o que não está no contexto |
| Prática 1 (1,5 h) | Rodar `chamar_llm.py` com 5 perguntas diferentes; anotar tokens de entrada e saída |
| Prática 2 (1,5 h) | Testar `--sistema` e `--max-tokens` baixo (ex.: 20). O que acontece com o `stop_reason`? |
| Projeto (4 h) | Rodar `experimento_temperatura.py` com 2 prompts diferentes e escrever as conclusões |

### Semana 2 (seg 23/11 – dom 29/11) — API na prática
| Bloco | O que fazer |
|-------|-------------|
| Teoria 1 (1 h) | Ler a referência da Messages API (parâmetros, formato da resposta, erros) |
| Teoria 2 (1 h) | Custos: preço por token de entrada × saída; comparar modelos na página de preços |
| Prática 1 (1,5 h) | Modo `--chat`: conversar 10 turnos e observar os tokens de entrada crescendo |
| Prática 2 (1,5 h) | Revisão de Python: `argparse`, funções, tratamento de erro — ler o código linha a linha |
| Projeto (4 h) | Desafio abaixo + atualizar o README principal e o Notion |

## Setup (Windows)

```powershell
cd 01-fundamentos
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # depois abra o .env e cole sua chave
python chamar_llm.py "Explique o que é um token em 3 frases"
```

> **Segurança:** a chave fica só no `.env`, que está no `.gitignore`. Nunca cole a chave no código nem em prints.
> Se ela vazar, apague-a no Console e gere outra.

## Desafio da fase

Adicione ao `chamar_llm.py` uma opção `--custo` que calcula quanto a chamada custou em dólares, a partir dos tokens de entrada e saída e do preço do modelo (consulte a página de preços oficial). Dica: guarde os preços num dicionário `{modelo: (preco_entrada, preco_saida)}` por milhão de tokens.

## Como saber que a fase acabou

Consigo explicar para alguém, sem consultar nada: o que é um token, por que conversas longas ficam mais caras, o que a temperatura faz e por que o modelo pode inventar respostas.
