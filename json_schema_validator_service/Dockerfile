# Use the official Python image as the base
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=json_schema_validator.settings
ENV GOOGLE_CLOUD_PROJECT=ode-sbx-3228

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run Django's built-in development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]