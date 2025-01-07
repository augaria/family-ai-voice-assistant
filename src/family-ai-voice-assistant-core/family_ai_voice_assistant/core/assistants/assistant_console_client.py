import requests
import argparse

from ..contracts import ChatRequest
from ..logging import colored_print, Fore


def main():
    parser = argparse.ArgumentParser(
        description="Family AI Voice Assistant Console Client"
    )
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='API host'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='API port'
    )
    parser.add_argument(
        '--speak',
        action='store_true',
        help='speaks the answer or not'
    )

    args = parser.parse_args()

    url = f"http://{args.host}:{args.port}/chat"

    while True:
        colored_print("[User] ", Fore.CYAN, '')
        question = input()
        if question.lower() == 'q':
            break

        data = ChatRequest(
            question=question,
            speak_answer=args.speak
        ).to_dict()

        try:
            response = requests.post(url, json=data)

            if response.status_code == 200:
                colored_print(f"[Assistant] {response.text}", Fore.MAGENTA)
            else:
                colored_print(
                    (
                        f"request failed, status_code: {response.status_code},"
                        f" error: {response.text}"
                    ),
                    Fore.RED
                )

        except requests.exceptions.RequestException as e:
            colored_print(
                f"request failed, error: {e}",
                Fore.RED
            )
