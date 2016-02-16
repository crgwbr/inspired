FROM python:3.5
ENV PYTHONUNBUFFERED 0

RUN mkdir /code
WORKDIR /code

# Install setup tools
RUN wget https://bootstrap.pypa.io/ez_setup.py -O - | python
RUN pip install --upgrade pip

# Install requirements
ADD requirements.txt /code
RUN pip install -r requirements.txt

# Add rest of code
ADD . /code/
