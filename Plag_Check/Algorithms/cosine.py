import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def tokenize_sentence(text):
    sentences = re.split('(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=\\.|\\?|\\!)\\s', text)

    return sentences
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDBkODI4NTItYjc4Zi00OWRhLTgzNTYtMWYwNDYxZjYwNGU1IiwidHlwZSI6ImFwaV90b2tlbiJ9.bK2f2Vrck6bwsMta6_E5CXuP-TrSo42uexsCyER4tSc'


def get_urls(query):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + query
    try:
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all("a")
        urls = []
        for link in links:
            href = link.get('href')
            if "url?q=" in href and not "webcache" in href and "youtube" not in href and "pdf" not in href:
                url = href.split("?q=")[1].split("&sa=U")[0]
                urls.append(url)
        return urls
    except Exception as e:
        print("Content Not Found Web", e)
        return []


def get_text_from_url(url, limit=500):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')

        text = ' '.join([para.text for para in paragraphs])

        truncated_text = text[:limit]

        return truncated_text
    except Exception as e:
        print("Error fetching website content:", e)
        return ''

def get_cosine_similarity(sent1, sent2):
    vectorizer = CountVectorizer().fit_transform([sent1, sent2])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1]

def check_one_sent(sent):
    ans = []
    urls = get_urls(sent)
    for url in urls:
        website_text = get_text_from_url(url)
        if website_text:
            similarity = get_cosine_similarity(sent, website_text)
            ans.append([similarity, url])
    return ans

def get_ans_for_one_sent(sent):
    ans = check_one_sent(sent)
    if ans:
        max_similarity, max_url = max(ans, key=lambda x: x[0])
        return max_similarity, max_url
    return 0, ''

def main_function(txt):
    all_sentences = tokenize_sentence(txt)
    ans = []
    for x in all_sentences:
        similarity, url = get_ans_for_one_sent(x)
        ans.append([similarity, url, x])
    return ans
