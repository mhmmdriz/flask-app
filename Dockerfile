# Gunakan image Python sebagai base
FROM python:3.9-slim

# Atur variabel lingkungan
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Buat direktori kerja untuk aplikasi
WORKDIR /app

# Salin file requirements.txt ke dalam container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi ke dalam container
COPY . /app/

# Expose port 8080 (port default Flask dalam aplikasi ini)
EXPOSE 8080

# Jalankan aplikasi
CMD ["python", "main.py"]
