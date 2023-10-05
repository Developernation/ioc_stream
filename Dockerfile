FROM python:3.9-alpine

ADD requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
ADD . .

#WORKDIR /app

# Run app.py when the container launches
ENTRYPOINT ["python", "/app/iocstream.py"]


