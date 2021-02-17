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