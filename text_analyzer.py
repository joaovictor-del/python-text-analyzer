"""Calcula estatísticas de leitura para textos ou arquivos."""

import argparse
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


WORD_PATTERN = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)
SENTENCE_PATTERN = re.compile(r"[.!?]+")


@dataclass(frozen=True)
class TextReport:
    words: int
    characters: int
    characters_without_spaces: int
    sentences: int
    reading_minutes: int
    top_words: tuple[tuple[str, int], ...]


def analyze_text(text: str, top: int = 10) -> TextReport:
    if top < 1:
        raise ValueError("A quantidade de palavras deve ser pelo menos 1.")

    words = [match.group(0).casefold() for match in WORD_PATTERN.finditer(text)]
    counts = Counter(words)
    ranked_words = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:top]
    return TextReport(
        words=len(words),
        characters=len(text),
        characters_without_spaces=sum(not character.isspace() for character in text),
        sentences=len(SENTENCE_PATTERN.findall(text)),
        reading_minutes=math.ceil(len(words) / 200),
        top_words=tuple(ranked_words),
    )


def read_input(path: Optional[Path]) -> str:
    if path is not None:
        return path.read_text(encoding="utf-8")
    return sys.stdin.read()


def format_report(report: TextReport) -> str:
    lines = [
        f"Palavras: {report.words}",
        f"Caracteres (com espaços): {report.characters}",
        f"Caracteres (sem espaços): {report.characters_without_spaces}",
        f"Frases (aproximado): {report.sentences}",
        f"Tempo de leitura estimado: {report.reading_minutes} min",
        "Palavras mais frequentes:",
    ]
    if report.top_words:
        lines.extend(f"  {word}: {count}" for word, count in report.top_words)
    else:
        lines.append("  (nenhuma palavra encontrada)")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gere estatísticas de um texto.")
    parser.add_argument("file", nargs="?", type=Path, help="arquivo .txt; sem arquivo, lê do stdin")
    parser.add_argument("--top", type=int, default=10, help="quantidade de palavras no ranking")
    args = parser.parse_args()
    print(format_report(analyze_text(read_input(args.file), args.top)))


if __name__ == "__main__":
    main()
