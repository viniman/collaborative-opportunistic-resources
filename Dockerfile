FROM python:3.6.1-alpine
RUN pip install flask
RUN pip install json
COPY app.py /app.py
CMD ["python","app.py"]