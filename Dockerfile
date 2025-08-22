FROM public.ecr.aws/lambda/python:3.11

COPY app ${LAMBDA_TASK_ROOT}/app
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["app.main.handler"]