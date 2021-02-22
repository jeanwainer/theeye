# The Eye (submission)

This is the test submission for a job application (original briefing in the bottom of this document).
It's written in python, using django, django rest framework, postgresql and celery with rabbitmq.

The application provides two endpoints: one for receiving (and listing) events, and one for listing errors (incoming
requests that didn't validate). 

## How to run

### Using docker

Make sure you have docker and docker-compose installed.
```bash
$ git clone https://github.com/jeanwainer/theeye.git
$ sudo docker-compose up --build -d
```

The server will run at port 8002: http://localhost:8002 (check out urls and endpoints below)

### Running locally (without docker)

Make sure you are under a virtual environment and postgresql is installed.

```bash
$ git clone https://github.com/jeanwainer/theeye.git
$ cp .env-sample .env
#Please edit .env files with your postgresql credentials and rabbitmq is running
$ pip install -r requirements.txt
```

Run rabbitmq and start celery worker:
```bash
# Start rabbitmq from docker container
$ sudo docker run -d -p 5672:5672 rabbitmq:alpine
$ celery -A theeye worker --loglevel=INFO
```
Run django's development server
```bash
$ ./manage.py runserver
```
## Endpoints
There are two endpoints:

- **/theeye/events**: Endpoint for creating (POST) and listing (GET) events.
- **/theeye/errors**: Endpoint for listing requests that did not validate (wrong date, payload)

Also the **root url** will show a swagger application to use as a reusable client.


##Discussions

Provided the entities constraints, I realized that only one model (table) was needed to accomodate the data, with a
structure similar to the json request. There was no reason to create multiple tables - in fact that would only
compromise performance.
Since the payload of data varies, and the many options were not provided, I assumed by the event examples that it's
always a json object. Thus I used a JSONField for storing this data. While it seemed that keys such as "host" and "path"
are always present, I decided not to validate against that to keep it as flexible as possible. The only validations are
against:
a) Empty payload
b) Non-JSON object (such as a string)

Given the *constraints*, I understand that it was important to reply as fast as possible (*not leave them hanging*),
while at the same time delaying its processing, due to the high demand nature of this application.

For this, I used celery for queueing tasks with RabbitMQ as a broker. As soon as the request is received **and**
authenticated, it's queued for processing while a status code of **202 Accepted** returns to the client.
Processing is then done, and if it does not validate, it's entire content is saved on another table for error monitoring
(as in *use cases*).

Two API endpoints were implemented: one for inserting and listing event data, and one for listing failed requests (error
monitoring). Since session_id, category and time range needed to be queried, they may be through incremental query
parameters.


### DB and Performance
I understand that performance is a critical issue, and while the given constraints have been addressed,
there is always room for improvements. For one, it would be interesting to aggregate multiple data into a single insert
query, using `bulk_insert()`.
####Indexes
At first, I thought of creating db indexes for the searchable fields (session_id, timestamp and category).
But then I understand that this could affect INSERT performance which should be the bottleneck of this application,
so I removed those indexed.

###Validations:
The document reads:
> Different types of Events can have different validations for their payloads

And then:

> Your team should be able to monitor errors that happen in "The Eye", for example:
> An event that is sending an unexpected value in the payload

Since the validations for each type of Event have not been defined, judging by the examples given I assume that an
"unexpected value" is something that does not fit the examples, such as any value that is not a valid dictionary. 




---------------------------------------------------

# The Eye

## Story

You work in an organization that has multiple applications serving websites, but it's super hard to analyze user behavior in those, because you have no data.

In order to be able to analyze user behavior (pages that are being accessed, buttons that are being clicked, forms that are being submitted, etc..), your team realized you need a service that aggregates that data.

You're building "The Eye", a service that will collect those events from these applications, to help your org making better data-driven decisions.

## Workflow

* We don't want you to be a code monkey, some things will not be 100% clear - and that's intended. We want to understand your assumptions and approaches you've taken during the implementation - if you have questions, don't hesitate to ask
* Your commit history matters, we want to know the steps you've taken throughout the process, make sure you don't commit everything at once
* In the README.md of your project, explain what conclusions you've made from the entities, constraints, requirements and use cases of this test

## Entities

```
Application
    |
    |
  Event ---- Session
```

* An Event has a category, a name and a payload of data (the payload can change according to which event an Application is sending)
* Different types of Events (identified by category + name) can have different validations for their payloads
* An Event is associated to a Session
* Events in a Session should be sequential and ordered by the time they occurred
* The Application sending events is responsible for generating the Session identifier 
* Applications should be recognized as "trusted clients" to "The Eye"
* Appllications can send events for the same session 

Example of events:
```json
{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "page interaction",
  "name": "pageview",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}

{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "page interaction",
  "name": "cta click",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
    "element": "chat bubble"
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}

{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "form interaction",
  "name": "submit",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
    "form": {
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}
```

## Constraints & Requirements

* "The Eye" will be receiving, in average, ~100 events/second, so consider not processing events in real time
* When Applications talk to "The Eye", make sure to not leave them hanging
* Your models should have proper constraints to avoid race conditions when multiple events are being processed at the same time

## Use cases:

**You don't need to implement these use cases, they just help you modelling the application**

* Your data & analytics team should be able to quickly query events from:
  * A specific session
  * A specific category
  * A specific time range

* Your team should be able to monitor errors that happen in "The Eye", for example:
  * An event that is sending an unexpected value in the payload
  * An event that has an invalid timestamp (i.e.: future)


## Pluses - if you wanna go beyond

* Your application is documented
* Your application is dockerized
* A reusable client that talks to "The Eye"