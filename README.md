# Distributed systems

Replicated log app created with Python, FastAPI and Docker.

## Table of contents
* [Project structure](#project-structure)
* [Project description](#project-description)
* [Setup](#setup)


## Project structure
```
├── code                     # Sorce code.
│   ├── master.py            # Implements Master node functionality.
│   └── secondary.py         # Implements Secondary node functionality.
├── Dockerfile               # Base Dockerfile for docker-compose 
├── docker-compose.yml       # Define and run 3 docker containers
├── README.md                # This readme.
├── Pipfile                  # All necessary dependencies.
└── Pipfile.lock             # Specify dependincies from Pipfile (versions, etc.).
```

## Project description

This application consists of one master node and two secondary nodes. 
Master node replicates received messages on secondary nodes. 
HTTP is used for communication between services. 
They run in separate docker containers. 
Dockerfile is the base for all services and is used in docker-compose.yaml.

The master node has two methods:

*GET* /get-messages - This method stands for returning all messages\
*POST* /add-message - This method stands for adding new messages to the list and replicating it in the secondaries.

The secondary node has one method:

*GET* /get-messages-secondary  - This method stands for returning all messages

## Setup

To get started with application, start FastAPI services in docker using the following command:

    docker-compose up -d

Wait for a few seconds and you should be able to access API endpoints:

- Master node at  http://localhost:8000/.
- First Secondary node at  http://localhost:8001/.
- Second Secondary node at  http://localhost:8002/.

To stop running application, run the following command:

    docker-compose down -v