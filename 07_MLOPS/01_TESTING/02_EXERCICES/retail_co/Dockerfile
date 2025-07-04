FROM continuumio/miniconda3
WORKDIR /home

# Copy the application code
COPY . .

# Install system dependencies (add build tools)
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y nano build-essential gcc

# Install Python dependencies
RUN pip install -r requirements.txt

# Default command
CMD ["python", "-m", "pytest", "tests/"]