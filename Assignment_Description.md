RESTful services, Docker and Kubernetes
==============

***University of Amsterdam***

# 1. Introduction

This tutorial uses OpenAPI to define a RESTful web service and Python to implement it. The RESTful web service uses a database to store data.

* Swagger is an implementation of OpenAPI. Swagger provides tools that help developers design, build, document, and consume RESTful web services.
Applications implemented from OpenAPI interface files can automatically generate documentation for endpoints, parameters, and data models. This helps keep the documentation, client
libraries, and source code in sync.
You can find a short technical explanation [here](https://www.youtube.com/watch?v=pRS9LRBgjYg)

* Git is an open-source distributed version control system. Version control helps keep track of changes in a project and allows for collaboration between many developers.
You can find a short technical explanation [here](https://www.youtube.com/watch?v=wpISo9TNjfU)

* GitHub Actions automates your software development workflows from within GitHub. In GitHub Actions, a workflow is an automated process that you set up in your GitHub
repository. You can build, test, package, release, or deploy any project on GitHub as a workflow.

* Docker performs operating-system-level virtualization, also known as "containerization". Docker uses the resource isolation features of the Linux kernel to allow independent
"containers" to run within a Linux instance.
You can find a short technical explanation on containerization [here](https://www.youtube.com/watch?v=0qotVMX-J5s)


* Kubernetes is an open-source container orchestration system for automating software deployment, scaling, and management.
You can find a short technical explanation on container orchestration [here](https://www.youtube.com/watch?v=kBF6Bvth0zw)

# 2. Tutorial


The steps of this tutorial are as follows:

1. [Write OpenAPI definition using SwaggerHub](#22-openapi-definition)  
2. [Generate the service stubs in Python](#25-generate-python-code)  
3. [Implement the logic](#26-implement-the-logic)  
4. [Build and Test Docker Image](#27-docker-image)
5. [Write Tests](#28-testing)  
6. [Deploy Web Service on Kubernetes](#29-deploy-web-service-on-kubernetes)
7. [Hands-on Exercises](#3-hands-on-exercise)
8. [Questions](#4-questions)



## 2.1 Prerequisites
* **Create GitHub Account**: In case you don’t have a GitHub account, follow these instructions to create one: [https://github.com/join](https://github.com/join)

* **Setup Docker Hub**: If you do not have a Docker Hub account, follow these instructions to create one: [https://hub.docker.com/signup](https://hub.docker.com/signup)

* **SwaggerHub Account:** If you have a GitHub account, you may go to [https://app.SwaggerHub.com/login](https://app.SwaggerHub.com/login) 
and select 'Log In with GitHub'. Alternatively, you can select to sign up.

* **Docker and Docker Compose:** You can find instructions on how to install Docker here: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
You may also find a detailed tutorial on Docker here: [https://docker-curriculum.com/](https://docker-curriculum.com/). To verify that Docker is installed correctly, run:
    ```shell
    docker run hello-world
    ```
  You can find instructions on how to install Docker Compose here: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/) 

* **PyCharm:** In this tutorial, we will use the PyCharm Integrated Development Environment (IDE). If you have a
preferred IDE, you are free to use it. You can find instructions on how to install PyCharm here: [https://www.jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)

    If you are using snap, you can type:
    ```shell
    sudo snap install PyCharm-community --classic
    ```
    You may also find a detailed tutorial on PyCharm here: 
    [https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html](https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html)



## 2.2 OpenAPI Definition
In this section, we will define a web service interface that will support the Create, Read, Update, Delete (CRUD) pattern 
for manipulating resources using OpenAPI. For a more in-depth understanding of Swagger and OpenAPI, you may follow this tutorial:
[https://idratherbewriting.com/learnapidoc/openapi_tutorial.html](https://idratherbewriting.com/learnapidoc/openapi_tutorial.html)

Log in to your SwaggerHub account at [https://app.SwaggerHub.com/login](https://app.SwaggerHub.com/login) and select 'Create New' -> 'Create New API'

<img src="/images/swhub1.png" alt="swagger" width="800"/>

Name your API 'tutorial'.

Then select version 3.0.x and 'Template' 'Simple API' and press 'CREATE API'.

<img src="/images/swgub2.png" alt="swagger" width="800"/>

You will get an OpenAPI template

<img src="/images/swgub3.png" alt="swagger" width="800"/>


Replace the definition with the following: [openAPI_1.yaml](sources/openAPI_1.yaml)

You will notice that the editor at the bottom throws some errors:
```
Errors (2)
$refs must reference a valid location in the document
$refs must reference a valid location in the document
```

This indicates that "#/components/schemas/Student" is not defined. 
You can find more about '$refs' here: [https://swagger.io/docs/specification/using-ref/](https://swagger.io/docs/specification/using-ref/)


## 2.3 Define Objects
Scroll down to the bottom of the page and create the following nodes:
* components
  * schemas
    * Student
    * GradeRecord


The code should look like this:
```yaml
components:
  schemas:
    Student:
      type: object
      required:
        - first_name
        - last_name
      properties:
        ...
    GradeRecord:
      type: object
      required:
        - subject_name
        - grade
      properties:
        ...
```


Define the properties of the Student and GradeRecord objects.

The Student properties to define are:

| Property Name | Type                    | 
|---------------|-------------------------|
| student_id    | number (integer format) | 
| first_name    | string                  |
| last_name     | string                  |
| grade_records  | array                   |

The GradeRecord properties to define are:

| Property Name | Type                                            | 
|---------------|-------------------------------------------------|
| subject_name  | string                                          | 
| grade         | number ( float format, minimum: 0, maximum: 10) |                                   |


---

 **NOTE**

Note which properties are required and which are optional. This affects the service’s validation process.
 To get more information on the 'required' see: [https://swagger.io/docs/specification/data-models/data-types/](https://swagger.io/docs/specification/data-models/data-types/) in the 
 'Required Properties' Section.

---

It is helpful to add 'example' fields in the properties. That way, your API is easier to consume.

You can find details about the 'example' field here: [https://swagger.io/docs/specification/adding-examples/](https://swagger.io/docs/specification/adding-examples/)
You can find details about data models here: [https://swagger.io/docs/specification/data-models/](https://swagger.io/docs/specification/data-models/)

## 2.4 Add Delete method

At the moment, the API definition only has 'GET' and 'POST' methods. We will add a 'DELETE' 
method. Under the '/student/{student_id}' path add the following:
```yaml
    delete:
      summary: deletes a student
      description: |
        delete a single student 
      operationId: delete_student
      parameters:
      - name: student_id
        in: path
        description: the uid
        required: true
        schema:
          type: number
          format: integer
      responses:
        "200":
          
        "400":
          
        "404":
          
```
You will need to fill in the proper responses for 200, 400, and 404. More information about responses can be found here: [https://swagger.io/docs/specification/describing-responses/](https://swagger.io/docs/specification/describing-responses/)

## 2.5 Generate Python Code

Now that we have the OpenAPI definitions, we can generate the Python server stub. Select 'Codegen'->'Server Stub'->
'python-flask'

<img src="/images/swgub6.png" alt="swagger" width="800"/>


Save the 'python-flask-server-generated.zip' and unzip the archive. Open PyCharm and open the project.

<img src="/images/pych1.png" alt="swagger" width="800"/>


To create the virtual environment for the project, go to 'File'->'Settings'->'Project'->'Python Interpreter' or ‘PyCharm'->'Preferences'->Project'->'Python Interpreter'. Select Python version 3.8 or later. Then select the gear icon to add a new environment:

<img src="/images/pych2.png" alt="swagger" width="800"/>

Select 'New environment' and press 'OK' 

Replace the 'requirements.txt' file with this [requirements.txt](sources/requirements.txt)

Open the 'requirements.txt' file and right click and select install all packages.

---


<img src="/images/pych3.png" alt="swagger" width="800"/>

Open the file 'swagger_server/swagger/swagger.yaml' and in the section 'servers' you should have only one url and description.
The servers section should look like this:
```yaml
servers:
- url: https://virtserver.swaggerhub.com/tutorial/1.0.0
  description: SwaggerHub API Auto Mocking
```

Keep only one server entry so the service starts at [http://localhost:8080/tutorial/1.0.0/ui/](http://localhost:8080/tutorial/1.0.0/ui/).


Open the '\_\_main\_\_.py' file and press Run to start the flask server: 

<img src="/images/pych4.png" alt="swagger" width="800"/>

The API UI will be available at [http://localhost:8080/tutorial/1.0.0/ui/](http://localhost:8080/tutorial/1.0.0/ui/) .  

On the UI select 'POST' and 'Try it out':

<img src="/images/pych6.png" alt="swagger" width="800"/>


The response body should be: "do some magic!"
In PyCharm if you open the 'default_controller.py' file, you'll see that the method 'add_student' returns the string "do some magic!".


---

 **NOTE**

 If you make any changes to the code you'll need to restart the flask server. 

---


## 2.5 Git Repository
Create a private Git repository.

---

 **IMPORTANT**

 **Don't forget to make your repository public from the day of submission and onwards.**

---

Go to the directory of the code and initialize the git repository and 
push the code:
```shell
git init
git add .
git commit -m "first commit"
git remote add origin <REPOSETORY_URL>
git push -u origin main
```

## 2.6 Implement the logic

In PyCharm create a package named 'service'. To do this, right-click the 'swagger_server' package select 'New'->
'Python Package' and enter the name 'service'

<img src="/images/pych7.png" alt="swagger" width="300"/>

Inside the service package create a new python file named 'student_service'
In the student_service add the following code: [student_service.py](sources/student_service.py)

Now you can add the corresponding methods in the 'default_controller.py'. To do that on the top of the 'default_controller.py' add:

```python
from swagger_server.service.student_service import *
```

In the 'add_student' method, add 'add(body)' to the return statement. so now the method becomes :

```python
def add_student(body=None):  # noqa: E501
    """Add a new student

    Adds an item to the system # noqa: E501

    :param body: Student item to add
    :type body: dict | bytes

    :rtype: float
    """
    if connexion.request.is_json:
        body = Student.from_dict(connexion.request.get_json())  # noqa: E501
        return add(body)
    return 500,'error'
```

Do the same for the rest of the methods. For example, in the ‘delete_student’ method in the 'default_controller.py' file, you need to add ‘delete(student_id)’ in the return statement. 

In general, it is a good idea to write an application using layered architecture. By segregating 
an application into tiers, a developer can modify or add a layer instead of reworking the 
entire application.

This is why we should create a new package in the code called 'service' and a python file named
'student_service.py'. In this code template we use a simple file-based database to store and 
query data called TinyDB. 

More information on TinyDB can be found here: [https://tinydb.readthedocs.io/en/latest/getting-started.html](https://tinydb.readthedocs.io/en/latest/getting-started.html)
Now, the 'default_controller.py' just needs to call the service's methods. 

---

 **NOTE**

 Don't forget to regularly commit and push your code.

---

## 2.7 Docker Image 

You can now build your web service as a Docker image and push it to Docker Hub. To do that, open the Dockerfile 
in the PyCharm project and change the python version from:
```Dockerfile
FROM python:3.9-alpine
```
To:
```Dockerfile
FROM python:3.8-alpine
```

So the Dockerfile will look like this: [Dockerfile](sources/Dockerfile)

Open a new terminal in the location of the Dockerfile and type:
```
docker build --tag <REPO_NAME>/student_service .
```

If the command fails, you may need to use sudo.
Now test the image:

```
docker run -it -p 8080:8080 <REPO_NAME>/student_service
```

---

 **NOTE**

 Don't forget to stop the server from PyCharm otherwise, you'll get an error:
 ```
 shell docker: Error response from daemon: driver failed programming external connectivity on endpoint trusting_joliot (8cbc8523e15eb68f343d048ab59a9e6d): Error starting userland proxy: listen tcp4 0.0.0.0:8080: bind: address already in use. ERRO[0001] error waiting for the container: context canceled
```

---

## 2.8 Testing

Before writing the tests in Github you need to create a token in Docker hub. To do that follow these instructions: [https://docs.docker.com/docker-hub/access-tokens/](https://docs.docker.com/docker-hub/access-tokens/)
Next you need to add your Docker hub and token to your Github project secrets.
To create secrets follow these instructions [https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)

You need to create two secrets, one named REGISTRY_USERNAME and one REGISTRY_PASSWORD.
Therefore, you need to run the above instructions twice. The first time the name of the secret will be REGISTRY_USERNAME, and the second will be REGISTRY_PASSWORD.

In your code directory create a new folder named 'postman'. In the new 'postman' folder add these files: 
* [collection.json](sources/collection.json)
* [environment.json](sources/environment.json)

Make sure your code in the Git repository is up-to-date. Go to the repository page and create a new file with 
'Add file'->'Create new file'. On the top define the path of your file.

```
.github/workflows/main.yml
```


Set the contents of your file as: [main.yml](sources/main.yml)

Commit and push your changes to GitHub. After that, any time you commit new code to your repository, your code will be automatically tested, and the Docker container will be built and pushed in DockerHub. 

To check the tests, you can go to your Github repository and click on 'Actions'. After the action is completed, the build container should be in your Dockerhub registry. 


---

 **NOTE**

 Remember to fill in the REPO_NAME in main.yml, which should be your docker hub **username**, NOT your docker hub 
 repository name.
 
The REGISTRY_USERNAME is your **username** for docker hub, NOT your docker hub repository name.

---


## 2.9 Deploy Web Service on Kubernetes 

To deploy the web service on a Kubernetes (K8s) cluster, you may use Minikube or MicroK8s. 

### 2.9.0 Minikube
You can find Minikube installation instructions: 
[https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/). 
After you complete the installation, make sure you start Minikube by typing:
```shell
minikube start --addons=ingress,ingress-dns,metrics-server
```

### 2.9.1 MicroK8s 

You can find MicroK8s installation instructions: [https://MicroK8s.io/](https://MicroK8s.io/)

If you have access to a cloud VM you may install MicroK8s there. Alternatively, you may also use 
VirtualBox: [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)

After you complete the installation, make sure you start MicroK8s and enable DNS
```shell
microk8s start
microk8s enable dns
```

---

 **NOTE**

 In Linux, you may need to use these commands with sudo 
 
 If you get an error:
 ```
 sudo: microk8s: command not found
 ```
 
 /snap/bin is probably not in your path.  Either use: \
 
 ```
 sudo /snap/bin/microk8s start
 ```
 or add /snap/bin to your PATH.

---


## 2.10 Test K8s Cluster

This is a basic Kubernetes deployment of Nginx. On the master node, create a Nginx deployment:
```shell
microk8s kubectl create deployment nginx --image=nginx
```

You may check your Nginx deployment by typing:
```shell
microk8s kubectl get all
```

The output should look like this:
```shell
NAME                         READY   STATUS              RESTARTS   AGE
pod/nginx-748c667d99-zdxh6   0/1     ContainerCreating   0          13s

NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.152.183.1   <none>        443/TCP   2m54s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   0/1     1            0           35s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-748c667d99   1         1         0       13s
```
You will notice in the first line 'ContainerCreating'. This means that the K8s cluster is downloading and starting the 
Nginx container. After some minutes, if you run again:
```shell
microk8s kubectl get all
```

The output should look like this:
```shell
NAME                         READY   STATUS    RESTARTS   AGE
pod/nginx-748c667d99-zdxh6   1/1     Running   0          43s

NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.152.183.1   <none>        443/TCP   3m24s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   1/1     1            1           65s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-748c667d99   1         1         1       43s
```

At this point, Nginx is running on the K8s cluster, however it is only accessible from within the cluster. To expose 
Nginx to the outside world, we should type: 
```shell
microk8s kubectl create service nodeport nginx --tcp=80:80
```

To check your Nginx deployment type:
```shell
microk8s kubectl get all
```

You should see the among others the line:
```shell
service/nginx        NodePort    10.152.183.82   <none>        80:31119/TCP   9s
```

This means that port 80 is mapped on port 31119 of each node in the K8s cluster. 

---

 **NOTE**

 The mapped port will be different on your deployment. Now we can access Nginx from 
 http://IP:NODE_PORT .

---

You may now delete the Nginx service by using:
```shell
microk8s kubectl delete service/nginx
```

## 2.11 Deploy Web Service on K8s Cluster

To deploy a RESTful Web Service on the K8s Cluster create a folder named
'service' and add this file in the folder:
[student_service.yaml](sources/student_service.yaml)

Open 'student_service.yaml' and replace the line:
```yaml
image: IMAGE_NAME
```
with the name of your image as typed in the docker push command. 


If you choose to integrate with an external database, you will need to add the Deployment and 
service for MongoDB:
[mongodb.yaml](sources/mongodb.yaml)

To create all the deployments and services, type in the K8s folder:
```shell
microk8s kubectl apply -f .
```

This should create the my-temp-service deployments and services. To see what is running on the cluster type:
```shell
microk8s kubectl get all
```
You should see something like this:
```shell
NAME                           READY   STATUS    RESTARTS   AGE
pod/nginx-6799fc88d8-q7hzv     1/1     Running   0          21m
pod/service-6c75dff7db-57sw5   1/1     Running   0          53s

NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
service/kubernetes   ClusterIP   10.152.183.1     <none>        443/TCP          26m
service/service      NodePort    10.152.183.176   <none>        8080:30726/TCP   53s

NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx     1/1     1            1           21m
deployment.apps/service   1/1     1            1           53s

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-6799fc88d8     1         1         1       21m
replicaset.apps/service-6c75dff7db   1         1         1       53s

```

Note that in this output, 'service/service' is mapped to 30726. In your case, it may be a different number.

Now your service should be available on http://IP:NODE_PORT/


# 3. Exercises 

## 3.1 MongoDB Integration

The code provided above uses an internal database called TinyDB. Change the 
code so that your service saves data in a MongoDB. This includes configuration 
files for the database endpoint, database names, and the Dockerfile, etc.
For testing your code locally use this file: 
[docker-compose.yaml](sources/docker-compose.yaml). Make sure you replace the 
image with your own.

---

 **NOTE**

 The docker-compose.yaml file above will be also used to run the postman tests.  
 If you need to install Docker Compose you can follow the instructions here: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/) .

---

## 3.2 Add New Method

Add a new method to the web service that will return the average grade of a student.
The new method should be a GET method with the following path:

```
/student/{student_id}/average_grade
```

The method should return the average grade of the student with id 'student_id'.
The method should return a 404 error if the student does not exist or if the student has no grades.
Add the new method to the OpenAPI definition, implement the logic, and test it.

# 3.3 Questions

1. Explain how OpenAPI helped you in the development of the RESTful web service.
2. In which cases is TinyDB preferred over MongoDB, and vice versa?