"""Utility module that encapsulates the dummy conversational agent logic.

This is **not** a production-ready model – it is intentionally kept simple so the
rest of the application can be demonstrated without heavy ML dependencies. The
goal of this refactor is to make the code *cleaner*, *safer* and slightly more
flexible while still retaining the original behaviour.
"""

from __future__ import annotations

import json
import logging
import random
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration & logging
# ---------------------------------------------------------------------------

MODELS_DIR = Path("models")
TRAINING_DATA_PATH = Path("data") / "training_data.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s ﹣ %(levelname)s ﹣ %(message)s")


def _ensure_training_data_store() -> None:
    """Create an empty training_data.json file if it does not exist yet."""

    if not TRAINING_DATA_PATH.exists():
        TRAINING_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        TRAINING_DATA_PATH.write_text("[]")


def load_model(model_path: str | Path) -> str:
    """Load the serialized model from *model_path*.

    For this demo the model is just a plain-text file. If the file does not
    exist we fall back to a dummy string so the rest of the pipeline can still
    operate.
    """

    try:
        with open(model_path, "r", encoding="utf-8") as f:
            logging.info("Model successfully loaded from %s", model_path)
            return f.read()
    except FileNotFoundError:
        logging.warning("No model file found at %s – using a dummy model instead", model_path)
        return "<dummy-model>"


def generate_responses(context: str, _model: str, *, num_responses: int = 5) -> list[str]:
    """Generate *num_responses* candidate replies for the given *context*.

    The implementation is intentionally naive – it simply samples responses
    from two hard-coded pools depending on whether the user seems *sad* or not.
    Offensive language is removed automatically.
    """

    sad_responses = [
        "I'm sorry to hear that. Is there anything I can do to help?",
        "It's okay to feel sad sometimes. I'm here for you.",
        "Sending you a virtual hug.",
        "I'm here to listen if you want to talk about it.",
        "Remember that this feeling will pass. You're strong.",
        "Let me know if there's anything I can do to make you feel better.",
        "You are not alone – I'm right here with you.",
    ]

    upbeat_responses = [
        "You have a great smile!",
        "I'm not a photographer, but I can picture us together.",
        "Are you a magician? Because whenever I look at you, everyone else disappears.",
        "Do you believe in love at first sight, or should I walk by again?",
        "If you were a vegetable, you'd be a cute-cumber.",
        "Is it hot in here, or is it just our conversation?",
        "If beauty were time, you'd be eternity.",
    ]

    pool = sad_responses if "sad" in context.lower() else upbeat_responses
    chosen = random.sample(pool, k=min(num_responses, len(pool)))
    logging.debug("Generated candidate responses: %s", chosen)
    return filter_responses(chosen)


_OFFENSIVE_PATTERN = re.compile(r"\b(?:hate|kill|die)\b", flags=re.IGNORECASE)


def filter_responses(responses: list[str]) -> list[str]:
    """Replace offensive replies with an apology placeholder."""

    filtered: list[str] = []
    for resp in responses:
        if _OFFENSIVE_PATTERN.search(resp):
            filtered.append("I'm sorry, I can't respond to that.")
        else:
            filtered.append(resp)
    return filtered


def get_user_feedback(responses: list[str]) -> str:
    """Blocking CLI helper that asks the user to pick the best response."""

    print("Please choose the best response (1-5):")
    for i, response in enumerate(responses, start=1):
        print(f"{i}. {response}")

    while True:
        try:
            choice = int(input())
            if 1 <= choice <= len(responses):
                return responses[choice - 1]
        except ValueError:
            pass
        print("Invalid choice. Please enter a number between 1 and 5.")


def save_conversation(context: str, responses: list[str], best_response: str) -> None:
    """Append a new training sample to *training_data.json*."""

    _ensure_training_data_store()

    with TRAINING_DATA_PATH.open("r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append(
            {
                "context": context,
                "responses": responses,
                "best_response": best_response,
            }
        )
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)


def main() -> None:
    """Simple CLI entry-point for manual data collection / testing."""

    model = load_model(MODELS_DIR / "model.txt")
    print("Model loaded.")

    context = input("Enter the conversation context: ")
    responses = generate_responses(context, model)
    best_response = get_user_feedback(responses)
    save_conversation(context, responses, best_response)
    print("Feedback saved. Thank you!")


if __name__ == "__main__":
    main()
