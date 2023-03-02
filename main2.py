from flask import Flask
from flask import render_template
from flask import url_for, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/training/<prof>')
def hello(prof):
    if 'инженер' in prof or 'строитель' in prof:
        pict = 'inz.jpg'
    else:
        pict = 'nauch.jpg'
    location = url_for('static', filename=f'img/{pict}')
    print(location)
    return render_template('base2.html', pict=pict, location=location)


@app.route('/success')
def success():
    return f'''success'''


@app.route('/distribution')
def distrib():
    people = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венкат Капут', 'Тедди Сандерс', 'Шон Бин']
    return render_template('places.html', people=people, title='Распределение')


@app.route('/table/<pol>/<int:age>')
def table(pol, age):
    pict = {
        'pink': url_for('static', filename='img/pink.png'),
        'red': url_for('static', filename='img/red.png'),
        'green': url_for('static', filename='img/green.png'),
        'purple': url_for('static', filename='img/purple.png')
    }
    people = {
        'boy': url_for('static', filename='img/boy.png'),
        'man': url_for('static', filename='img/man.png'),
        'girl': url_for('static', filename='img/girl.png'),
        'woman': url_for('static', filename='img/woman.png')
    }
    return render_template('table.html', pol=pol, age=age, urls=pict, people=people,
                           style=url_for('static', filename='css/style.css'))


if __name__ == '__main__':
    app.run()
