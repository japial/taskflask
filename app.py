from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'An Error Occurred'

    else:
        tasks = Todo.query.order_by(Todo.created_at).all()
        return render_template('index.html', tasks=tasks)


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.completed = request.form['completed']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'An Error Occurred'
    else:
        return render_template('edit.html', task=task)


@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'An Error Occurred'



if __name__ == "__main__":
    app.run(debug=True)
