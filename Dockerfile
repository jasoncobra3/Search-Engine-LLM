# Base image (official Python 3.9 slim)
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files (except those in .dockerignore)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Health check (optional but recommended)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Launch command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]