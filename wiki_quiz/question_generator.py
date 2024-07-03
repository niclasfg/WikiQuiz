import requests
from bs4 import BeautifulSoup
import random
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)

WIKIPEDIA_URLS = {
    'en': "https://en.wikipedia.org/wiki/Special:Random",
    'sv': "https://sv.wikipedia.org/wiki/Special:Slumpsida",
    'zh': "https://zh.wikipedia.org/wiki/Special:随机页面"
}

COMMON_WORDS_LIST = {
    'en': 'static/common_words_en.txt',
    'sv': 'static/common_words_sv.txt',
    'zh': 'static/common_words_zh.txt',
}

def load_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return None
    
def is_word_in_contents(contents, word):
    return word in contents

def get_random_wikipedia_article(language):
    response = requests.get(WIKIPEDIA_URLS[language])
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find(id="firstHeading").text, soup.find(id="mw-content-text").find_all("p")

def get_valid_paragraphs(paragraphs):
    return [p.text for p in paragraphs if len(p.text.split()) > 20 and '[' not in p.text]

def get_valid_words(words, language):
    common_words = load_file_contents(COMMON_WORDS_LIST[language])
    return [word for word in words if word.isalnum() and not is_word_in_contents(common_words,word.lower()) and len(word) > 1]

def generate_question(language):
    title, paragraphs = get_random_wikipedia_article(language)
    
    valid_paragraphs = get_valid_paragraphs(paragraphs)
    
    if not valid_paragraphs:
        return generate_question(language)
    
    selected_paragraph = random.choice(valid_paragraphs)
    words = word_tokenize(selected_paragraph)
    
    # Filter words: keep only alphanumeric words with length > 1
    valid_words = get_valid_words(words, language)
    
    if len(valid_words) < 4:
        return generate_question(language)
    
    correct_answer = random.choice(valid_words)
    other_words = [word for word in valid_words if word.lower() != correct_answer.lower()]
    
    
    choices = random.sample(other_words, 3) + [correct_answer]
    random.shuffle(choices)
    
    blanked_text = selected_paragraph.replace(correct_answer, "_____", 1)
    
    return {
        "statement": blanked_text,
        "choices": choices,
        "answer": correct_answer,
        "title": title
    }