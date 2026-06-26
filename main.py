from string import punctuation

from flask import Flask, request
from flask_cors import CORS

# from typing_extensions import Sequence
from db import (
    add_todo,
    create_todos_table,
    delete_selectedtodo,
    delete_todo,
    edit_todo,
    fetch_todos,
    get_todo,
    reorder_todos
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
    completed = data.get("completed", False)
    sequence = data.get("sequence", 0)

    if sequence < 0:
        return {"error": "Sequence must be a positive integer!"}, 400

    if not isinstance(sequence, int):
        return {"error": "Sequence is not supported!"}, 400

    if not text:
        return {"error": "Text is required!"}, 400

    if len(text) <= 4:
        return {"error": "Text must be at least 4 characters long!"}, 400

    if any(char in punctuation for char in text):
        return {"error": "Text must not contain punctuation!"}, 400

    try:
        add_todo(text, completed, sequence)
    
    except Exception as e:
        return {"error": str(e)}, 500

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
def get_todo_route(id, sequence):
    if get_todo(id, sequence):
        return {"message": "Todo finished!"}

    else:
        return {"error": "Resource not found!"}, 404


@app.route("/todos", methods=["DELETE"])
def delete_selectedTodos_route():
    data = request.get_json()
    if not data or "todosIds" not in data:
        return {"error": "Missing todosIds list!"}, 400

    todos_ids = data.get("todosIds")

    delete_selectedtodo(todos_ids)

    return {"message": f"{len(todos_ids)} todos deleted successfully!"}

@app.route("/todos/reorder", methods=["PATCH"])
def reorder_todos_route():
    data = request.get_json()
    if not data or "todosIds" not in data:
        return {"error": "Missing todosIds list!"}, 400

    todos_ids = data.get("todosIds")
    if not todos_ids or not isinstance(todos_ids, list):
        return {"error": "todosIds must be a list!"}, 400

    reorder_todos(todos_ids)
    return {"message": "Todos reordered!"}
