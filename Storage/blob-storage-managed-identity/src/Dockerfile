#FROM python:3.12
FROM storageacrzuxtumaevhs6w.azurecr.io/bmoussaud_python_ai:0.1
LABEL author="bmpoussaud"

COPY app.py ./
COPY bitnet.py ./
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
