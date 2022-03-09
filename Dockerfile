FROM python:3.9-slim
ARG PORT
ARG ADDRESS
ARG VERSION
EXPOSE ${PORT}
ENV \
    NAME=consotracker \
    STREAMLIT_DEV=true \
    MPLBACKEND=agg \
    DOWNLOAD_VERBOSE=1 \
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
    && chown -R ${NAME}. /home/ \
    if [[ ${STREAMLIT_DEV} = true ]]; then; usermod -aG sudo {NAME} ; fi
USER ${NAME}
CMD [ "streamlit", "run", "app/main.py" ]
