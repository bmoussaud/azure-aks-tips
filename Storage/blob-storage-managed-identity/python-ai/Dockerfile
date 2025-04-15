FROM python:3.12
LABEL author="bmpoussaud"
LABEL description="Python AI application Hugging Face and Azure Blob Storage"
# Update system packages to address vulnerabilities
#RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*
#RUN apt install curl git 
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

