FROM python:3.9-slim
EXPOSE 8080
COPY . ./app
WORKDIR /app
RUN pip3 install --upgrade -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port", "8080"]
