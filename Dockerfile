FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN python -m pip install --upgrade pip
RUN pip3 install numpy==1.12.0
RUN pip3 install "scikit_learn==0.22.2.post1"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]