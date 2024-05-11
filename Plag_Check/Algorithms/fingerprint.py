import requests
from sklearn.feature_extraction.text import CountVectorizer
import re

from Plag_Check.Algorithms.ngram import extract_urls

#API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDBkODI4NTItYjc4Zi00OWRhLTgzNTYtMWYwNDYxZjYwNGU1IiwidHlwZSI6ImFwaV90b2tlbiJ9.bK2f2Vrck6bwsMta6_E5CXuP-TrSo42uexsCyER4tSc'

def split_into_sentences(text):
    sentences = re.split('(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=\\.|\\?|\\!)\\s', text)
    return sentences

def get_text_from_url(url, limit=500):
    try:
        headers = {'Authorization': f'Bearer {API_KEY}'}
        response = requests.get(url, headers=headers)
        text = response.text[:limit]  # Limit the text to a maximum of 500 characters
        return text
    except Exception as e:
        print("Error fetching website content:", e)
        return ''

def generate_fingerprint(text, n):
    vectorizer = CountVectorizer(ngram_range=(n, n)).fit_transform([text])
    fingerprint = vectorizer.toarray().flatten()
    return fingerprint

def calculate_similarity(fingerprint1, fingerprint2):
    dot_product = sum(fingerprint1[i] * fingerprint2[i] for i in range(len(fingerprint1)))
    magnitude1 = sum(fingerprint1[i] ** 2 for i in range(len(fingerprint1))) ** 0.5
    magnitude2 = sum(fingerprint2[i] ** 2 for i in range(len(fingerprint2))) ** 0.5

    cosine_sim = dot_product / (magnitude1 * magnitude2) if magnitude1 * magnitude2 != 0 else 0.0
    return cosine_sim

def check_one_sentence(sent, n):
    ans = []
    urls = extract_urls(sent)
    for url in urls:
        website_text = get_text_from_url(url)
        if website_text:
            fingerprint1 = generate_fingerprint(sent, n)
            fingerprint2 = generate_fingerprint(website_text, n)
            similarity = calculate_similarity(fingerprint1, fingerprint2)
            ans.append([similarity, url])
    return ans

def get_best_match_for_sentence(sent, n):
    ans = check_one_sentence(sent, n)
    if ans:
        max_similarity, max_url = max(ans, key=lambda x: x[0])
        return max_similarity, max_url
    return 0, ''

def fingerprinting_algorithm(text, n=3):
    all_sentences = split_into_sentences(text)
    results = []
    for sentence in all_sentences:
        similarity, url = get_best_match_for_sentence(sentence, n)
        results.append([similarity, url, sentence])
    return results

