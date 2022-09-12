"""
Backend
"""
import os
import random
import numpy as np
from sqlalchemy import exc
from sqlalchemy.sql.expression import func
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(req, questions):
    """ Paginate questions """
    page = req.args.get('page', 1, type=int)
    start = (page - 1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in questions]
    displayed_questions = formatted_questions[start:end]

    return displayed_questions


def create_app():
    """ create and configure the app """
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # """
    # @TODO: Set up CORS. Allow '*' for origins.
    # Delete the sample route after completing the TODOs
    # """
    # """
    # @TODO: Use the after_request decorator to set Access-Control-Allow
    # """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # """
    # @TODO:
    # Create an endpoint to handle GET requests
    # for all available categories.
    # """
    @app.route('/categories', methods=['GET'])
    def get_categories():

        categories = Category.query.order_by(Category.id).all()
        # displayed_books = paginate_books(request, categories)

        if len(categories) == 0:
            abort(404)

        return jsonify({
            # 'success':True,
            'categories': [category.format() for category in categories],
            # 'total_categories': len(categories)
        })

    # """
    # @TODO:
    # Create an endpoint to handle GET requests
    # for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category,
    # categories.

    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination
    # at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.
    # """
    @app.route('/questions', methods=['GET'])
    def get_questions():

        questions_category = request.args.get('category', 'All', type=str)

        if questions_category == 'All':
            questions = Question.query.order_by(Question.id).all()
        else:
            current_category = Category.query.filter(
                Category.type == questions_category).one_or_none()
            if current_category is None:
                abort(
                    404,
                    'No questions found in category '+questions_category
                )
            else:
                questions = Question.query.filter(
                    Question.category == current_category.id).all()
            
        displayed_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()

        if len(displayed_questions) == 0:
            abort(404, 'No questions on this page')

        return jsonify({
            'success': True,
            'questions':  displayed_questions,
            'total_questions': len(questions),
            'categories': [category.format() for category in categories],
            'current_category': questions_category
        })

    # """
    # @TODO:
    # Create an endpoint to DELETE question using a question ID.

    # TEST: When you click the trash icon next to a question,
    # the question will be removed.
    # This removal will persist in the database
    # and when you refresh the page.
    # """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(422, 'unprocessable')
            else:
                question.delete()
                questions = Question.query.order_by(Question.id).all()
                displayed_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'deleted': question_id,
                "questions": displayed_questions,
                "total_questions": len(questions),

            })
        except exc.SQLAlchemyError:
            abort(500)

    # """
    # @TODO:
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.

    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will
    # appear at the end of the last page
    # of the questions list in the "List" tab.
    # """
    @app.route('/questions', methods=['POST'])
    def add_question():

        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        if question and answer and category and difficulty:
            question = Question(question=question, answer=answer,
                                category=category, difficulty=difficulty)

            question.insert()

            questions = Question.query.order_by(Question.id).all()
            # formatted_books = [book.format() for book in books]
            displayed_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': displayed_questions,
                'total_questions': len(questions)
            })

        abort(422)

    # """
    # @TODO:
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # """
    @app.route('/search_questions', methods=['POST'])
    def search_question():

        body = request.get_json()
        search = body.get('search', None)
        if search:            
            #raise Exception(search)
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search))).all()
                #Question.question.like(search)).all()
                # Question.question.ilike(f"{search}")).order_by(
                # Question.id).all()            
            displayed_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': displayed_questions,
                'total_questions': len(displayed_questions)
            })
        abort(422)

    @app.route('/fetch_category', methods=['POST'])
    def fetch_category():

        body = request.get_json()
        category = body.get('category', None)
        if category:
            cat = Category.query.get(category)
            questions = Question.query.order_by(
                Question.id).filter_by(category=category).all()
            
            displayed_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions':  displayed_questions,
                'total_questions': len(questions),
                'current_category': cat.type  
            })
        abort(422)

    # """
    # @TODO:
    # Create a GET endpoint to get questions based on category.

    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    # """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        category_id = 1 if category_id is None else category_id
        current_category = Category.query.get(category_id)
        questions = Question.query.order_by(
            Question.id).filter_by(category=category_id).all()

        displayed_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()

        if len(questions) == 0:
            abort(404, 'No questions in this category')

        return jsonify({
            'success': True,
            'questions':  displayed_questions,
            'total_questions': len(questions),
            'categories': [category.format() for category in categories],
            'current_category': current_category.format()
        })

    # """
    # @TODO:
    # Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.

    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    # """
    @app.route('/quizzes', methods=['POST'])
    def play():

        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        next_question = Question.query.order_by(Question.id).filter_by(
            category=quiz_category).filter(
            Question.id.not_in(previous_questions)).order_by(
                func.random()).first()

        if next_question:
            return jsonify({
                'success': True,
                'question': next_question.format(),
            })
        
        abort(404, 'No More Question in this category')

    # """
    # @TODO:
    # Create error handlers for all expected errors
    # including 404 and 422.
    # """
    @app.errorhandler(404)
    def not_found(error):
        str(error)
        return (
            jsonify({"success": False, "error": 404,
                    "message": str(error)}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": str(error)}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400,
                    "message": str(error)}),
            400,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500,
                    "message": 'Internal Server Error'}),
            500,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": str(error)}),
            405,
        )
    
    return app