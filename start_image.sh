# Build the docker image from the local directory.
docker build -t biomonitor .

# Run the docker image!
docker run -it -v /Volumes/:/datavolumes -v ~/Downloads:/downloads -p 8000:8000 biomonitor
