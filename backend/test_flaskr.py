import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        self.DB_USER = os.getenv('DB_USER', 'postgres')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')  
        self.DB_NAME = os.getenv('DB_NAME', 'trivia')  
        self.DB_PATH = 'postgresql://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

        self.new_question = {
            'question': 'Test_New_Question',
            'answer': 'Test_New_Answer',
            'difficulty': 1,
            'category': 1
        }
        self.new_search = {
            'searchTerm': 'is'
        }
        self.new_notfnd_search = {
            'searchTerm': 'zzzzzz'
        }
        self.new_quiz = {'previous_questions': [],
                         'quiz_category': {'type': 'Sports', 'id': 6}}
        self.up_quiz  = {'previous_questions': []}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_sent_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_sent_not_found_category(self):
        res = self.client().get('/categories/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_for_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_sent_not_found_questions_per_category(self):
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    def test_delete_question(self):
        question = Question(question='Test_Delete_Question', 
                            answer='Test_Delete_Answer', 
                            category=1, 
                            difficulty=1)
        question.insert()
        question_id = question.id

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        del_question = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(del_question, None)

    def test_422_sent_delete_unprocessable_request(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['created'])

    def test_405_sent_add_not_allowed_request(self):
        res = self.client().post('/questions/999', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_search_questions(self):
        res = self.client().post('/questions/search', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_search_not_found_question(self):
        res = self.client().post('/questions/search', json=self.new_notfnd_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_play_quiz(self):
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_play_unprocessable_quiz_request(self):
        res = self.client().post('/quizzes', json=self.up_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()