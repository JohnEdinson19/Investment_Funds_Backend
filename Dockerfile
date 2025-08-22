# Usa la imagen base de Python 3.11 para Lambda
FROM public.ecr.aws/lambda/python:3.11

# Copia los archivos de tu proyecto al contenedor
COPY app ${LAMBDA_TASK_ROOT}/app
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Instala las dependencias
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Establece el comando de entrada para Lambda
CMD ["app.main.handler"]