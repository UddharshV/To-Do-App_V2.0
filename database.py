import sqlite3

from flask import g

def connect_to_db():
    sql=sqlite3.connect("/Users/uddharshv/Documents/PROJECTS/To-Do List V2/todoapp.db")
    sql.row_factory=sqlite3.Row
    return sql

def get_db():
    if not hasattr(g,"todo_db"):
        g.todo_db=connect_to_db()
    return g.todo_db