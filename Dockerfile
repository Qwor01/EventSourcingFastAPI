FROM python:3.12

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . /app

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]