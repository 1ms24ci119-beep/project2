"""Text normalization and corpus loading utilities."""

from pathlib import Path
import re
from typing import Iterable, List

TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")


def tokenize(text: str) -> List[str]:
    """Lowercase text and return word-like tokens."""
    return TOKEN_PATTERN.findall(text.lower())


def load_corpus(path: str) -> List[List[str]]:
    """Load a UTF-8, one-sentence-per-line corpus and tokenize each line."""
    corpus_path = Path(path)
    if not corpus_path.is_file():
        raise FileNotFoundError(f"Corpus file not found: {corpus_path}")
    sentences = []
    for line in corpus_path.read_text(encoding="utf-8").splitlines():
        tokens = tokenize(line)
        if tokens:
            sentences.append(tokens)
    if not sentences:
        raise ValueError("The corpus contains no usable text.")
    return sentences


def prepare_sentences(lines: Iterable[str]) -> List[List[str]]:
    """Prepare in-memory lines; useful for tests and small experiments."""
    return [tokens for line in lines if (tokens := tokenize(line))]
