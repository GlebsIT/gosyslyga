from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class FormAddSkill(Form):
    id_logic = StringField('id_logic')
    id_parents = StringField('id_parents')
    response = StringField('response', validators=[DataRequired()])
    template = StringField('template')
    button = StringField('button')
    command = StringField('command')
    submit = SubmitField('добавить')


class FormDeleteSkill(Form):
    id_del = HiddenField('id_del')
    deletSub = SubmitField('delete')
