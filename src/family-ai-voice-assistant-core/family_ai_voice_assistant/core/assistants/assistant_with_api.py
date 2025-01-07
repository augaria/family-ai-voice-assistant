import threading
import requests

from flask import Flask, request

from ..clients import AssistantClient
from .basic_assistant import BasicAssistant
from ..configs import ConfigManager, AssistantApiConfig
from ..contracts import ChatRequest
from ..logging import Loggers


class AssistantWithApi(AssistantClient):
    def __init__(self):
        self._app = Flask(__name__)
        self._assistant = BasicAssistant()
        self.setup_routes()

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def setup_routes(self):
        @self._app.route('/shutdown', methods=['POST'])
        def shutdown():
            self.shutdown_server()
            return 'Server shutting down...'

        @self._app.route('/chat', methods=['POST'])
        def chat():
            try:
                data = ChatRequest.from_dict(request.json)
                if (
                    data is None
                    or data.question is None
                    or data.question == ""
                ):
                    Loggers().assistant.warning(
                        "Invalid request: question is not provided"
                    )
                    return "Invalid request: question is not provided", 400
                speak_answer = (
                    data.speak_answer
                    if data.speak_answer is not None
                    else False
                )
                return self._assistant.answer(
                    question=data.question,
                    speak_answer=speak_answer,
                    enable_interrupt=False
                )
            except Exception as e:
                Loggers().assistant.warning(
                    f"Failed to answer the question: {str(e)}"
                )
                return str(e), 500

    def run(self):
        config = ConfigManager().get_instance(AssistantApiConfig)
        if config is None:
            raise ValueError("AssistantApiConfig is not provided")
        port = config.port if config.port is not None else 5000

        assistant_thread = threading.Thread(target=self._assistant.run)

        api_thread = threading.Thread(target=self._app.run, kwargs={
            'host': '0.0.0.0',
            'port': port,
            'debug': False
        })

        assistant_thread.start()
        api_thread.start()

        assistant_thread.join()
        requests.post(f'http://localhost:{port}/shutdown')

        api_thread.join()
