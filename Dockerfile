FROM python:3.7
MAINTAINER Phil Davidson philip.davidson2@nhs.net

# Copy git repo to app directory
COPY . /app

# pyCIPAPI expects a copy of auth_credentials.py to be present. Won't be using it, but have copied the example version to prevent error
WORKDIR /app
COPY pyCIPAPI/example_auth_credentials.py pyCIPAPI/auth_credentials.py

# Install pyCIPAPI library and python requirements (i.e. Flask)
RUN pip install . && pip install -r service/requirements.txt

# Run Flask app
ENTRYPOINT ["python"]
CMD ["service/app.py"]