"""Command-line interface for Medical Notes Helper."""

import argparse
import sys

from medical_notes_helper.corpus import load_corpus, tokenize
from medical_notes_helper.model import NGramModel

DISCLAIMER = (
    "Administrative drafting aid only. Not for diagnosis or treatment. "
    "Use synthetic/de-identified text and review all output."
)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Suggest next words for administrative note drafting."
    )
    parser.add_argument("--corpus", default="data/admin_notes_sample.txt",
                        help="UTF-8 text corpus, one sentence per line.")
    parser.add_argument("--top-k", type=int, default=5,
                        help="Number of suggestions to display.")
    parser.add_argument("--alpha", type=float, default=1.0,
                        help="Add-k smoothing value (must be > 0).")
    parser.add_argument("--suggest", metavar="TEXT",
                        help="Print suggestions for TEXT and exit.")
    return parser


def show_suggestions(model, text, top_k):
    tokens = tokenize(text)
    suggestions = model.suggest(tokens, top_k=top_k)
    if not suggestions:
        print("No suggestions available.")
        return
    print("Suggestions:")
    for word, probability in suggestions:
        print(f"  {word:<18} {probability:.4f}")


def interactive_loop(model, top_k):
    print("\nMedical Notes Helper (administrative drafting only)")
    print(DISCLAIMER)
    print("Enter a phrase to receive next-word suggestions.")
    print("Commands: :help, :quit")
    while True:
        try:
            text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return
        if not text:
            continue
        if text.lower() in {":quit", ":q", "exit"}:
            print("Goodbye.")
            return
        if text.lower() == ":help":
            print("Type an administrative phrase; the model suggests likely next words.")
            print("Do not enter patient-identifying or sensitive information.")
            continue
        show_suggestions(model, text, top_k)


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.top_k < 1:
        raise SystemExit("--top-k must be at least 1")
    if args.alpha <= 0:
        raise SystemExit("--alpha must be greater than 0")
    try:
        sentences = load_corpus(args.corpus)
        model = NGramModel(n=3, alpha=args.alpha).fit(sentences)
    except (OSError, ValueError) as error:
        raise SystemExit(f"Error: {error}")

    if args.suggest is not None:
        print(DISCLAIMER)
        show_suggestions(model, args.suggest, args.top_k)
    else:
        print(f"Loaded {len(sentences)} synthetic/sample sentences.")
        interactive_loop(model, args.top_k)


if __name__ == "__main__":
    main()
