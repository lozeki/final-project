# Documentation
## Create the website with GitHub, Docker Cloud, and Amazon Web Services.

### Create the Project on local computer and push it to the remote repository on github

1. Create a new repository on GitHub without README, license, or gitignore files by click on the new button on repositories tab. 

2. Open Git Bash on your PC.

3. Create a folder on your PC for the project.

4. Initialize the local directory as a Git repository.
```
   $ git init
```
5. Create README.md file and add the file to your repository.
```
   $ echo "# final-project" >> README.md
   $ git add README.md
```
6. Commit it to your local repository.
```
   $ git commit -m "Create the repo for final project"
```
7. Connect your repository to github ( you can copy the remote repository URL from your github setup page).
```
   $ git remote add origin https://github.com/lozeki/final-project.git
```
8. Push the changes in your local repository to GitHub (you’ll have to type your github usename and password when you push to github).
```
   $ git push -u origin master
```
### Create the repository on Docker cloud and connect it with your repository on github

1. Create a new repository on Docker cloud and link it with your repository on github under Builds tab.

2. Configure automated builds for specific tags by click on Configure automated builds.

..* Build location - small
..* Autotest - Internal Pull Requests
..* Source type - Tag
..* Source - /^[0-9.]+$/
..* Docker Tag - release-{sourceref}

### Prepare Dockerfile, YML, an other files to run the image.

1. Build a Dockerfile to install the software we need on the server.

```
FROM ubuntu:xenial

# Location for copy all the files we need
COPY . /src

# The working location
WORKDIR /src

# Install requirement software
RUN apt-get update -y
RUN apt-get install -y --assume-yes --no-install-recommends apt-utils 
RUN apt-get install -y python3 python3-pip
RUN pip3 install Werkzeug Jinja2 Flask
```
2. Use docker-compose.test.yml file to run our desire function(We only need the test function in this project).
```
sut:
    build: .
    command: ./run_tests.sh
```
3. Create the Test run_tests.sh
```
#!/bin/bash
echo "Running Flask Unit Tests"
python3 final_web_test.py
```
4. Build the test function on final_web_test.py to control the test on the Flask webserver.
```
import unittest
import final_web

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = final_web.app.test_client()
    def tearDown(self):
        pass
    def test_home_page(self):
        # Render the / path of the website
        rv = self.app.get('/')
        # Chech that the page contians the desired phrase
        assert b'Final Project Website' in rv.data 
 
if __name__ == '__main__':
    unittest.main()
``` 
5. Create final_web.py, then Push your branch to your github, and start a pull request. The test will fail because we didn't write any code for final_web.py.

6. Build the The main program final_web.py which controls how the Flask website will run. Commit and push changes to the github branch. If the test passes, merge and submit a link to your pull request. If the test fails, redo it again. 
```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():

    return "Final Project Website"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
```
### Ansible-playbooks: A simple and Powerful automation. We use it to buid an control the version of our images.
  
####Ansible is a radically simple IT automation engine that automates cloud provisioning, configuration management, application deployment, intra-service orchestration, and many other IT needs.

1. Copy the ansible folder to the repository.

2. Use git tags to control the version of the images.
```
# Set your most recent commit to your docker-cloud-test's master branch to 0.0.1.
git checkout master
git pull origin master
git tag 0.0.1

#Push your tags to github and verify through the UI that they exist.
git push --tags origin master
```
2. Connecting to the Remote Server with SSH-key.
..*Use the private ssh key to connect with the  AWS instance.

3. Clone your repository and run the ansible-playbooks:
```
ansible-playbook configure-host.yml -v --extra-vars "student_username=tnguyen"

ansible-playbook deploy-website-production.yml -v

ansible-playbook deploy-website-staging.yml -v
```
### Use Prometheus to monitor the Python flask server

#### Prometheus is a great metrics monitoring system. We'll used it to monitor some system level metrics such as CPU and Memory utilization along with some application level metrics such as number of page loads and page load time.
..* Use Dockerfile to install prometheus library
```
pip3 install prometheus_client
```
..* Create the monitor program prometheus_metrics.py in the same place as our main code final_web.py.
```
import time
from flask import request
from flask import Response
from prometheus_client import Summary, Counter, Histogram
from prometheus_client.exposition import generate_latest
from prometheus_client.core import  CollectorRegistry
from prometheus_client.multiprocess import MultiProcessCollector

_INF = float("inf")
# Create a metric to track time spent and requests made.
REQUEST_TIME = Histogram(
    'app:request_processing_seconds', 
    'Time spent processing request',
    ['method', 'endpoint'],
    buckets=tuple([0.0001, 0.001, .01, .1, 1, _INF])
)
REQUEST_COUNTER = Counter(
    'app:request_count', 
    'Total count of requests', 
    ['method', 'endpoint', 'http_status']
)


def setup_metrics(app):
    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def increment_request_count(response):
        request_latency = time.time() - request.start_time
        REQUEST_TIME.labels(request.method, request.path
            ).observe(request_latency)

        REQUEST_COUNTER.labels(request.method, request.path,
                response.status_code).inc()
        return response

    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")
```
..* Import setup_metrics into the Python code final_web.py 
```
from prometheus_metrics import setup_metrics
setup_metrics(app)
```
..* Push everything to the remote repository on github

..* run the test with command
```
curl 54.183.61.188:8081/metrics
```
### The website use CSS and images from static folder, the default folder for addition files.
