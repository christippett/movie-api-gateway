FROM python:3.5

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && groupadd -r app \
    && useradd -r -g app app

COPY . /app
RUN chown -R app /app

COPY ./compose/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh \
    && chown app /entrypoint.sh \
    && mkdir /cert

WORKDIR /app
ENV PYTHONPATH /app

ENTRYPOINT ["/entrypoint.sh"]
