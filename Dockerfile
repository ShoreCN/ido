FROM daocloud.io/python:stretch

MAINTAINER shore Chen

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 7712
CMD ["python", "Main_WF.py"]
