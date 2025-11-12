# 1. Base Image: Use a stable Python image
FROM python:3.11-slim

# 2. Environment Setup: Prevents Python from writing .pyc files and buffers stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Working Directory: Set the directory inside the container
WORKDIR /app

# 4. Copy Dependencies: Copy the requirements file into the container
COPY requirements.txt /app/

# 5. Install Dependencies: Run pip install to set up the Django environment
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Code: Copy all your project files into the container
COPY . /app/

# 7. Default Command: Set the command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]