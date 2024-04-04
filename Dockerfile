# Specify base image
FROM ubuntu:22.04

# Set working directory. / is fine for most scenarios.
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=nointeractive

# Install any linux dependencies
RUN apt -y update; apt -y install --no-install-recommends -y build-essential
RUN apt-get -y update; apt-get -y install git python3-pip lsof curl libpq-dev jq redis-tools libmagic-dev
RUN apt-get -y install cmake ffmpeg
RUN apt-get -y install uvicorn

# Copy requirements.txt to working directory
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install "cython<3.0.0" wheel && pip install pyyaml==5.4.1 --no-build-isolation

RUN pip install torch==2.0.0
RUN pip install transformers==4.25.1
RUN pip install langchain==0.1.13
RUN pip install openai==1.11.0
RUN pip install whisper-timestamped==1.12.20
RUN pip install ffmpeg-python==0.2.0
RUN pip install langchain-community==0.0.29
RUN pip install langchain-core==0.1.33
RUN pip install langchain_openai==0.0.8
RUN pip install langchain-experimental==0.0.52
RUN pip install spacy==3.7.2
RUN pip install fastapi==0.75.0
RUN pip install yt_dlp==2024.3.10
RUN pip install python-dotenv==1.0.0
RUN pip install faiss-cpu==1.8.0


# Copy the rest of the files from the api directory to the working directory
# COPY api/* /usr/src/app
COPY api/* .
# COPY . .

# run API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]