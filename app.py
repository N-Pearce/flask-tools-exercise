from flask import Flask, request, session, flash, render_template, redirect
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

@app.route('/new-survey', methods=['POST'])
def empty_responses():
    session['responses'] = []
    return redirect('/questions/1')

@app.route('/questions/<int:num>')
def show_question(num):
    # import pdb
    # pdb.set_trace()
    print("*******************")
    print(session['responses'])
    print("*******************")
    if len(session['responses']) == num-1:
        try:
            return render_template('question.html', question=survey.questions[num-1], num=num-1)
        except:
            return redirect('/thanks')
    else:
        flash("Attampting to access invalid question")
        return redirect(f'/questions/{len(responses)+1}')

@app.route('/answer/<int:num>', methods=["POST"])
def add_response(num):
    responses = session['responses']
    responses.append(request.form['response'])
    session['responses'] = responses
    num += 2
    return redirect(f'/questions/{num}')

@app.route('/thanks')
def thank_user():
    return render_template('thanks.html')