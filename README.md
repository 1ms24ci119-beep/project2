# Medical Notes Helper

A local command-line tool that suggests the next word while clinic staff draft **administrative** note text. It uses a small n-gram language model with Laplace (add-k) smoothing.

> **Safety and scope:** This is an educational drafting aid, not a medical device or clinical decision-support system. It does not diagnose, recommend treatment, interpret symptoms, or verify clinical accuracy. Use only synthetic or properly de-identified text. Do not enter patient names, dates of birth, addresses, record numbers, or other identifying information. A human staff member must review every draft.

## Features

- Clean and tokenize text consistently.
- Build unigram, bigram, and trigram counts from a local corpus.
- Estimate next-word probabilities with add-k smoothing.
- Suggest likely next words from the preceding context.
- Interactive CLI and one-shot command mode.
- Synthetic starter corpus; no patient data is included.
- Unit tests for cleaning, counts, smoothing, and suggestions.

## Requirements

- Python 3.9+
- No third-party dependencies.

## Quick start

```bash
python -m medical_notes_helper --corpus data/admin_notes_sample.txt
```

At the prompt, type a short administrative phrase such as `appointment was` and press Enter. Type `:help` for commands and `:quit` to exit.

One-shot suggestions:

```bash
python -m medical_notes_helper --corpus data/admin_notes_sample.txt --suggest "follow up appointment"
```

Change the number of suggestions or smoothing value:

```bash
python -m medical_notes_helper --top-k 5 --alpha 0.5
```

## Example

```text
Medical Notes Helper (administrative drafting only)
Loaded 20 synthetic sentences.
Enter a phrase to receive next-word suggestions.
Type :help for commands, :quit to exit.

> appointment was
Suggestions:
  scheduled       0.2143
  confirmed       0.0714
  rescheduled     0.0714
```

Exact probabilities depend on the corpus and context.

## Corpus format

The starter corpus is plain text with one synthetic sentence per line. To use another corpus, save it as UTF-8 text and pass its path with `--corpus`. Use only text you are authorized to process and that has been properly de-identified. This project does not provide an anonymization guarantee or detect all personal information.

## How it works

1. **Preprocessing:** lowercase text, normalize punctuation, and split into word tokens.
2. **Counting:** count unigrams, bigrams, and trigrams from the corpus.
3. **Prediction:** use the last two words for trigram context; if unavailable, back off to the last word, then unigram frequency.
4. **Smoothing:** apply add-k smoothing so unseen continuations receive non-zero probability.
5. **Generation:** rank candidate vocabulary words by conditional probability and display the top-k suggestions.

For a context of `n-1` words, add-k smoothing is:

`P(word | context) = (count(context, word) + k) / (count(context) + k * vocabulary_size)`

This is a compact teaching implementation, not a production-grade language model.

## Project structure

```text
medical-notes-helper/
├── data/
│   └── admin_notes_sample.txt
├── docs/
│   └── DESIGN.md
├── medical_notes_helper/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── corpus.py
│   └── model.py
├── tests/
│   ├── test_corpus.py
│   └── test_model.py
├── .gitignore
├── LICENSE
└── README.md
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Limitations

- Suggestions are based only on the supplied corpus and may be repetitive or grammatically awkward.
- A small corpus produces weak estimates, especially for longer contexts.
- Add-k smoothing is simple and may reduce the probability of common phrases.
- The tool does not save notes, connect to an EHR, or transmit data.
- The tool does not perform anonymization, clinical validation, or access control.

## Future improvements

- Add a configurable corpus-quality report.
- Compare add-k smoothing with interpolation/backoff.
- Add a reviewable local draft export that avoids storing input by default.
- Add role-based templates using synthetic examples only.
