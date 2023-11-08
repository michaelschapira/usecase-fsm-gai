FROM redhat/ubi9-minimal:9.3-1361

ENV PORT=3000
ENV HOME=/app
workdir /app
copy . ./
RUN chmod -R 777 /app
RUN microdnf -y install python3 pip
RUN pip install -r requirements.txt
RUN chmod +x ./startup.sh

CMD ["./startup.sh"]


