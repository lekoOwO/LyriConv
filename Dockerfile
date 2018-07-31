FROM python:3-alpine

ENV PORT 8080
ENV HOST 0.0.0.0

ADD app.py /LyriConv/
ADD lyric.py /LyriConv/
ADD modules/*.py /LyriConv/modules/
ADD requirements.txt /LyriConv/

WORKDIR /LyriConv

RUN apk add --no-cache gcc musl-dev g++ libxslt-dev

RUN pip install -r ./requirements.txt
RUN apk del gcc musl-dev g++ libxslt-dev

CMD ["python", "./app.py"]

EXPOSE 8080
