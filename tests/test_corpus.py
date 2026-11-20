import unittest

from medical_notes_helper.corpus import prepare_sentences, tokenize


class CorpusTests(unittest.TestCase):
    def test_tokenize_lowercases_and_removes_punctuation(self):
        self.assertEqual(tokenize("Appointment CONFIRMED!"), ["appointment", "confirmed"])

    def test_prepare_sentences_skips_blank_lines(self):
        self.assertEqual(prepare_sentences(["Hello clinic", "", "Next visit"]),
                         [["hello", "clinic"], ["next", "visit"]])


if __name__ == "__main__":
    unittest.main()
