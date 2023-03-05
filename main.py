import datetime
from flask import Flask, render_template, redirect, request, abort, url_for
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user
from forms.login import LoginForm
from forms.registration_form import RegistrationForm
from forms.jobs import JobsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init('db/mars_explorer.db')
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/success')
def main():
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db_session.global_init('db/mars_explorer.db')
        db_sess = db_session.create_session()
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.hashed_password = form.password.data
        user.modified_date = datetime.datetime.now()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           form=form, style=url_for('static', filename='css/style.css'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    global db_sess, form
    form = LoginForm()
    if form.validate_on_submit():
        db_session.global_init('db/mars_explorer.db')
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/success")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', style=url_for('static', filename='css/style.css'),
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/')
def list_of_jobs():
    db_session.global_init('db/mars_explorer.db')
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    print(jobs, current_user.id)
    names = {}
    for i in jobs:
        names[i] = db_sess.query(User).filter(i.team_leader == User.id).first()
    for i in jobs:
        print(i.is_finished)
    return render_template('show_jobs.html', jobs=jobs, names=names, style=url_for('static', filename='css/style.css'))


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data
        current_user.jobs.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html',
                           form=form, style=url_for('static', filename='css/style.css'))


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = JobsForm()
    if request.method == "GET":
        jobs = []
        db_sess = db_session.create_session()
        jobs.append(db_sess.query(Jobs).filter(Jobs.id == id,
                                               Jobs.team_leader == current_user.id
                                               ).first())
        if current_user.id == 1:
            jobs.append(db_sess.query(Jobs).filter(Jobs.id == id).first())
        print(jobs)
        jobs = jobs[-1]
        if jobs:
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.start_date.data = jobs.start_date
            form.end_date.data = jobs.end_date
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = []
        jobs.append(db_sess.query(Jobs).filter(Jobs.id == id,
                                               Jobs.team_leader == current_user.id
                                               ).first())
        if current_user.id == 1:
            jobs.append(db_sess.query(Jobs).filter(Jobs.id == id).first())
        jobs = jobs[-1]
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.start_date = form.start_date.data
            jobs.end_date = form.end_date.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           form=form, style=url_for('static', filename='css/style.css'))


"""
@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.author == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')
"""

if __name__ == '__main__':
    app.run()
