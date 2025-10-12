FROM python:3.11-slim

# set workdir
WORKDIR /app

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY app.py .

# expose port
EXPOSE 8000

# default command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]