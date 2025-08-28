# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./app /code/app
COPY ./tests /code/tests

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# Use 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
