FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Command to run the app
CMD ["streamlit", "run", "canvas.py", "--server.port=8080", "--server.address=0.0.0.0", "--browser.gatherUsageStats=False", "--server.enableXsrfProtection=False", "--server.enableCORS=False"]
