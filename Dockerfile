FROM python:3.9-slim

WORKDIR /Test

COPY requirements.txt .
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV NAME LibraryManagementSystem

CMD ["python", "app.py"]
