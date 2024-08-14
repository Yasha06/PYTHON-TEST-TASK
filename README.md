# Restaurant Menu Management API

## Description

This project provides a REST API for managing restaurant menus. The API allows user registration, restaurant creation, menu uploading for each day, voting for menus, and retrieving voting results.

## Usage

For detailed information on how to use the API, please refer to the Postman documentation:
https://documenter.getpostman.com/view/37608420/2sA3s6GAY2#07dc14aa-4c5e-4744-a540-3d5762ca518b

## Requirements

- Python 3.8+
- Flask
- flask_sqlalchemy
- Flask_Login
- Werkzeug
- SQLAlchemy

## Installation

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/yourusername/restaurant-menu-api.git](https://github.com/Yasha06/PYTHON-TEST-TASK.git)
    cd restaurant-menu-api
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database:**

    ```bash
    python
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

## Running the Application

To start the local server, run:

```bash
set FLASK_APP=main.py
flask run
