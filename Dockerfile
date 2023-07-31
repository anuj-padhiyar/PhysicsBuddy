# start by pulling the python image
# FROM python:3.11-alpine
FROM python:3.9-slim

# switch working directory
WORKDIR /app

# copy every content from the local file to the image
COPY . /app

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
# configure the container to run in an executed manner
# ENTRYPOINT [ "python" ]

CMD ["python", "app.py"]
