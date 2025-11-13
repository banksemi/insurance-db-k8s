FROM python:3.13

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 패키지 설치 후 앱 복사
COPY app.py /app/
CMD ["python", "app.py"]
