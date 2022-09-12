
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        load_dotenv('./.env')
        self.database_name = os.getenv('TEST_DATABASE')  # 'trivia'
        self.database_user = os.getenv('TEST_DB_USER')
        self.database_pwd = os.getenv('TEST_DB_PWD')
        self.database_host = os.getenv('TEST_DB_HOST')
        self.database_port = os.getenv('TEST_DB_PORT')
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "postgres", "localhost:5432", self.database_name)
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(
            self.database_user, self.database_pwd, self.database_host, self.database_port, self.database_name)        
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.new_question = {"question": "Who is the author of the novel Anansi Boys", "answer": "Neil Gaiman", "difficulty": 4, "category": 5}

            self.quiz_questions = {
                            "quiz_category": 3,
                            "previous_questions": [5, 12]
                        }
            
            self.quiz_questions2 = {
                            "quiz_category": 2,
                            "previous_questions": [16, 17, 18, 19]
                        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """Test Get All Available Categories_____________ """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data['success'], True)
        # self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions_by_category(self):
        """Test Get Questions By Category"""
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data['success'], True)
        # self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        """Test Get Questions Per Page """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])

    def test_get_paginated_questions_in_specific_category(self):
        """Test Get Questions Per Page In Specific Category """
        res = self.client().get('/questions?category=Science')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], 'Science')

    def test_get_paginated_questions_of_category(self):
        """Test Get Questions of a Category With Post"""
        res = self.client().post('/fetch_category', json={"category": "3"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])        
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], 'Geography')
    
    def test_get_paginated_questions_in_undefined_category(self):
        """Test Get Questions Per Page In Undefined Category """
        res = self.client().get('/questions?category=Toto')
        data = json.loads(res.data)         

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "404 Not Found: No questions found in category Toto")

    def test_404_get_questions_beyond_valid_page(self):
        """Test Get Questions Beyong Valid Page """
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "404 Not Found: No questions on this page")

    #def test_delete_question(self):
    #    """Test Get Delete Specific Question """
    #    res = self.client().delete("/questions/32")
    #    data = json.loads(res.data)

    #    question = Question.query.filter(Question.id == 32).one_or_none()

    #    self.assertEqual(res.status_code, 200)
    #    self.assertEqual(data["success"], True)
    #    self.assertEqual(data["deleted"], 32)
    #    self.assertTrue(data["total_questions"])
    #    self.assertTrue(len(data["questions"]))
    #    self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        """Test Get Delete Non Existing Question """
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(
                data["message"],
                "422 Unprocessable Entity: unprocessable"
            )

    def test_create_new_question(self):
        """Test Get Create New Question """
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))

    def search_questions(self):
        """Search for questions based on search term"""
        res = self.client().post("/questions", {"search": "ovel"})
        data = json.loads(res.data)
        search = "%"+f"ovel"+"%"
        questions = Question.query.filter(
            Question.title.ilike(search)).order_by(
            Question.id).all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(questions), len(data['questions']))
        for i, question in enumerate(questions):
            self.assertEqual(question, data['questions'][i]['question'])

    def test_get_question_to_play(self):
        """Test Get New Question Play """
        res = self.client().post("/quizzes", json=self.quiz_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertNotIn(data["question"]["id"],
            self.quiz_questions["previous_questions"])
        self.assertEqual(self.quiz_questions["quiz_category"],
            data["question"]["category"])
        
    def test_get_question_to_play_no_more_questions(self):
        """Test Get New Question Play No More Question"""
        res = self.client().post("/quizzes", json=self.quiz_questions2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 
            "404 Not Found: No More Question in this category")        

# Make the tests conveniently executable
if __name__ == "__main__":

    
    unittest.main()