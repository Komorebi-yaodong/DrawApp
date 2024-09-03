FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 9001
CMD ["streamlit", "run", "main.py", "--server.port","9001"]