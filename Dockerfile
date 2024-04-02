FROM chinhlengoc/ai_demo_1_base

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt
RUN apt update
RUN apt-get install -y ffmpeg
EXPOSE 5001

CMD python3 app.py
