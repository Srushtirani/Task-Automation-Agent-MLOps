
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/home/user

WORKDIR /app

RUN useradd --create-home --uid 1000 user

COPY requirements.txt .
RUN python -m pip install --upgrade pip --timeout=180 --retries=10 && \
    python -m pip install --no-cache-dir --timeout=180 --retries=10 -r requirements.txt

COPY --chown=user:user app.py agent.py ./
COPY --chown=user:user tests ./tests

RUN chown -R user:user /app

USER user

EXPOSE 7860

CMD ["python", "-m", "streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=7860", \
     "--server.headless=true"]
