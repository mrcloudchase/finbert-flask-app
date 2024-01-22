
# Docker Configuration for FinBERT Flask Application

This README provides information about the Docker configuration for containerizing the FinBERT Flask application.

## Dockerfile Explanation

The `Dockerfile` in this directory is used to build a Docker image for the FinBERT Flask application. Here's a breakdown of its contents:

- `FROM python:3.8-slim-buster`: This line specifies the base image, using Python 3.8 on a slim Buster variant.
- `WORKDIR /app`: Sets the working directory inside the container to `/app`.
- `COPY finbert/ /app/finbert`: Copies the pre-downloaded FinBERT model and tokenizer files into the container.
- `COPY requirements.txt .`: Copies the `requirements.txt` file into the container.
- `RUN pip3 install -r requirements.txt`: Installs the Python dependencies defined in `requirements.txt`.
- `COPY app/. .`: Copies the application code into the container's working directory.
- `CMD ["python3", "app.py"]`: The command that runs the Flask application when the container starts.

## Building the Docker Image

To build the Docker image, run the following command in the root directory of the project (where the Dockerfile is located):

```bash
docker build -t finbert-flask-app:latest .
```

This command builds the Docker image with the tag `finbert-flask-app:latest`.

## Running the Container

After building the image, you can start a container with:

```bash
docker run -p 5000:5000 finbert-flask-app:latest
```

This command runs the container and maps port 5000 of the container to port 5000 on the host machine, allowing you to access the Flask application at `http://localhost:5000`.

## Notes

- Ensure the `finbert/` directory with the model and tokenizer files is present as expected by the Dockerfile.
- Adjust the Docker build and run commands according to your project setup and requirements.
