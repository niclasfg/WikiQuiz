from flask import Flask, render_template, request, session, redirect, url_for
from question_generator import generate_question

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'score' not in session:
        session['score'] = 0
        session['current_question'] = generate_question()

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = session['current_question']['answer']

        if user_answer == correct_answer:
            session['score'] += 1
            session['current_question'] = generate_question()
        else:
            return redirect(url_for('game_over'))

    return render_template('game.html', question=session['current_question'], score=session['score'])

@app.route('/game_over')
def game_over():
    final_score = session['score']
    session.clear()
    return render_template('game_over.html', score=final_score)

if __name__ == '__main__':
    app.run(debug=True)