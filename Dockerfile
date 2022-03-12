FROM python:3.9-slim
ARG VERSION
ARG NAME_APP
ENV \
    NAME=${NAME_APP:-consotracker} \
    MPLBACKEND=agg \
    STREAMLIT_DEV=true \
    STREAMLIT_DOWNLOAD_INFO=${STREAMLIT_LOG_LEVEL:-true} \
    STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false \
    STREAMLIT_CLIENT_CACHING=true \
    STREAMLIT_SERVER_HEADLESS=true \
    VERSION=${VERSION:-v0.0.0}

COPY . /home/
WORKDIR /home
RUN apt update -qy \
    && pip3 --no-cache-dir install -e . \
    && groupadd -g 1001 ${NAME} \
    && useradd -rMl -u 1001 -g ${NAME} ${NAME} \
    && chown -R ${NAME}. /home/ \
    && if [[ ${STREAMLIT_DEV} = true ]]; then usermod -aG sudo {NAME} ; fi
USER ${NAME}
CMD [ "sh", "-c", "streamlit run --server.port ${PORT} app/main.py" ]
