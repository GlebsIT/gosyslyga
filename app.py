from flask import Flask, render_template, request
from forms import FormAddSkill,FormDeleteSkill
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# from models import Logic
# from sqlalchemy.orm import mapper


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class Logic(db.Model):
    __tablename__ = 'logic_skill'
    id_logic = db.Column(db.Integer, primary_key=True)
    id_parents = db.Column(db.String(64))
    response = db.Column(db.String(256))
    template = db.Column(db.String(256))
    command = db.Column(db.String(256))
    button = db.Column(db.String(256))

    def __repr__(self):
        return '<Response {}>'.format(self.response)



@app.route('/')
def main():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)


def rekursia(logic,id_parents,iterator,rekurs_element):
    for val in logic:
        if val.id_parents == str(id_parents) and  rekurs_element.get(val.id_logic,0) == 0:
            #iterator += 1
            rekurs_element[val.id_logic] = len(rekurs_element)
            rekursia(logic,val.id_logic,len(rekurs_element),rekurs_element)

@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user_account.html')

@app.route('/analitik', methods=['GET', 'POST'])
def info():
    form = FormAddSkill()
    delform = FormDeleteSkill()
    if request.form.get('id_del') != None:
        Logic.query.filter_by(id_logic=request.form.get('id_del')).delete()
        db.session.commit()
    elif request.form.get('id_logic') != None and request.form.get('id_logic') !='':
        skill = Logic.query.filter_by(id_logic=int(request.form.get('id_logic'))).first()
        skill.id_parents = request.form.get('id_parents')
        skill.template = request.form.get('template')
        skill.response = request.form.get('response')
        skill.button = request.form.get('button')
        skill.command = request.form.get('command')
        db.session.commit()
    elif request.form.get('id_parents') != None:
        skill = Logic(id_parents = request.form.get('id_parents'), response = request.form.get('response'),
                      template = request.form.get('template'), button = request.form.get('button'), command = request.form.get('command'))
        db.session.add(skill)
        db.session.commit()
    logic = Logic.query.all()
    logic = sorted(logic, key=lambda logic: logic.id_parents)
    rekurs_element = {}
    rekursia(logic,'',0, rekurs_element)
    logic = sorted(logic,key=lambda logic: rekurs_element[logic.id_logic])
    head_id = ''
    if len(logic) > 0:
        head_id = str(logic[0].id_logic)
    return render_template('info.html', title="lk", logic=logic, form=form, delform=delform, head = head_id)

