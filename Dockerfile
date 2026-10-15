FROM python:3.12-slim

# вывод сразу в консоль, русский текст в UTF-8
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    DB_PATH=/app/data/houses.db \
    REPORTS_DIR=/app/reports \
    TZ=Europe/Moscow

# часовой пояс, чтобы в истории расчётов было московское время
RUN apt-get update && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# сначала библиотеки (этот шаг кэшируется, если requirements.txt не менялся)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# потом код
COPY model/ model/
COPY tests/ tests/
COPY main.py pytest.ini ./

# база и отчёты хранятся снаружи контейнера
VOLUME ["/app/data", "/app/reports"]

CMD ["python", "main.py"]
