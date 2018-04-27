# Build the docker image from the local directory.
docker build -t biomonitor .

# Run the docker image!
docker run -it --restart=always -v /Volumes/:/Volumes -v ~/Downloads:/Downloads -p 1492:1492 biomonitor
