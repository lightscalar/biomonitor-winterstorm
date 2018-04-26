# Let's use python 3.6 for this image.
FROM python:3.6

ADD . /app

# Make sure we have the appropriate setup software.
RUN pip install setuptools

# Get the necessary software for the image.
RUN pip install -r ./app/requirements.txt

# Run the system!
CMD [ "sh", "./app/wrapper.sh" ]
