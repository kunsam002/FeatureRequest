# Feature Request App

Feature Request App allows the user to create "feature requests" by making a request for a new feature that will be added onto an existing piece of software.

Application hosted on http://18.191.173.166:5055/
## Installation

Database Setup (PostgreSQL)

Login to PostgreSQL console
```postgresql
create database britecorerequest;
create user postgres with encrypted password 'postgres';
grant all privileges on database britecorerequest to postgres;
```

Install and setup application

```bash
bash install.sh
```
## Running UnitTest

```bash
bash run_tests.sh

```

## Running Application

```bash
python wsgi.py

```

## Default Access Credentials

```text
username: kunsam002
password: 1234@Abcd

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first or contact the developer to discuss what you would like to change.


## Prerequisites
Linux OS

Python3.6

python3-pip

virtualenv

PostgreSQL

Flask

SQLAlchemy

npm

less

All dependencies and requirements can be found in the requirements.txt file

