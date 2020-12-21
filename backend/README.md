# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Refrence

## Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

To run the Trivia webpage locally, please run `npm start` from within the `frontend` directory once the backend is up and running as per instructions in `## Running the Server` section above. The webpage will run locally at the default URL  http://127.0.0.1:3000/

Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

```
400: Bad Request
404: Resource Not Found
422: Not Processable
```

## Endpoints

GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}
```

GET '/questions'
- Fetches the paginated list of questions with list of categories and number of questions in the database.
- Request Arguments: page number (in the query String), considered as page 1 if not provided.
- Returns: Paginated List of Questions (Max 10 at a time), List of categories (Dictionary of category Id and category Type), Total number of Questions and a Success Message
```
    {
    "success": True,
    "questions": [
        {
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 1,
        },
        {
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        }
    ],
    "total_questions": 2,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    }
```

DELETE '/questions/<int:question_id>'
- Deletes a particular Question.
- Request Arguments: Question Id of the question to be deleted.
- Returns: Question Id of the question which was deleted with a success message.
```
        {
            'success': True,
            'deleted': 1
        }
```

POST '/questions'
- Takes the new question entered by User and store it in the Questions table to be included in Trivia Quiz.
- Request Arguments: Fields should be passed in the request body in JSON format - Question, Answer, Category, and Difficulty
- Returns: Question Id of the question which was added with a success message.
```
        {
            'success': True,
            'created': 2
        }
```

POST '/questions/search'
- Fetches the list of questions with the search string in the Question text.
- Request Arguments: searchTerm should be passed in the request body
- Returns: List of Questions, total number of questions, current Category with a success message.
```
    {
        'success': True,
        'questions': [
            {
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 1,
            },
            {
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            }
        ],
        'total_questions': 2,
        'current_category': null
    }
```

GET '/categories/<int:category_id>/questions'
- Fetches the list of questions for a particular category
- Request Arguments: Category Id should be passed in the URI
- Returns: List of Questions, total number of questions, current Category with a success message.
```
    {
        'success': True,
        'questions': [
            {
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 1,
            },
            {
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            }
        ],
        'total_questions': 2,
        'current_category': null
    }
```

POST '/quizzes'
- Fetches a new question each time when called in the Quiz category.
- Request Arguments: Quiz category and the list of previous questions should be passed in the request body.
- Returns: A new Question with a success message.
```
    {
          'success': True,
          'question':  {
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 1,
            }
    }
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```