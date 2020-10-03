FROM python:3.8

RUN mkdir /server
WORKDIR /server
COPY . /server/.

RUN pip install -r requirements
RUN rm requirements.txt

ENTRYPOINT ["python", "/server/srv.py"]