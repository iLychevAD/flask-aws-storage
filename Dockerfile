#FROM python:alpine3.7
FROM public.ecr.aws/bitnami/python:3.7
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
