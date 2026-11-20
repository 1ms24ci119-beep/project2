# Design notes

## Data flow

`corpus file -> tokenizer -> n-gram counters -> smoothed distribution -> ranked suggestions -> CLI`

## Model choice

A trigram model uses up to two previous tokens to estimate the next token. When a context is not present, the implementation backs off by dropping the oldest context token. Add-k smoothing assigns non-zero probability to every word in the model vocabulary.

## Privacy and safety boundaries

- The sample corpus contains fictional administrative examples only.
- All processing is local; there are no network calls or external APIs.
- The CLI does not persist typed input.
- The tool does not attempt to identify or remove personal information.
- Never use identifiable patient data in this demo.
- Suggestions must not be treated as clinical facts or instructions.

## Known trade-offs

This implementation uses a small vocabulary collected from the corpus. It cannot suggest words absent from that vocabulary. Add-k smoothing is easy to explain but is not always the best estimator for natural language. Backoff here is a simple suffix-context fallback, not a full Kneser-Ney implementation.
