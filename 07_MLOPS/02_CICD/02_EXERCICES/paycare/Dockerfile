FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies (add build tools)
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y nano build-essential gcc

# Install Python dependencies
RUN pip install -r requirements.txt

# Make a volume mount point for the input/output CSV files
VOLUME ["/app/input_data.csv", "/app/output_data.csv"]

# Run the application (by default, run the main ETL process)
CMD ["python", "etl.py"]