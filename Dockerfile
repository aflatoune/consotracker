FROM python:3.9-buster
ARG PORT
ARG ADDRESS
ARG VERSION
EXPOSE ${PORT}
ENV \
    NAME=consotracker \
    MPLBACKEND=agg \
    STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false \
    STREAMLIT_CLIENT_CACHING=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ADDRESS=${ADDRESS:-} \
    STREAMLIT_SERVER_PORT=${PORT:-8501} \
    VERSION=${VERSION:-v0.0.0}
COPY . /home/
WORKDIR /home
RUN pip3 --no-cache-dir install -e . \
    && groupadd -g 1001 ${NAME} \
    && useradd -rMl -u 1001 -g ${NAME} ${NAME} \
    && chown -R ${NAME}. /home/
WORKDIR /home/app
USER ${NAME}
CMD [ "streamlit", "run", "index.py" ]
