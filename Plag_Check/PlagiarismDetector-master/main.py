from flask import Flask, render_template, redirect, send_file, url_for, request

from Plag_Check.Algorithms import cosine, string, fingerprint, ngram
from Plag_Check.Algorithms.ngram import plagiarism_detection_algorithm
from Plag_Check.Algorithms.string import boyer_moore_search
from forms import matchingform, fingerprintingform, Ngarmform, cosineform, PlagForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '827e763e55e41e32381c13afc4338d5f'

get_text = []

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
    ans = cosine.main_function(get_text[0])  # Replace with actual cosine similarity implementation
    return render_template('results.html', output=ans)

def results2():
    if request.method == 'POST':
        text_to_check = request.form['text_to_check']
        pattern_to_search = "your_pattern_here"  # Replace with the pattern you want to search

        # Call your Boyer-Moore algorithm here
        result_index = boyer_moore_search(text_to_check, pattern_to_search)

        if result_index != -1:
            result_text = f"Pattern found at index {result_index}"
        else:
            result_text = "Pattern not found in the text"

        return render_template('boyer_moore_result.html', text_to_check=text_to_check, result_text=result_text)
    else:
        return redirect(url_for('index'))


@app.route('/finger_result')
def results3():
    # Replace with actual fingerprinting implementation
    ans3 = "Replace this with the result of fingerprinting algorithm"
    return render_template('finger_result.html', output=ans3)


@app.route('/ngram_result')
def results4():
    ngram_results = plagiarism_detection_algorithm(get_text[0], n=3)  # Change 'n' as needed
    print(ngram_results)
    # return redirect('/ngram_result')  # Comment out redirect for debugging
    return render_template('ngram_result.html', output=ngram_results)


@app.route('/display_image')  # Add this route for the display_image function
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


@app.route('/About.html')
def about():
    return render_template('About.html')

@app.route('/contact us.html')
def contact():
    return render_template('contact us.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8082')
