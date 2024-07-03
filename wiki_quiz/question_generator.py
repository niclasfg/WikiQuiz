import requests
from bs4 import BeautifulSoup
import random
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)

def get_random_wikipedia_article():
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find(id="firstHeading").text, soup.find(id="mw-content-text").find_all("p")

def generate_question():
    title, paragraphs = get_random_wikipedia_article()
    
    valid_paragraphs = [p.text for p in paragraphs if len(p.text.split()) > 20 and '[' not in p.text]
    
    if not valid_paragraphs:
        return generate_question()
    
    selected_paragraph = random.choice(valid_paragraphs)
    words = word_tokenize(selected_paragraph)
    
    # Filter words: keep only alphanumeric words with length > 3
    valid_words = [word for word in words if word.isalnum() and len(word) > 3]
    
    if len(valid_words) < 4:
        return generate_question()
    
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