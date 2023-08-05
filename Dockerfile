FROM selenium/standalone-chrome as build

USER root
RUN apt-get update && apt-get install python3-distutils xvfb -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

FROM build as install
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

FROM install
COPY app.py .

ENV PYTHONUNBUFFERED=1


ENTRYPOINT ["python3", "-u", "app.py"]