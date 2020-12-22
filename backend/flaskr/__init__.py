import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from flasgger import Swagger
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  Swagger(app)
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/categories')
  def get_categories():
    '''
    This is Trivia API GET method to fetch all trivia categories
    ---
    tags:
      - Trivia API
    responses:
      Good Response:
        description: All Trivia question Categories
      404:
        description: Category Not Found
      500:
        description: Something went wrong!
    '''
    categories=Category.query.order_by(Category.id).all()
    if len(categories) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })

  @app.route('/questions')
  def get_questions():
    '''
    This is Trivia API GET method to fetch all trivia questions
    Call this Method with page number in the URI as a query string.
    If page number is not passed, it will be considered as the request for first page.
    Maximum 10 questions are passed in a single call based on pagination.
    ---
    tags:
      - Trivia API
    parameters:
      - page: page
        in: path
        type: Integer
        required: true
        description: page number
    responses:
      Good Response:
        description: At most 10 questions returned as per pagination logic.
      404:
        description: Question Not Found!
      500:
        description: Something went wrong!
    '''
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.order_by(Question.id).all()
    categories= Category.query.order_by(Category.id).all()
    formatted_questions = [question.format() for question in questions]
    if len(formatted_questions) == 0 or page > len(questions)/QUESTIONS_PER_PAGE: 
      abort(404)

    return jsonify({
      'success': True,
      'questions': formatted_questions[start:end],
      'total_questions': len(questions),
      'categories': {category.id: category.type for category in categories},
      'current_category': None
    })

  @app.route("/questions/<int:question_id>", methods=['DELETE'])
  def delete_question(question_id):
    '''
    This is Trivia API DELETE method to Delete a particular Question.
    Call this Method with id of the question to be deleted
    ---
    tags:
      - Trivia API
    parameters:
      - question_id: question_id
        in: path
        type: Integer
        required: true
        description: ID of the Question to be deleted
    responses:
      Good Response:
        description: Deletes the question and returs the id of the deleted question.
      422:
        description: Unprocessable Request!
      500:
        description: Something went wrong!
    '''
    try:
        question = Question.query.filter(Question.id == question_id).one_or_none()
        question.delete()
        return jsonify({
            'success': True,
            'deleted': question_id
        })
    except Exception as e:
      print(f'Error ==> {e}')
      print(sys.exc_info())
      abort(422)
  
  @app.route("/questions", methods=['POST'])
  def add_question():
    '''
    This is Trivia API POST method to add a trivia question
    Receives the question and associated data from front end and saves it in Question Table.
    ---
    tags:
      - Trivia API
    parameters:
      - in: body
        question: question
        type: String
        required: true
        description: Question text
      - in: body
        answer: answer
        type: String
        required: true
        description: Answer text
      - in: body
        difficulty: difficulty
        type: Interger
        required: true
        description: Difficulty of the Question (1-4)
      - in: body
        category: category
        type: String
        required: true
        description: Category of the Question
    responses:
      Good Response:
        description: Saves the question and returns the id of the new question.
      500:
        description: Something went wrong!
    '''
    body = request.get_json()

    new_question    = body.get('question')
    new_answer      = body.get('answer')
    new_difficulty  = body.get('difficulty')
    new_category    = body.get('category')

    try:
        question = Question(question=new_question, 
                            answer=new_answer, 
                            difficulty=new_difficulty, 
                            category=new_category)
        question.insert()

        return jsonify({
            'success': True,
            'created': question.id,
        })

    except Exception as e:
      print(f'Error ==> {e}')
      print(sys.exc_info())
      abort(422)
    

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    '''
    This is Trivia API POST method to search questions with a given search string.
    Returns all the questions with search string.
    ---
    tags:
      - Trivia API
    parameters:
      - page: searchTerm
        in: body
        type: String
        required: true
        description: Search String
    responses:
      Good Response:
        description: All the questions with search string in the question text.
      404:
        description: Search String Not Found!
      500:
        description: Something went wrong!
    '''
    body = request.get_json()
    search_term = body.get('searchTerm', None)
    results=[]
    results = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term)))
    formatted_results = [result.format() for result in results]
    
    if (len(formatted_results) == 0):
      abort(404)    

    return jsonify({
        'success': True,
        'questions': formatted_results,
        'total_questions': len(formatted_results),
        'current_category': None
    })


  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    '''
    This is Trivia API GET method to filter questions by given category.
    Returns all the questions for a particular catgory.
    ---
    tags:
      - Trivia API
    parameters:
      - category_id: category_id
        in: path
        type: Integer
        required: true
        description: ID of the category
    responses:
      Good Response:
        description: All the questions for the given category id
      404:
        description: Question Not Found!
      500:
        description: Something went wrong!
    '''

    questions = Question.query.filter(Question.category == category_id).all()
    formatted_questions = [question.format() for question in questions]
    if len(formatted_questions) == 0:
      abort(404)

    return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(questions),
        'current_category': category_id
    })


  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    '''
    This is Trivia API POST method to play the Trivia Quiz.
    Returns a new question each time when called in the Quiz category.
    Front end should maintain the questions which are already asked in the session 
    and pass those previous questions with each request so that this method is 
    able to filter a new question from database which is not yet asked.
    ---
    tags:
      - Trivia API
    parameters:
      - category_id: category_id
        in: body
        type: Integer
        required: true
        description: ID of the category
    responses:
      Good Response:
        description: Send a new question to the client which is not yet asked in the quiz
      422:
        description: Unprocessable Request!
      500:
        description: Something went wrong!
    '''

    try:
      body = request.get_json()

      category = body.get('quiz_category')                             
      category_id   = category['id']
      previous_questions = body.get('previous_questions')

      if category_id == 0:
          filtered_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
      else:
          filtered_questions = Question.query.filter_by(category = category_id).filter(Question.id.notin_(previous_questions)).all()
      
      if len(filtered_questions) > 0:
        new_question = random.choice(filtered_questions).format() 
      else: 
        new_question = None

      return jsonify({
          'success': True,
          'question': new_question
      })
    except Exception as e:
      print(f'Error ==> {e}')
      print(sys.exc_info())
      abort(422)

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404
  
  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

  
  return app

    