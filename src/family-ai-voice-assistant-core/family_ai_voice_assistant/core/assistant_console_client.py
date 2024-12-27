import requests
import argparse

from .contracts import AskQuestionRequest
from .logging import colored_print, Fore


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
        '--speak_answer',
        action='store_true',
        help='speaks the answer or not'
    )

    args = parser.parse_args()

    # 构建请求的 URL
    url = f"http://{args.host}:{args.port}/ask_question"

    while True:
        colored_print("[User] ", Fore.CYAN, '')
        question = input()
        if question.lower() == 'q':
            break

        data = AskQuestionRequest(
            question=question,
            speak_answer=args.speak_answer
        ).to_dict()

        try:
            response = requests.post(url, json=data)

            if response.status_code == 200:
                colored_print(f"[assistant] {response.text}", Fore.MAGENTA)
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