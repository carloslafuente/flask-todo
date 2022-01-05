from flask import request, make_response, redirect, render_template, session

import unittest

from flask.helpers import flash, url_for

from app import create_app

from app.firestore_service import delete_todo, get_users, get_todos, put_todo, update_todo

from flask_login import login_required, current_user

from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm


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


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello() -> dict:
    # user_ip: str = request.cookies.get('user_ip')
    user_ip: str = session.get('user_ip')
    # username = session.get('username')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form,
    }

    users = get_users()

    if todo_form.validate_on_submit():
        put_todo(username, todo_form.description.data)

        flash('Tu tarea se creo con exito!')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def delete(todo_id):
    user_id = current_user.id

    delete_todo(user_id, todo_id)

    flash('Eliminado correctamente')

    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def update(todo_id, done):
    user_id = current_user.id

    update_todo(user_id, todo_id, done)

    flash('Eliminado correctamente')

    return redirect(url_for('hello'))
