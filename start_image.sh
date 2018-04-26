# Build the docker image from the local directory.
docker build -t biomonitor .

# Run the docker image!
docker run -it -v /Volumes/:/Volumes -v ~/Downloads:/Downloads -p 8000:8000 -p 5000:5000 biomonitor
