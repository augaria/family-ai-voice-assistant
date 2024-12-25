FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    sox \
    alsa-utils \
    portaudio19-dev \
    libatlas-base-dev \
    linux-headers-generic \
    libasound2 \
    pulseaudio \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry
RUN pip install --upgrade setuptools wheel

COPY src/family-ai-voice-assistant-core /app/family-ai-voice-assistant-core
COPY src/family-ai-voice-assistant-impl /app/family-ai-voice-assistant-impl
COPY src/family-ai-voice-assistant-tools /app/family-ai-voice-assistant-tools

WORKDIR /app/family-ai-voice-assistant-core
RUN poetry build && pip install dist/*.whl

WORKDIR /app/family-ai-voice-assistant-impl
RUN poetry build
RUN pip install "dist/*.whl[pvporcupine, azure-speech, openai-whisper, openai, ollama, coqui-tts]"

WORKDIR /app/family-ai-voice-assistant-tools
RUN poetry build && pip install dist/*.whl

WORKDIR /app

CMD ["start_family_ai_voice_assistant", "config.yaml"]
