from flask import Flask, request
from flask_cors import CORS

from db import add_todo, create_todos_table, delete_todo, edit_todo, fetch_todos, todo_finished

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

    if not text:
        return {"error": "Text is required!"}, 400

    add_todo(text)
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

    # if not text:
    #     return {"error": "Text is required!"}, 400

    edit_todo(id, text, completed)
    return {"message": "Todo edited!"}


@app.route("/todos/<int:id>", methods=["PUT"])
def valid_todo_route(id):
    if valid_todo(id):
        todo_finished(id)
        return {"message": "Todo finished!"}
    else:
        return {"error": "Invalid todo!"}, 400
