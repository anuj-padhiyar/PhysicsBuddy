# start by pulling the python image
# FROM python:3.11-alpine
FROM python:3.8

# copy every content from the local file to the image
COPY . /chatbot

# switch working directory
WORKDIR /chatbot

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py"]