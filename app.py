from flask import Flask, render_template, request, url_for, flash, redirect
from markupsafe import escape
import imageproc as ip
import os
import equation_solver as es

PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=('GET','POST'))
@app.route('/index',methods=('GET','POST'))
def show_index():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(os.path.abspath(os.getcwd()),'static/upload_brojevi.jpg'))
        return redirect(url_for('show_segmented'))
    return render_template("form.html")

@app.route('/seg',methods=('GET','POST'))
def show_segmented():
    solution=''
    if request.method == 'POST':
        equation = request.form['content']
        solution = es.solve(equation)
    full_filename = 'static/upload_brojevi.jpg'#os.path.join('static','upload_brojevi.jpg')
    rect = ip.get_rectangles(full_filename)
    ip.save_img_with_rect(full_filename,rect)
    brojevi = 'static/upload_brojevi_rect.jpg'
    crop = ip.cropped_dataset(full_filename,rect)
    eq = ip.data_to_model(crop)
    return render_template("index.html", image = brojevi, string = eq, solution = solution)

@app.route("/test")
def hello_world():
    return render_template("index.html", image = 'static/brojevi5.jpg')

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route("/upload", methods=('GET','POST'))
def hello_test():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(os.path.abspath(os.getcwd()),'testbrojevi.jpg'))
        return redirect(url_for('show_index'))
    return render_template("index.html")
