from flask import Blueprint, render_template, request

lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab4_index():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div', methods = ['GET', 'POST'])
def div_form():
    if request.method == 'GET':
        return render_template('lab4/div.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Оба поля должны содержать числа!')
    
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result, show_result=True)


@lab4.route('/lab4/sum', methods=['GET', 'POST'])
def sum_form():
    if request.method == 'GET':
        return render_template('lab4/sum.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sum.html', error='Поля должны содержать числа!')
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/ym', methods=['GET', 'POST'])
def mult_form():
    if request.method == 'GET':
        return render_template('lab4/ym.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/ym.html', error='Поля должны содержать числа!')  
    result = x1 * x2
    return render_template('lab4/ym.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/raz', methods=['GET', 'POST'])
def sub_form():
    if request.method == 'GET':
        return render_template('lab4/raz.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/raz.html', error='Оба поля должны быть заполнены!')
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/raz.html', error='Оба поля должны содержать числа!')
    result = x1 - x2
    return render_template('lab4/raz.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/st', methods=['GET', 'POST'])
def pow_form():
    if request.method == 'GET':
        return render_template('lab4/st.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/st.html', error='Оба поля должны быть заполнены!')
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/st.html', error='Оба поля должны содержать числа!')
    if x1 == 0 and x2 == 0:
        return render_template('lab4/st.html', error='Оба числа не могут быть нулями!')
    result = x1 ** x2
    return render_template('lab4/st.html', x1=x1, x2=x2, result=result)