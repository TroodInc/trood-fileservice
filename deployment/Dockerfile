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
    apt-get install -y python3-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr libjpeg-dev swig \
    build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libxt-dev libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
RUN bash -c 'cd; curl -O https://cairographics.org/releases/cairo-1.16.0.tar.xz; tar -xvf cairo-1.16.0.tar.xz; cd cairo-1.16.0; ./configure; make; make install'
RUN ldconfig

RUN pip install -r $APPDIR/requirements.txt --upgrade

RUN echo $TAG > ${APPDIR}/VERSION

EXPOSE 8000
CMD /usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8000 --reload --access-logfile - file_service.wsgi:application
