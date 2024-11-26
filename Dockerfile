# Use an official Python runtime as a parent image
FROM python:3.11

# Install git (to clone the repository)
RUN apt-get update && apt-get install -y git

RUN mkdir -p ./test && git clone https://github.com/Bhawnadixit/data_engineer_assignment.git ./test/

# Change to the /app/test/ directory
WORKDIR ./test

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 if your app needs it
EXPOSE 5000

# Define the command to run your application
CMD ["python", "run_scripts.py"]