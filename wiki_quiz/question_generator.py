import requests
from bs4 import BeautifulSoup
import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def get_random_wikipedia_article():
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find(id="firstHeading").text, soup.find(id="mw-content-text").find_all("p")

def generate_question():
    title, paragraphs = get_random_wikipedia_article()
    
    # Filter out short paragraphs and those with citations
    valid_paragraphs = [p.text for p in paragraphs if len(p.text.split()) > 20 and '[' not in p.text]
    
    if not valid_paragraphs:
        return generate_question()
    
    selected_paragraph = random.choice(valid_paragraphs)
    sentences = sent_tokenize(selected_paragraph)
    
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        
        # Look for nouns or numbers to blank out
        for i, (word, tag) in enumerate(tagged_words):
            if tag.startswith('NN') or tag == 'CD':
                blanked_sentence = " ".join(words[:i] + ["_____"] + words[i+1:])
                return {
                    "statement": blanked_sentence,
                    "answer": word,
                    "title": title
                }
    
    # If no suitable sentence found, try again
    return generate_question()