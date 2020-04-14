FROM python:3.6.7

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

RUN apt-get update -y && \
    apt-get install -y python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr libjpeg-dev swig 
RUN pip install -r $APPDIR/requirements.txt --upgrade

RUN echo $TAG > ${APPDIR}/VERSION

EXPOSE 8000
CMD /usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8000 --reload --access-logfile - file_service.wsgi:application
