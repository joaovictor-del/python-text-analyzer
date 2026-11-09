# Analisador de textos

Analise um arquivo ou texto enviado pelo terminal. O programa mostra estatísticas, tempo aproximado de leitura e palavras mais frequentes.

## Requisitos

- Python 3.9 ou superior

## Como usar

```bash
python3 text_analyzer.py artigo.txt
cat artigo.txt | python3 text_analyzer.py
```

Por padrão, mostra até 10 palavras mais frequentes. Para alterar a quantidade:

```bash
python3 text_analyzer.py artigo.txt --top 5
```

O tempo de leitura é estimado a 200 palavras por minuto. A contagem de frases é aproximada e baseada em pontuação (`.`, `!`, `?`).

## Testes

```bash
python3 -m unittest discover -s tests -v
```

## O que este projeto pratica

Expressões regulares Unicode, contagem de palavras, leitura de arquivos e entrada padrão, argumentos CLI e testes unitários.
