from flask import Flask, render_template, request, url_for, flash, redirect
from markupsafe import escape
import imageprocessing as ip
import os
import solver

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=('GET','POST'))
@app.route('/index',methods=('GET','POST'))
def show_index():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(os.path.abspath(os.getcwd()),'static/upload_brojevi.jpg'))
        return redirect(url_for('show_equation'))
    return render_template("index.html")

@app.route('/equation',methods=('GET','POST'))
def show_equation():
    solution=''
    if request.method == 'POST':
        equation = request.form['content']
        return redirect(url_for('show_results',equation=equation))
    full_filename = 'static/upload_brojevi.jpg'#os.path.join('static','upload_brojevi.jpg')
    rect_image = ip.save_img_with_rect(full_filename)
    eq = ip.process_image(full_filename)
    return render_template("equation.html", image = rect_image, string = eq)

@app.route('/results',methods=('GET','POST'))
def show_results():
    if request.method == 'POST':
        return redirect(url_for('show_index'))
    equation = request.args.get('equation')
    solution = solver.solve(equation)
    if solution != "Invalid Expression":
        solution = str(equation) + '=' + str(solution)
    else:
        solution = "Invalid Expression"
    return render_template("results.html",string=solution)
