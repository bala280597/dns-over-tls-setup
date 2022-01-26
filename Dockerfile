FROM python:2.7
WORKDIR /usr
COPY . .
EXPOSE 12555
CMD ["python", "./dnsovertls.py"]
