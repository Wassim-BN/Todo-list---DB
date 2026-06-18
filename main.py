from string import punctuation

from flask import Flask, request
from flask_cors import CORS
# from typing_extensions import Sequence

from db import (
    add_todo,
    create_todos_table,
    delete_todo,
    delete_selectedtodo,
    edit_todo,
    fetch_todos,
    get_todo,
)

app = Flask(__name__)
CORS(app)


@app.before_request
def init_db():
    create_todos_table()


@app.route("/")
def hello_world():
    return {"message": "Hello from todo-sv!"}


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = fetch_todos()
    return todos


@app.route("/todos", methods=["POST"])
def add_todo_route():
    data = request.get_json()
    text = data.get("text")
    sequence = data.get("sequence", None)
    completed = data.get("completed", False)
    
    if sequence is not None:
        return {"error": "Sequence is not supported!"}, 400

    if not text:
        return {"error": "Text is required!"}, 400

    if len(text) <= 4:
        return {"error": "Text must be at least 4 characters long!"}, 400

    if any(char in punctuation for char in text):
        return {"error": "Text must not contain punctuation!"}, 400

    add_todo(text, sequence, completed)
    return {"message": "Todo added!"}


@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo_route(id):
    delete_todo(id)
    return {"message": "Todo deleted!"}


@app.route("/todos/<int:id>", methods=["PATCH"])
def edit_todo_route(id):
    data = request.get_json()
    text = data.get("text")
    completed = data.get("completed", False)
    sequence = data.get("sequence", None)

    if not text:
        return {"error": "Text is required!"}, 400

    if len(text) <= 4:
        return {"error": "Text must be at least 4 characters long!"}, 400
 
    if any(char in punctuation for char in text):
        return {"error": "Text must not contain punctuation!"}, 400

    edit_todo(id, text, completed, sequence)
    return {"message": "Todo edited!"}


@app.route("/todos/<int:id>", methods=["GET"])
def get_todo_route(id):
    if get_todo(id):
        return {"message": "Todo finished!"}

    else:
        return {"error": "Resource not found!"}, 404


@app.route("/todos", methods=["DELETE"])
def delete_selectedTodos_route(todosIds):
    data = request.get_json()
    if not data or "todosIds" not in data:
        return {"error": "Missing todosIds list!"}, 400
    
    todos_ids = data.get("todosIds")
    
    delete_selectedtodo(todos_ids)
    
    return {"message": f"{len(todos_ids)} todos deleted successfully!"}