from flask import request, make_response, redirect, render_template, session

import unittest

from app import create_app

from app.firestore_service import get_users, get_todos


app = create_app()

todos = ['TODO 1', 'TODO 2', 'TODO 3']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def not_found(error):
    return render_template('500.html', error=error), 500


@app.route('/')
def index() -> dict:
    user_ip: str = request.remote_addr
    response = make_response(redirect('/hello'))
    # response.set_cookie('user_ip', user_ip)
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET'])
def hello() -> dict:
    # user_ip: str = request.cookies.get('user_ip')
    user_ip: str = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': map(lambda todo: todo.to_dict(), get_todos(username)),
        'username': username
    }

    users = get_users()

    for user in users:
        print({
            'username': user.id,
            'password': user.to_dict()['password']
        })

    return render_template('hello.html', **context)
