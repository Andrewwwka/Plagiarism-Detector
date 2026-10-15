# Use official Python 3.13 image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download NLTK data so it doesn't fail at runtime
RUN python -c "import nltk; nltk.download('punkt_tab'); nltk.download('punkt')"

# Copy the rest of your application code into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Command to run the FastAPI backend using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]