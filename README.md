# Unbabel Fullstack Challenge

Hey :smile:

Welcome to our Fullstack Challenge repository. This README will guide you on how to participate in this challenge.

In case you are doing this to apply for our open positions for a Fullstack Developer make sure you first check the available jobs at [https://unbabel.com/jobs](https://unbabel.com/jobs)

Please fork this repo before you start working on the challenge. We will evaluate the code on the fork.

**FYI:** Please understand that this challenge is not decisive if you are applying to work at [Unbabel](https://unbabel.com/jobs). There are no right and wrong answers. This is just an opportunity for us both to work together and get to know each other in a more technical way.

## Challenge

We're going to build a very simple translation web app based on the Unbabel API.

You can find more info about the api at [https://developers.unbabel.com](https://developers.unbabel.com)

1) Request an API Key to your hiring manager or point of contact for the hiring process at Unbabel so you can use the API for this tutorial.  
2) Build a basic web app with a simple input field that takes an English (EN) input translates it to Spanish (ES).  
3) When a new translation is requested it should add to a list below the input field (showing one of three status: requested, pending or translated) - (note: always request human translation)   
4) The list should be dynamically ordered by the size of the translated messages   

#### Requirements
* Use Flask web framework
* Use Bootstrap
* Use PostgreSQL
* Create a scalable application. 
* Only use Unbabel's Translation API on sandbox mode
* Have tests


#### Notes
* Page load time shouldnt exceed 1 second


#### Resources
* Unbabel's API: http://developers.unbabel.com/


---
# My Solution

For my solution it's required to have installed Python>=3.7, PostgresSQL>=12.1 and Docker>=2.1.0 .

I proposed 3 different scenarios to run the web app, they differ in terms of complexity and scalability.

## First approach, running on a shell

The simplest approach it's running locally on your terminal and connecting to a Postgres hosted in the same machine.

### Setup

First thing, change the diretory to the `web` folder of this repo.

Assuming that you're already in the desired environment, do:

```bash
pip install r requirements.txt
```

Define the following environment variable:

- `UNBABEL_DB_USR`
- `UNBABEL_DB_PWD`
- `UNBABEL_API_USR`
- `UNBABEL_API_KEY`
- `UNBABEL_DB_HOST`
- `UNBABEL_DB_PORT`
- `UNBABEL_DB_NAME_DEV`

Now it's time to work on the empty DB that you created for this project. The following command will create the tables and populate the dimension tables *languages* and *translations_status* with inital data:

```bash
python manage.py db upgrade
```

And finally, running the app by doing:

```bash
python app.py
```

Go to your browser and access http://localhost:8000/en-es/.

## Tests

For the tests, I've used the `unittest` framework.

The test covers the following cases:

- Querying the database;
- Correct Response from GET to the homepage;
- Method not allowed to the homepage;
- GET to the base URL without the prefix */en-es/*;
- Method not allowed to the end point *'/en-es/translations'*;
- Correct POST to *'/en-es/translations'*;
- Bad request to *'/en-es/translations'*;
- Correct PATCH to *'/en-es/translations/\<uid\>/'*;
- PATCH with a wrong translation UID;
- Correct DELETE to *'/en-es/translations'*.

### Running the tests

Before running the tests it's necessary to define the environment variables:

- `UNBABEL_DB_USR`
- `UNBABEL_DB_PWD`
- `UNBABEL_API_USR`
- `UNBABEL_API_KEY`
- `UNBABEL_DB_HOST`
- `UNBABEL_DB_PORT`
- `UNBABEL_DB_NAME_TEST`

Then, you just need to run:

```bash
python test_app.py
```

## Second approach, running on a Docker container

Now, we're going to run the app in a Docker container, but still having the Postgres database in your machine.

In the web directory, run the following command to build the image:

```bash
docker build -t unbabel-challenge:1.0 .
```

Then, use this command, changing to the correct values the environment variables, to run the container:

```bash
run -d -p 127.0.0.1:80:8000 --rm -e DB_HOST=<DB_HOST> -e UNBABEL_API_USR=<API_USR> -e UNBABEL_API_KEY=<API_KEY> -e UNBABEL_DB_USR=<DB_USR> -e UNBABEL_DB_PWD=<DB_PWD> --name unbabel-app unbabel-challenge:1.0 
```

**NOTE**: if you're running on a Mac, set DB_HOST=docker.for.mac.host.internal to connect to the Postgres database hosted in your machine.

You can access the app using http://localhost/en-es/.

## Last approach, running with Docker-Compose

In this last approach, it's considering Nginx to be the web-server in one container, our web app in another and the Postgres database now built from an image in a third container.

Before running, go back to the root of this repo and then it's required to define the Unbabel API username *<API_USR>* and key *<API_PWD>* environment variables in the `.env` file.

To get the containers running, just run the following command to build the images and then start the services:

```bash
docker-compose build
docker-compose up -d
```

Same as before, you can access the app using http://localhost/en-es/.



