# nCOV19.US API Documentation

#### Backend delpoyed at 👉 [Staging API](https://covid19-us-api-staging.herokuapp.com/) <br>


## 1️⃣ Getting started

To get the server running locally:

1. Install `pipenv` via `conda` or `pip`
2. Create virtual env. via `pipenv install`
3. Activate virtual env. `pipenv shell`
4. Run the app, `uvicorn api:APP --reload`


### TECH STACK 📚

-    FAST API
-    PyMongo

---

## 2️⃣ Endpoints

#### Main Routes

| Method | Endpoint                | Access Control | Description                                  |
| ------ | ----------------------- | -------------- | -------------------------------------------- |
| GET    | `/news` | all users      | Fetch US News |
| POST    | `/news` | all users      | Fetch specific state and topic news from Google News API |
| GET    | `/county` | all users      | Fetches all US County level data |
| GET    | `/twitter` | all users      | Fetch and return latest CDC Tweets |
| POST    | `/twitter` | all users      | Fetch and return State specific official Twitter tweets |
| GET    | `/country` | all users      | Fetch and return JHU CSSE Country level data as timeseries |

---

## 3️⃣ Data Model

### Refer to API Documentation 📖

[API Doc](https://covid19-us-api-staging.herokuapp.com/docs)


## 3️⃣ Environment Variables

In order for the app to function correctly, the user must set up their own environment variables.

create a .env file that includes the following:

  
    *  MONGODB_CONNECTION_URI - optional development db for using functionality not available in SQLite
    *  NEWS_API_KEY - set to "development" until ready for "production"
    *  JWT_SECRET - you can generate this by using a python shell and running import random''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#\$%^&amp;*(-*=+)') for i in range(50)])

    
## Contributing

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

