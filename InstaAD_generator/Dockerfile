# 1. Base Image: Lightweight Python
FROM python:3.10-slim

# 2. Install basic system tools (curl is useful for health checks)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 3. Set working directory inside the container
WORKDIR /app

# 4. Install dependencies
COPY backend_requirements.txt .
RUN pip install --no-cache-dir -r backend_requirements.txt

# 5. Copy the entire project into the container
# This copies 'server.py' and the 'Frontend' folder (which contains 'Backend')
COPY . .

# 6. Set Environment Variable
# This is optional, but it can be useful to ensure that Python can our modules.
ENV PYTHONPATH=/app

# 7. Expose the port
EXPOSE 8000

# 8. Run the server
CMD ["python", "server.py"]