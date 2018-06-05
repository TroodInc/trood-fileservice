FROM python:3

ENV APPDIR=/home/src
ENV PYTHONPATH=$PYTHONPATH:$APPDIR

RUN mkdir -p $APPDIR
WORKDIR $APPDIR

COPY ./file_service $APPDIR/file_service
COPY ./manage.py $APPDIR/
COPY ./requirements.txt $APPDIR/
RUN pip install -r $APPDIR/requirements.txt

EXPOSE 8000
CMD /usr/local/bin/gunicorn -b 0.0.0.0:8000 --reload --access-logfile - file_service.wsgi:application