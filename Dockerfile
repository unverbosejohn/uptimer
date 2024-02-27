FROM python:3.11

# Working directory in the container
WORKDIR /usr/src/app

# Copy Project files
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5001

# Define environment variable
# ENV NAME Test

# Run app.py when the container launches
CMD ["python", "./main.py"]