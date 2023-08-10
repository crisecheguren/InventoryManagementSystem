# Latest version of Python
FROM python:3.11.4

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install dependencies
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment to development
ENV FLASK_ENV=development

# Copy the sample data into the container
COPY sample_data.json .

# Run api.py when the container launches
CMD ["python", "api.py"]