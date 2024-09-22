FROM python:3.11-slim

WORKDIR /app

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip setuptools wheel

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 6224

COPY . /app/

CMD ["python", "app.py"]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD wget --no-verbose --tries=1 --spider http://localhost:6224/ || exit 1
