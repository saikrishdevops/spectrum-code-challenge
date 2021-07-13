# Simple Python Flask Dockerized Application#

Build the image using the following command

```bash
 docker build -t simple-flask-app:latest .
```

Run the Docker container using the command shown below.

```bash
docker run --rm -v "$PWD":/app -p 5000:5000 simple-flask-app
```

The application will be accessible at http:127.0.0.1:5000 or if you are using boot2docker then first find ip address using `$ boot2docker ip` and the use the ip `http://<host_ip>:5000`


API's

organisation wise json response:

http://localhost:5000/json

organisation wise json response with sort:

http://localhost:5000/json?sort=organization

organisation wise csv response:

http://localhost:5000/csv

organisation wise csv response with sort:

http://localhost:5000/csv?sort=organization

