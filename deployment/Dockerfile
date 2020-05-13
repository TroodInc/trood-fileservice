FROM python:3.6-alpine

ENV APPDIR=/home/src
ENV PYTHONPATH=$PYTHONPATH:$APPDIR

RUN mkdir -p $APPDIR
WORKDIR $APPDIR

COPY ./file_service $APPDIR/file_service
COPY ./plugins $APPDIR/plugins
COPY ./manage.py $APPDIR/
COPY ./requirements.txt $APPDIR/
COPY ./pytest.ini $APPDIR/
COPY ./docs/_static/swagger.yml $APPDIR/static/
COPY ./VERSION $APPDIR/


RUN apk add --no-cache \
    build-base cairo-dev cairo cairo-tools \
    jpeg-dev zlib-dev freetype-dev \
    postgresql-dev \
    libxml2-dev antiword ghostscript-dev poppler-utils pango-dev tesseract-ocr swig\
    gcc libxslt-dev  autoconf automake && \
    pip install --upgrade pip --force-reinstall --no-cache-dir && \
    pip install -r $APPDIR/requirements.txt --upgrade && \
    apk del --no-cache

RUN cd ~ && \
  wget http://www.gnu.org/software/unrtf/unrtf-0.21.9.tar.gz && \
  tar xzvf unrtf-0.21.9.tar.gz && \
  cd unrtf-0.21.9/ && \
  ./bootstrap && \
  ./configure && \
  make && \
  make install

RUN echo $TAG > ${APPDIR}/VERSION

EXPOSE 8000
CMD /usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8000 --reload --access-logfile - file_service.wsgi:application