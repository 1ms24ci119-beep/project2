"""A transparent n-gram next-word model with add-k smoothing."""

from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Tuple


class NGramModel:
    def __init__(self, n: int = 3, alpha: float = 1.0):
        if n < 1:
            raise ValueError("n must be at least 1")
        if alpha <= 0:
            raise ValueError("alpha must be greater than 0")
        self.n = n
        self.alpha = float(alpha)
        self.unigrams = Counter()
        self.context_counts = defaultdict(Counter)
        self.vocabulary = set()

    def fit(self, sentences: Iterable[List[str]]) -> "NGramModel":
        """Count n-grams. Sentence boundaries are intentionally not predicted."""
        self.unigrams.clear()
        self.context_counts.clear()
        self.vocabulary.clear()

        for sentence in sentences:
            tokens = list(sentence)
            if not tokens:
                continue
            self.unigrams.update(tokens)
            self.vocabulary.update(tokens)
            for index, word in enumerate(tokens):
                start = max(0, index - (self.n - 1))
                context = tuple(tokens[start:index])
                # Store every suffix context up to n-1 words for backoff.
                for size in range(min(self.n - 1, len(context)) + 1):
                    suffix = context[-size:] if size else tuple()
                    self.context_counts[suffix][word] += 1

        if not self.vocabulary:
            raise ValueError("Cannot train on an empty corpus.")
        return self

    def _context(self, previous_tokens: List[str]) -> Tuple[str, ...]:
        return tuple(previous_tokens[-(self.n - 1):]) if self.n > 1 else tuple()

    def distribution(self, previous_tokens: List[str]) -> Dict[str, float]:
        """Return a probability distribution over known vocabulary words."""
        if not self.vocabulary:
            raise RuntimeError("Model has not been trained.")
        context = self._context(previous_tokens)
        while context not in self.context_counts and context:
            context = context[1:]
        counts = self.context_counts.get(context, Counter())
        denominator = sum(counts.values()) + self.alpha * len(self.vocabulary)
        return {
            word: (counts.get(word, 0) + self.alpha) / denominator
            for word in sorted(self.vocabulary)
        }

    def suggest(self, previous_tokens: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        probabilities = self.distribution(previous_tokens)
        return sorted(probabilities.items(), key=lambda item: (-item[1], item[0]))[:top_k]
