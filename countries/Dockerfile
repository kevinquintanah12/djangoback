# Use the official Python image as a base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . .


# Install gunicorn
RUN pip install gunicorn

# Run gunicorn when the container starts
CMD ["gunicorn", "countries.wsgi:application", "--bind", "0.0.0.0:8000"]

