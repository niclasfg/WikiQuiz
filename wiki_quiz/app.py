from flask import Flask, render_template, request, session, redirect, url_for
from question_generator import generate_question

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

LANGUAGES = {
    'en': 'English',
    'sv': 'Swedish',
    'zh': 'Chinese'
}

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/set_language', methods=['POST'])
def set_language():
    language = request.form.get('language')
    if language in LANGUAGES:
        session['language'] = language
        return redirect(url_for('game'))
    return redirect(url_for('index'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'language' not in session:
        return redirect(url_for('index'))

    if 'score' not in session:
        session['score'] = 0
        session['current_question'] = generate_question(session['language'])

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = session['current_question']['answer']

        if user_answer == correct_answer:
            session['score'] += 1
            session['current_question'] = generate_question(session['language'])
        else:
            return redirect(url_for('game_over'))

    return render_template('game.html', question=session['current_question'], score=session['score'])

@app.route('/game_over')
def game_over():
    final_score = session['score']
    language = session.get('language', 'en')
    session.clear()
    return render_template('game_over.html', score=final_score, language=LANGUAGES[language])

if __name__ == '__main__':
    app.run(debug=True)