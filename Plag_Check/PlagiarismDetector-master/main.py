from datetime import datetime
from flask import Flask, render_template, redirect, send_file, url_for, request
from Plag_Check.Algorithms import cosine, string, fingerprint, ngram
from Plag_Check.Algorithms.ngram import plagiarism_detection_algorithm
from Plag_Check.Algorithms.string import boyer_moore_search
import psycopg2
from psycopg2 import Error
from forms import matchingform, fingerprintingform, Ngarmform, cosineform, PlagForm
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key_here')

app.config['API_KEY'] = os.environ.get('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDBkODI4NTItYjc4Zi00OWRhLTgzNTYtMWYwNDYxZjYwNGU1IiwidHlwZSI6ImFwaV90b2tlbiJ9.bK2f2Vrck6bwsMta6_E5CXuP-TrSo42uexsCyER4tSc')
get_text = []

# database connection
def connect_to_postgresql():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port",
            database="your_database"
        )
        print("Connected to PostgreSQL successfully")
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None

# Call the function to connect to PostgreSQL
connection = connect_to_postgresql()

@app.route('/', methods=['POST', 'GET'])
def index():
    form = PlagForm()
    if form.validate_on_submit():
        text = form.checkText.data
        print("Text:", text)
        get_text.clear()
        get_text.append(text)
        return redirect('/results')
    return render_template('index.html', form=form)

@app.route('/results')
def results():
    now = datetime.now()
    ans = cosine.main_function(get_text[0])  # Replace with actual cosine similarity implementation
    return render_template('results.html', output=ans)

@app.route('/finger_result')
def results3():
    now = datetime.now()
    ans3 = fingerprint.fingerprinting_algorithm(get_text[1])
    return render_template('result.html', output=ans3)

@app.route('/ngram_result')
def results4():
    now = datetime.now()
    ngram_results = plagiarism_detection_algorithm(get_text[0], n=3)
    print(ngram_results)
    # return redirect('/ngram_result')
    return render_template('ngram_result.html', output=ngram_results)

@app.route('/display_image')
def display_image():
    image_path = 'Images/Img1.png'
    return send_file(image_path, mimetype='Images/MS-CIT-1')

@app.route('/boyer_moore.html')
def boyer_moore():
    form = matchingform()
    if form.validate_on_submit():
        text = form.checkText.data
        print(text)
        get_text.clear()
        get_text.append(text)
        return redirect('/boyer_moore_result')
    return render_template('boyer_moore.html', form=form)

@app.route('/fingerprinting.html')
def fingerprinting():
    form = fingerprintingform()
    if form.validate_on_submit():
        text = form.checkText.data
        print(text)
        get_text.clear()
        get_text.append(text)
        return redirect('/finger_result')
    return render_template('fingerprinting.html', form=form)

@app.route('/ngram.html')
def ngarm():
    form = Ngarmform()
    if form.validate_on_submit():
        text = form.checkText.data
        print(text)
        get_text.clear()
        get_text.append(text)
        return redirect('/ngram_result')
    return render_template('ngram.html', form=form)

@app.route('/cosine.html')
def cosines():
    form = cosineform()
    if form.validate_on_submit():
        text = form.checkText.data
        print(text)
        get_text.clear()
        get_text.append(text)
        return redirect('/results')
    return render_template('cosine.html', form=form)

@app.route('/index.html')
def Home():
    return render_template('index.html')

@app.route('/About.html')
def about():
    return render_template('About.html')

@app.route('/contact us.html')
def contact():
    return render_template('contact us.html')

@app.route('/Article Rewriter.html')
def Articel():
    return render_template('Article Rewriter.html')

@app.route('/download_report')
def download_report():
    return "Download Report functionality will be implemented here."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8086')
