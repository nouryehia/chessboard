# Chessboard

This is the backend for Autograder 2.0

### Development
This is a pseudo-RESTful API written in Python using the FlaskAPI framework that has been Dockerized for ease
of use. It runs using gunicorn as the development server.

I recommend you use Visual Studio Code to work on this app (and the frontend). It can be downloaded
<a href="https://code.visualstudio.com" target="_blank">here</a>.
Some useful plugins to install are Python and Docker, and you'll want to install `flake8` on pip3 (use `pip3 install flake8`).
You also may want to install vscode-icons and Visual Studio Intellicode here as well.

Flake8 is a linter which enforces strict style guidlines, so make sure to keep it happy and our code will look beautiful.

To start developing: `docker-compose up -d --build`


To shut down: `docker-compose down --volumes`

To get a visual representation of the API layer once it's running, navigate to localhost:1337

We'll eventually be using <a href="https://hub.docker/com" target="_blank">DockerHub</a> for image management, so be sure
to make an account there.

### Useful Links
1. <a href="https://www.flaskapi.org/" target="_blank">Flask API documentation</a>
2. <a href="https://flask-sqlalchemy.palletsprojects.com/en/2.x/" target="_blank">Flask SQLAlchemy documentation</a>
3. <a href="https://docs.python.org/3/index.html" target="_blank">Python3 Documentation</a>
4. <a href="https://en.wikipedia.org/wiki/List_of_HTTP_status_codes" target="_blank">HTTP Status Codes</a>
5. <a href="https://medium.com/@trstringer/debugging-a-python-flask-application-in-a-container-with-docker-compose-fa5be981ec9a" target="_blank">Debugging Flask Apps</a>
6. <a href="https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints" target="_blank">Flask Blueprints Documentation</a>
7. <a href="https://stackoverflow.com/questions/41731704/use-docker-compose-with-multiple-repositories" target="_blank">Docker-Compose multiple repos together</a>


### License
This is a closed source project. Collaboration from anyone other than the Autograder team + approved guests is not allowed.
