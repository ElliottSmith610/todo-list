from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "Banana"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todolist.db"
db = SQLAlchemy(app)
db.init_app(app)
Bootstrap(app)

# TODO: Multiple users?


class CreateTodoForm(FlaskForm):
    text = StringField("Todo", validators=[DataRequired()], render_kw={"placeholder": "Enter your todo here! e.g. Buy Bread"})
    submit = SubmitField("Submit")


class Todo(db.Model):
    __tablename__ = "Todo"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {column.name: str(getattr(self, column.name)) for column in self.__table__.columns}


class Done(db.Model):
    __tablename__ = "Done"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {column.name: str(getattr(self, column.name)) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    form = CreateTodoForm()
    if form.validate_on_submit():
        new_todo = Todo()
        new_todo.text = form.text.data
        db.session.add(new_todo)
        db.session.commit()
    all_todos = db.session.query(Todo).all()
    todo_list = [todo.to_dict() for todo in all_todos]
    all_done = db.session.query(Done).all()
    done_list = [done.to_dict() for done in all_done]
    return render_template('home.html', form=form, todo_list=todo_list, done_list=done_list)


@app.route("/<int:todo_id>")
def mark_done(todo_id):
    todo_to_delete = Todo.query.get(todo_id)
    done = Done()
    done.text = todo_to_delete.text
    db.session.add(done)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete/<int:done_id>")
def delete(done_id):
    done_to_delete = Done.query.get(done_id)
    db.session.delete(done_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
