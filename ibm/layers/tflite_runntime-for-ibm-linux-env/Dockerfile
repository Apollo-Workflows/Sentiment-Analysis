FROM ibmfunctions/action-python-v3.7
COPY requirements.txt ./
COPY * ./
RUN echo "deb http://ftp.debian.org/debian sid main" >> /etc/apt/sources.list && apt-get update && apt-get -y -t sid install libc6 libc6-dev libc6-dbg && rm -r /var/lib/apt/lists/*
RUN pip install -r requirements.txt