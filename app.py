from flask import Flask,render_template, request, redirect, url_for
from database import get_db, connect_to_db

app=Flask(__name__,template_folder="templates")

@app.route('/', methods=["POST", "GET"])
def index():
    db=get_db()
    task_cursor=db.execute("select * from todolist")
    all_tasks=task_cursor.fetchall()

    return render_template("index.html", all_tasks=all_tasks)

@app.route('/insert_task', methods=["POST"])
def insert_task():
    if request.method == "POST":
        task_entered=request.form['task_name']
        db=get_db()
        db.execute("INSERT INTO todolist(task,status) VALUES (?,?)", [task_entered,False])
        db.commit()
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route('/delete_task/<int:id>', methods=["POST"])
def delete_task(id):
    if request.method == "POST":
        db=get_db()
        db.execute("DELETE FROM todolist WHERE id = ?", [id])
        db.commit()
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route('/edit_task/<int:id>', methods=["POST","GET"])
def edit_task(id):
    if request.method == "POST":
        new_task_name=request.form['task_name']
        db=get_db()
        db.execute("UPDATE todolist SET task = ? WHERE id = ?", [new_task_name,id])
        db.commit()
        return redirect(url_for("index"))
    else:
        db=get_db()
        task_cursor=db.execute("SELECT * FROM todolist WHERE id = ?", [id])
        task_to_edit=task_cursor.fetchone()
        return render_template("edit.html",task_to_edit=task_to_edit)
    
@app.route('/toggle_status/<int:id>',methods=["POST"])
def toggle_status(id):
    db=get_db()
    current_status=db.execute("SELECT status FROM todolist WHERE id = ?", [id]).fetchone()['status']
    new_status= not current_status
    db.execute("UPDATE todolist SET status = ? WHERE id = ?", [new_status,id])
    db.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)