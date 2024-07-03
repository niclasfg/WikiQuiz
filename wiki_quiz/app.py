from flask import Flask, render_template, request, redirect, url_for, session
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Language mapping
language_map = {
    'en': 'en.wikipedia.org',
    'sv': 'sv.wikipedia.org',
    'zh': 'zh.wikipedia.org'
}

# Function to get a random Wikipedia statement
def get_random_statement(language):
    url = f'https://{language_map[language]}/wiki/Special:Random'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    
    for paragraph in paragraphs:
        if paragraph.text.strip():
            return paragraph.text.strip(), url
    return None, None

# Function to create a quiz question
def create_quiz_question(statement):
    words = statement.split()
    random_index = random.randint(0, len(words) - 1)
    correct_word = words[random_index]
    words[random_index] = '_____'
    choices = [correct_word]
    
    while len(choices) < 4:
        fake_word = random.choice(words)
        if fake_word not in choices:
            choices.append(fake_word)
    
    random.shuffle(choices)
    return ' '.join(words), correct_word, choices

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    session['language'] = request.form['language']
    session['streak'] = 0
    return redirect(url_for('game'))

@app.route('/game')
def game():
    language = session.get('language', 'en')
    statement, url = get_random_statement(language)
    if not statement:
        return redirect(url_for('game_over'))
    
    question, correct_word, choices = create_quiz_question(statement)
    session['correct_word'] = correct_word
    session['question'] = question
    session['choices'] = choices
    session['url'] = url
    
    return render_template('game.html', question=question, choices=choices, url=url)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_choice = request.form['choice']
    correct_word = session.get('correct_word')
    
    if user_choice == correct_word:
        session['streak'] += 1
        return redirect(url_for('game'))
    else:
        return redirect(url_for('game_over'))

@app.route('/game_over')
def game_over():
    streak = session.get('streak', 0)
    return render_template('game_over.html', streak=streak)

if __name__ == '__main__':
    app.run(debug=True)