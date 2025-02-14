FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

LABEL maintainer=wytheli168@163.com

WORKDIR /opt

RUN apt-get update && apt-get install -y gettext

COPY requirements.txt ./

RUN pip3 --default-timeout=100 install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

COPY . .

RUN chmod +x /opt/bin/start.sh

EXPOSE 8000

CMD ["./bin/start.sh"]
