from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('Id начальника')
    work_size = IntegerField('Количество работы в часах')
    collaborators = TextAreaField('Id работников, через запятую')
    start_date = DateField('Дата начала работ')
    end_date = DateField('Дата окончания работ')
    is_finished = BooleanField("Работа закончена")
    submit = SubmitField('Применить')