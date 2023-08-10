FROM python:3.11
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt --no-cache-dir && chmod +x /src/start.sh
EXPOSE 80
EXPOSE 8080
CMD ["bash", "/src/start.sh"]
