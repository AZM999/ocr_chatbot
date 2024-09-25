FROM        python:3.11-slim-bookworm

ENV         PYTHONUNBUFFERED=1

RUN         apt update \ 
            && apt -y install tesseract-ocr 

WORKDIR     /backend

COPY        ./requirements.txt .

COPY        ./ /backend/

RUN         ls -la /backend/*
RUN         pip install -r requirements.txt
RUN         mkdir -p uploaded_files

EXPOSE      8000

CMD         ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0", "--reload"]
