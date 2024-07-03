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

def get_random_wikipedia_article(language):
    response = requests.get(WIKIPEDIA_URLS[language])
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find(id="firstHeading").text, soup.find(id="mw-content-text").find_all("p")

def generate_question(language):
    title, paragraphs = get_random_wikipedia_article(language)
    
    valid_paragraphs = [p.text for p in paragraphs if len(p.text.split()) > 20 and '[' not in p.text]
    
    if not valid_paragraphs:
        return generate_question(language)
    
    selected_paragraph = random.choice(valid_paragraphs)
    words = word_tokenize(selected_paragraph)
    
    # Filter words: keep only alphanumeric words with length > 1
    valid_words = [word for word in words if word.isalnum() and len(word) > 1]
    
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