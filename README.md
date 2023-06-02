# Social Media API
Users can create profiles, follow other users, create and retrieve posts, manage likes and comments.

## Features

- register with their email and password to create an account
- authenticate with JWT
- create and update your profile, including profile picture, bio, and other details
- view profiles of other users, search for users by username, follow and unfollow other users
- create new posts with text content and optional media attachments 
- retrieve posts of other users, search posts by tags and author name
- like and unlike posts, add comments to posts and view comments on posts
- endpoints documented with swagger
- ready to build and run on docker, dockerfile and docker-compose files provided

## Setting up project and getting started

Install using GitHUB
```sh
git clone https://github.com/amber-marichi/social-media-api.git
cd social-media-api
```

Set up variables
Prepare the .env file using .env.sample provided in project main directory. Change following values accordingly to database name, user name and password. Save file with variables as ".env"
```sh
SECRET_KEY=SECRET_KEY
POSTGRES_DB=POSTGRES_DB
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
```

### To run using Docker
!! Docker with docker compose must be installed and ready

Run docker compose command and wait for containers to build and start
```sh
docker compose up
```
Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

### To run locally
!! Python3.8+ with pip should be installed and ready.
PostgreSQL database should be running locally or in Docker with creds corresponding to ones stated in your .env file.

1. Create and activate venv:
```sh
python -m venv venv
```

2. Activate environment:

On Mac and Linux:
```sh
source venv/bin/activate
```
On Windows
```sh
venv/Scripts/activate
```

3. Install requirements:

```sh
pip install -r requirements.txt
```

4. Apply migrations

```sh
python manage.py migrate
```

5. Start the app:

```sh
python manage.py runserver
```

## To get access to the app
1. Go to registration page and enter email with password to use for access
```sh
http://127.0.0.1:8000/api/user/register/
```
2. After registration proceed to token page. Enter email and password to obtain access token. Save it to use later
```sh
http://127.0.0.1:8000/api/user/token/
```
3. Now you are ready to proceed with using service by submitting access token in http request header. Check out endpoints documentation for details.
```sh
http://127.0.0.1:8000/api/doc/swagger/
```
