# Event Sourcing App with FastAPI

Welcome to my Event Sourcing App built with FastAPI! This application aims to serve as a PoC of the principles of event sourcing to manage and persist state changes.

## Table of Contents
- [Introduction to Event Sourcing](#introduction-to-event-sourcing)
- [Advantages of Event Sourcing](#advantages-of-event-sourcing)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running the Application in Docker](#running-in-docker)

## Introduction to Event Sourcing

**Event Sourcing** is a design pattern in which changes to the application state are stored as a sequence of events. Instead of persisting the current state, each state change is captured as an immutable event and stored in the order it occurred. The current state can then be reconstructed by replaying these events.

## Advantages of Event Sourcing

- **Auditability**: Every change to the state is recorded, providing a complete audit trail.
- **Scalability**: Events can be distributed across different storage systems, allowing for scalable state management.
- **Flexibility**: Allows for replaying and reprocessing of events to reconstruct past states or fix errors.

## Installation

To get started with the application, follow these steps to set up your environment and install dependencies.

### Prerequisites

- Python 3.7+
- `virtualenv` package
- (For running in docker) Docker installed

### Steps

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/eventsourcing-app.git
    cd eventsourcing-app
    ```

2. **Create a virtual environment**

    ```bash
    python3 -m venv env
    ```

3. **Activate the virtual environment**

    On Windows:
    ```bash
    .\env\Scripts\activate
    ```
    On macOS and Linux:
    ```bash
    source env/bin/activate
    ```

4. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

After installing the dependencies, you can run the FastAPI application using the following command:

```bash
uvicorn main:app --reload
```

## Running in Docker

To run the application using Docker simply run the followint Steps:

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/eventsourcing-app.git
    cd eventsourcing-app
    ```
2. **Build the docker image**

    ```bash
    docker build -t my-fastapi-app .
    ```
2. **Run the docker container**

    ```bash
    docker run -d -p 8000:8000 my-fastapi-app
    ```
