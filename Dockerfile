FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -qq -y build-essential nodejs yarn
RUN mkdir /src
WORKDIR /src
ADD ./src /src
RUN pip install -r requirements/local.txt
