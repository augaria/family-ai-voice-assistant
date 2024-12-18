FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-gi \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools \
    gstreamer1.0-pulseaudio \
    alsa-utils \
    libasound2 \
    portaudio19-dev \
    linux-headers-generic \
    build-essential \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/local/bin/python3 /usr/bin/python3

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

RUN mkdir -p /configs
RUN mkdir -p /resources
RUN mkdir -p /logs
RUN mkdir -p /data

CMD ["start_family_ai_voice_assistant", "/configs/config.yaml"]
