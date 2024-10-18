# Usar una imagen base oficial de Python
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /apipython

# Copiar el archivo de requisitos
COPY requirements.txt /apipython/requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir --upgrade -r /apipython/requirements.txt

# Copiar el resto del código de la aplicación
COPY . /apipython/

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]