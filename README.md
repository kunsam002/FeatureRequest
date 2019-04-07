# Feature Request App

Feature Request App allows the user to create "feature requests" by making a request for a new feature that will be
 added onto an existing piece of software.

Application hosted on http://104.248.94.181:5055/

## Prerequisites
Ubuntu OS

Python3.6

python3-pip

virtualenv

PostgreSQL

Flask

SQLAlchemy

npm

less

All dependencies and requirements can be found in the requirements.txt file

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
Pull requests are welcome. For major changes, please open an issue first or contact the developer to discuss what you
 would like to change.


## Code Solution
The Feature Request App allows users create feature requests with respect to clients, by identifying product area the
 request should categorized under. 

The following were measures taken around application workflow;

* As a form of security, only registered users can create feature requests.
* User is expected to register and login with a secured password combination.
* Logged-In user can create feature request associated with a client and product area.
* Only a Feature request author has the right to make modifications to created feature requests.
* Only a Feature request author has the right to delete an existing feature request. 