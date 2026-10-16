# 1. Use an official, lightweight Python runtime as a parent image
FROM python:3.11-slim

# 2. Set environment variables to optimize Python inside the container
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr (helps with real-time logging)
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy only requirements first to leverage Docker's cache layers
COPY requirements.txt .

# 5. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
COPY . .

# 7. Create a non-root user and switch to it for better security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# 8. Inform Docker that the container listens on port 5000 at runtime
EXPOSE 5000

# 9. Run the application using Gunicorn (production WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
