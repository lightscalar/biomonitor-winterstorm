# Build the docker image from the local directory.
docker build -t biomonitor .

# Run the docker image!
docker run -it --restart=always -v `pwd`/dist/zipped:/zipout -v `pwd`/api/data:/save -v /Volumes/:/Volumes -v ~/Downloads:/Downloads -p 5000:5000 -p 8000:8000 biomonitor
