FROM python:3.10-slim
WORKDIR /app

# Step 1: Copy requirements from the folder where you just saw them
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 2: Copy the rest of your files (ui.py, agent.py, etc.)
COPY app/ .

EXPOSE 8501

# Step 3: Run ui.py (since it is now in the container's root /app)
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]