# Let's use python 3.6 for this image.
FROM python:3.6

COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD . /app

# Make sure we have the appropriate setup software.
RUN pip install setuptools

# Run the system!
CMD [ "sh", "./app/wrapper.sh" ]
