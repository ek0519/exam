FROM nginx/unit:1.23.0-python3.9

ENV APP_ROOT '/src'

COPY requirements.txt $APP_ROOT/requirements.txt

RUN apt update && apt install -y python3-pip                                  \
    && pip3 install -r $APP_ROOT/requirements.txt                                     \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

COPY .docker/fastapi/config.json /docker-entrypoint.d/config.json

COPY ./ $APP_ROOT
WORKDIR $APP_ROOT

EXPOSE 8001

CMD ["bash", "./start-reload.sh"]