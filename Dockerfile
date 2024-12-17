FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    alsa-utils \
    libasound2 \
    portaudio19-dev \
    linux-headers-generic \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry
RUN pip install --upgrade setuptools wheel
RUN pip install playsound==1.3.0

COPY src/family-ai-voice-assistant-core /app/family-ai-voice-assistant-core
COPY src/family-ai-voice-assistant-impl /app/family-ai-voice-assistant-impl
COPY src/family-ai-voice-assistant-tools /app/family-ai-voice-assistant-tools

WORKDIR /app/family-ai-voice-assistant-core
RUN poetry build && pip install dist/*.whl

WORKDIR /app/family-ai-voice-assistant-impl
RUN poetry build && pip install dist/*.whl

WORKDIR /app/family-ai-voice-assistant-tools
RUN poetry build && pip install dist/*.whl

WORKDIR /app
COPY config.yaml /app/config.yaml

CMD ["start_family_ai_voice_assistant", "config.yaml"]
