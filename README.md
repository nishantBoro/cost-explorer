# Cost Explorer

## Install dependencies:

```
virtualenv <env-name>
source <env_name>/bin/activate
pip3 install requirements.txt
```

## Settings.py:

Open ./costExplorer/settings.example.py
Configure your database, put your secret key and rename the file as settings.py

## Migrate data to your database:

This will create all the necessary tables in the database:

```
python3 manage.py makemigrations
python3 manage.py migrate
```
### Populate your database with this SQL Dump: https://drive.google.com/file/d/1aF_u32ASu0o6Ah9cdKxPYvj7dDeSnVE-/view?usp=sharing

## Create Super-user

This will create a superuser/admin for the site:

```
python3 manage.py createsuperuser
.
.
python3 manage.py makemigrations
python3 manage.py migrate
```

## Run development server

```
python3 manage.py runserver

```
