import sqlite3


def get_db_connection():
    conn = sqlite3.connect("todos.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.close()


def create_todos_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            sequence INTEGER NULL UNIQUE,
            CHECK (typeof(sequence) = 'integer' OR sequence IS NULL)
        );
    """)
    conn.commit()
    conn.close()


def fetch_todos():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def add_todo(text, completed, sequence):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO todos (text, completed, sequence) VALUES (?, ?, ?)",
            (text, completed, sequence),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception("Sequence must be a unique integer!")

    finally:
        conn.close()


def edit_todo(id, text=None, completed=None, sequence=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    if text is not None:
        fields.append("text = ?")
        values.append(text)

    if completed is not None:
        fields.append("completed = ?")
        values.append(completed)

    if sequence is not None:
        fields.append("sequence = ?")
        values.append(sequence)

    # Nothing to update
    if not fields:
        conn.close()
        return False

    values.append(id)

    sql = f"UPDATE todos SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(sql, values)

    conn.commit()
    conn.close()
    return True


def delete_todo(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def delete_selectedtodo(todosIds):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE * FROM selectedTodos")
    conn.commit()
    conn.close()


def get_todo(id, sequence):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE todos SET completed = 1 WHERE id = ? AND sequence = ?",
        (id, sequence),
    )
    conn.commit()
    conn.close()

def reorder_todos(todos_ids):
    conn = get_db_connection()
    cursor = conn.cursor()

    for index, todo_id in enumerate(todos_ids):
        cursor.execute("UPDATE todos SET sequence = ? WHERE id = ?", (index + 1, todo_id))

    conn.commit()
    conn.close()