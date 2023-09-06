<div align="center">

<img src="https://sun9-62.userapi.com/impg/3zMcQewrgogSBElLFe1NzNAUCujZTi12J1D5Ig/5fV2DF9yeLM.jpg?size=512x512&quality=96&sign=1b2e8ecb1a11312e1751ee9ff4064c99&type=album" alt="logo" width="150" height="auto" />
<h1>Task Manager</h1>

[![Actions Status](https://github.com/amahmetov1998/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/amahmetov1998/python-project-52/actions)
[![project-check](https://github.com/amahmetov1998/python-project-52/actions/workflows/main.yml/badge.svg)](https://github.com/amahmetov1998/python-project-52/actions/workflows/main.yml)
<a href="https://codeclimate.com/github/amahmetov1998/python-project-52/maintainability"><img src="https://api.codeclimate.com/v1/badges/803e8528452fb88da331/maintainability" /></a>
<a href="https://codeclimate.com/github/amahmetov1998/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/803e8528452fb88da331/test_coverage" /></a>
</div>

## About
Task Manager is a management system that allows you to set tasks, assign executors and change their statuses.
Login and authentication are required to work with the system.

## Deploy
This project hosted on Render.com: https://web-task-manager.onrender.com/.
If it doesn't work, you can run the app locally.

<img src="https://sun9-28.userapi.com/impg/LkY8wLzkyS_ufzYu0ljMnJb35_jRVlHrpe6eaw/N-oFh2ujFLs.jpg?size=1280x609&quality=96&sign=552b170d79b508db4954c0c3478b7096&type=album" width="auto" height="auto" />

---
## Installation

### Python
Make sure you have the Python version 3.8.1 or higher:
```
python --version
Python 3.8.1+
```
### Poetry
The project uses Poetry as a dependency manager. [Install](https://python-poetry.org/docs/#installation) Poetry.

### Application
Clone repository and install dependencies:
```
git clone https://github.com/amahmetov/python-project-83.git
make install
```
Create `.env` file in the root and add the next variables:
```
SECRET_KEY = '{your secret key}'
```
### Migrations
Create and apply all migrations:
```
make migrate
```
## Usage
Start the gunicorn Flask server:
```
make start
```
The server will be available at http://127.0.0.1:8000.

It is possible to start it local in development mode:
```
make dev
```
The dev server will be available at http://127.0.0.1:5000.