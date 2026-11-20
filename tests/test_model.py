import unittest

from medical_notes_helper.model import NGramModel


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.model = NGramModel(n=3, alpha=1.0).fit([
            ["appointment", "was", "scheduled"],
            ["appointment", "was", "scheduled"],
            ["appointment", "was", "confirmed"],
            ["form", "was", "received"],
        ])

    def test_known_context_ranks_frequent_continuation_first(self):
        suggestions = dict(self.model.suggest(["appointment", "was"], top_k=4))
        self.assertGreater(suggestions["scheduled"], suggestions["confirmed"])

    def test_smoothed_distribution_sums_to_one(self):
        distribution = self.model.distribution(["unseen", "context"])
        self.assertAlmostEqual(sum(distribution.values()), 1.0)

    def test_unseen_word_context_has_no_zero_probabilities(self):
        distribution = self.model.distribution(["unknown"])
        self.assertTrue(all(value > 0 for value in distribution.values()))

    def test_invalid_alpha_rejected(self):
        with self.assertRaises(ValueError):
            NGramModel(alpha=0)


if __name__ == "__main__":
    unittest.main()
