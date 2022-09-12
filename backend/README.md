# The TRIVIA App

The Trivia App is one of the project of the Udacity Full Stack Developer Nanodegree, which in reality is a game, a quiz that invites player to answer a bunch of questions. This Python App demonstratres how one can implementing an API following best practices and documenting it.
This project was also a wonderful opportunity to learn and practice Test Driven Development.
This application has a frontend and a backend, but my main work was done in the backend.
As required we followed the PEP8 style guidelines.

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

The backend provides the API endpoints used by the frontend to work correctly.

First you may want to install and activate a virtual environment. This is useful for you to have a separate environment for your project as versions of package dependencies may vary depending on the application your are developing.

To create your virtual environment, use the following commands:
```
python -m venv venv
```

Then to activate:
```
venv\Scripts\activate
```

Next you will need to install the dependencies of your projects. From the backend folder run `pip install requirements.txt`. Required packages are provided in the requirements file. 

You can then run the application with the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
export FLASK_DEBUG=True
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.
The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

You need to have some data in the database to see how the api behaves. With Postgres running, create a `trivia` database:

```
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```
psql trivia < trivia.psql
```

Then to allow the backend to connect to the database, you will need to configure the database path. Here this path contains sensitive informations, you can configure them in a separate .env file in the backend folder. 

Before that make sure dotenv is intall with the following command:

```
pip install python-dotenv
```


Then in your .env file configure like this:

```
PROD_DATABASE = 'trivia_test'
PROD_DB_USER = 'postgres'
PROD_DB_PWD = ''
PROD_DB_HOST = 'localhost'
PROD_DB_PORT = 5432

TEST_DATABASE = 'trivia_test'
TEST_DB_USER = 'postgres'
TEST_DB_PWD = ''
TEST_DB_HOST = 'localhost'
TEST_DB_PORT = 5432
```


#### Frontend

From the frontend folder, run the following commands to start the client: 

```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
python test_flaskr.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: For now the app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: For now the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "404 Not Found: No questions found in category Religion"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: 
- 422: Not Processable 
- 500: Internal Server Error

### Endpoints 

#### GET /categories
- General:
    - Returns a list of all categories
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ]
}
```

#### GET /questions
- General:
    - Returns a paginated list of questions objects, and total number of questions, current category and all the available categories
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "current_category": "All",
  "questions": [
    {
      "answer": "Etoo Fils Samuel",
      "category": 6,
      "difficulty": 5,
      "id": 1,
      "question": "Who is the best footballer in Africa before between 2000 and 2020"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Sadio Mane",
      "category": 6,
      "difficulty": 3,
      "id": 3,
      "question": "Who is the best footballer in Africa after 2020"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Roger Milla",
      "category": 6,
      "difficulty": 5,
      "id": 7,
      "question": "Who is the best footballer in Africa before 2000"
    },
    {
      "answer": "Magnus Effect",
      "category": 1,
      "difficulty": 5,
      "id": 8,
      "question": "How do we call the way the footballer Roberto Carlos used to kick free kiiks ?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "success": true,
  "total_questions": 24
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and questions list based on current page number to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/questions/33`
```
{
    "deleted": 33,
    "questions": [
        {
            "answer": "Etoo Fils Samuel",
            "category": 6,
            "difficulty": 5,
            "id": 1,
            "question": "Who is the best footballer in Africa before between 2000 and 2020"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Sadio Mane",
            "category": 6,
            "difficulty": 3,
            "id": 3,
            "question": "Who is the best footballer in Africa after 2020"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Roger Milla",
            "category": 6,
            "difficulty": 5,
            "id": 7,
            "question": "Who is the best footballer in Africa before 2000"
        },
        {
            "answer": "Magnus Effect",
            "category": 1,
            "difficulty": 5,
            "id": 8,
            "question": "How do we call the way the footballer Roberto Carlos used to kick free kiiks ?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        }
    ],
    "success": true,
    "total_questions": 49
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, success value, total questions, and questions list. 
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Are you a human being", "answer":"Yes, I am", "category":"3", "difficulty":"3"}'`
```
{
    "created": 56,
    "questions": [
        {
            "answer": "Etoo Fils Samuel",
            "category": 6,
            "difficulty": 5,
            "id": 1,
            "question": "Who is the best footballer in Africa before between 2000 and 2020"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Sadio Mane",
            "category": 6,
            "difficulty": 3,
            "id": 3,
            "question": "Who is the best footballer in Africa after 2020"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Roger Milla",
            "category": 6,
            "difficulty": 5,
            "id": 7,
            "question": "Who is the best footballer in Africa before 2000"
        },
        {
            "answer": "Magnus Effect",
            "category": 1,
            "difficulty": 5,
            "id": 8,
            "question": "How do we call the way the footballer Roberto Carlos used to kick free kiiks ?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        }
    ],
    "success": true,
    "total_questions": 50
}
```

#### POST /fetch_category
- General:
    - Fetch questions based on category. Returns a the category, the list of questions from the specified category, success value and total questions of the category.
- `curl http://127.0.0.1:5000/fetch_category -X POST -H "Content-Type: application/json" -d '{"category":2}'`
```
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 4
}
```

#### POST /search_questions
- General:
    - Search questions based on a search term. Returns a list of questions for whom the search term is a substring of the question, success value and total questions found.
- `curl http://127.0.0.1:5000/search_questions -X POST -H "Content-Type: application/json" -d '{"search":"afr"}'`
```
{
    "questions": [
        {
            "answer": "Etoo Fils Samuel",
            "category": 6,
            "difficulty": 5,
            "id": 1,
            "question": "Who is the best footballer in Africa before between 2000 and 2020"
        },
        {
            "answer": "Sadio Mane",
            "category": 6,
            "difficulty": 3,
            "id": 3,
            "question": "Who is the best footballer in Africa after 2020"
        },
        {
            "answer": "Roger Milla",
            "category": 6,
            "difficulty": 5,
            "id": 7,
            "question": "Who is the best footballer in Africa before 2000"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Sadio Mane",
            "category": 6,
            "difficulty": 3,
            "id": 24,
            "question": "Who is the best footballer in Africa after 2020"
        },
        {
            "answer": "Roger Milla",
            "category": 6,
            "difficulty": 5,
            "id": 26,
            "question": "Who is the best footballer in Africa before 2000"
        }
    ],
    "success": true,
    "total_questions": 6
}
```

#### POST /quizzes
- General:
    - Finds a question in a given category and that is not one of the previous questions. Returns a random question in the given category that was not selected and success value.
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":3, "previous_questions": [13, 14]}'`
```
{
    "question": {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
    },
    "success": true
}
```

## Authors
Yours truly, Wilfried Deudjui Mbouwé

## Acknowledgements 
The awesome team at Udacity ie coach Caryn, coach Amy and coach Badiou !