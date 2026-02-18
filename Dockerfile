FROM python:3.10-slim

RUN groupadd -r appuser && useradd -r -g appuser -d /apps -s /sbin/nologin -c "Application User" appuser

WORKDIR /apps

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /apps

USER appuser

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
