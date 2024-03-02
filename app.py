from flask import Flask, request, flash, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = 'pwab'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
from surveys import satisfaction_survey as survey

@app.route('/')
def show_survey():
    responses.clear()
    return render_template('survey.html', survey=survey)

@app.route('/questions/<int:num>')
def show_question(num):
    if len(responses) == num-1:
        try:
            return render_template('question.html', question=survey.questions[num-1], num=num-1)
        except:
            return redirect('/thanks')
    else:
        flash("Attampting to access invalid question")
        return redirect(f'/questions/{len(responses)+1}')

@app.route('/answer/<int:num>', methods=["POST"])
def add_response(num):
    responses.append(request.form['response'])
    num += 2
    return redirect(f'/questions/{num}')

@app.route('/thanks')
def thank_user():
    return render_template('thanks.html')