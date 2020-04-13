# [nCOV19.US](https://ncov19.us) API Documentation

<<<<<<< HEAD
<<<<<<< HEAD
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Version: v0.1.5](https://img.shields.io/badge/release-v0.1.5-blue)
![Python Version](https://img.shields.io/badge/python-v3.7-blue)
![Build](https://github.com/ncov19-us/back-end/workflows/Build/badge.svg?branch=staging&event=push)
[![Coverage Status](https://coveralls.io/repos/github/ncov19-us/back-end/badge.svg?branch=coverall)](https://coveralls.io/github/ncov19-us/back-end?branch=coverall)
[![CodeFactor](https://www.codefactor.io/repository/github/ncov19-us/back-end/badge)](https://www.codefactor.io/repository/github/ncov19-us/back-end) 

#### Backend delpoyed at 👉 [Public API](https://api.ncov19.us/) <br>


## 1️⃣ Getting started

To get the server running locally:

1. Install `pipenv` via `conda` or `pip`
2. Create virtual env. via `pipenv install`
3. Activate virtual env. `pipenv shell`
4. Run the app, `uvicorn api:app --reload`


### TECH STACK 📚

-    FAST API
-    PyMongo

---

## 2️⃣ Endpoints
=======
=======
[![CodeFactor](https://www.codefactor.io/repository/github/ncov19-us/back-end/badge)](https://www.codefactor.io/repository/github/ncov19-us/back-end) 

>>>>>>> c678aa1... chore: updated README
#### Backend delpoyed at 👉 [api.ncov19.us](https://api.ncov19.us) <br>

## 1️⃣ Endpoints
>>>>>>> 63920e4... chore: updated README

#### Main Routes

| Method | Endpoint                | Access Control | Description                                  |
| ------ | ----------------------- | -------------- | -------------------------------------------- |
| GET    | `/news` | all users      | Fetch US News |
| POST    | `/news` | all users      | Fetch specific state and topic news from Google News API |
| GET    | `/county` | all users      | Fetches all US County level data |
| GET    | `/twitter` | all users      | Fetch and return latest CDC Tweets |
| POST    | `/twitter` | all users      | Fetch and return State specific official Twitter tweets |
| GET    | `/country` | all users      | Fetch and return JHU CSSE Country level data as timeseries |

### Refer to API Documentation 📖

[API Doc ReDoc](https://api.ncov19.us/redoc)

[API Doc Swagger](https://api.ncov19.us/docs)

<<<<<<< HEAD
<<<<<<< HEAD
[API Doc Postman](https://explore.postman.com/api/3596/ncov19us-api)

[API Doc ReDoc](https://covid19-us-api-staging.herokuapp.com/redoc)
=======
[API Doc ReDoc](https://api.ncov19.us/redoc)
>>>>>>> 0813a59... refactor: change Aaron to standard feat: adding basic test

[API Doc Swagger](https://api.ncov19.us/docs)
=======
## 2️⃣ Getting started

<<<<<<< HEAD
To get the server running locally:
>>>>>>> 63920e4... chore: updated README

1. Install `pipenv` via `conda` or `pip`
2. Create virtual env. via `pipenv install`
3. Activate virtual env. `pipenv shell`
4. Run the app, `uvicorn api:APP --reload`

### TECH STACK 📚

-    FAST API
=======
-    FastAPI
>>>>>>> 12ce435... feat: coverall badge attempt #12
-    PyMongo

---

## 4️⃣ Contributors

### Project Leaders

[<img src="https://github.com/favicon.ico" width="20"> ](https://github.com/hurshd0)    [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="20"> ](https://www.linkedin.com/in/hanchunglee/)    [<img src="https://twitter.com/favicon.ico" width="20">](https://github.com/leehanchung)    **[Han Lee](https://github.com/hurshd0)**    |    Maintainer

[<img src="https://github.com/favicon.ico" width="20"> ](https://github.com/hurshd0)    [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="20"> ](https://www.linkedin.com/in/hurshd/)    [<img src="https://twitter.com/favicon.ico" width="20">](https://twitter.com/hurshd0)    **[Hursh Desai](https://github.com/hurshd0)**    |    Maintainer

---


## 3️⃣ Contributing

When contributing to this repository, please read [CONTRUBTION](./CONTRIBUTION.md) guide.

Please note we have a [CODE OF CONDUCT](./CODE_OF_CONDUCT.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

