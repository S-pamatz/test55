# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the 'fullstack' directory contents into the container at /usr/src/app
COPY ./package/fullStack /usr/src/app/

# Install any needed packages specified in requirements.txt
# Adjust the path if requirements.txt is inside the fullStack directory
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
# Adjust the path if app.py is inside the fullStack directory
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

