# Use the official Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /claims-api/

# Copy the local directory contents into the container at /claims-api
COPY . /claims-api
COPY keys/jwt_key.pub.pem /var/jwt_key.pub.pem
COPY keys/jwt_key /var/secrets/jwt_key

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Specify the volume for data stored in /opt/claims-api/
VOLUME ["/opt/claims-api"]

# Set the environment variable for the application to use the data from /opt/claims-api/
#ENV DATA_DIR /opt/claims-api/


# Set the entry point to run the application
CMD ["python","app.py"]
