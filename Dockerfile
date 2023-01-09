FROM squidfunk/mkdocs-material:9.0.3

# Build-time flags
ARG BUILD_MODE=false
ARG LOCALIZE_SITE_URL=true
ARG OPTIMIZE_IMAGES=false

ARG GIT_REPO

ENV LOCALIZE_SITE_URL=$LOCALIZE_SITE_URL
ENV OPTIMIZE_IMAGES=$OPTIMIZE_IMAGES
ENV GIT_REPO=$GIT_REPO

# Environment variables
ENV PIP_NO_CACHE_DIR=1

COPY ./mkdoxin /docs/mkdoxin
COPY ./requirements.txt /docs/mkdoxin/requirements.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /docs/mkdoxin/requirements.txt && \
    mkdir /docs/site && mkdir /docs/site/version

RUN if [ "${OPTIMIZE_IMAGES}" = "true" ]; then \
    python3 -m pip install --upgrade Pillow; \
    fi

ENTRYPOINT [ "python3", "mkdoxin/mkdoxin.py" ]
