import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import re

def split_into_sentences(text):
    sentences = re.split('(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=\\.|\\?|\\!)\\s', text)
    return sentences

def extract_urls(query):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + query
    try:
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all("a")
        urls = [link.get('href').split("?q=")[1].split("&sa=U")[0] for link in links if "url?q=" in link.get('href') and not "webcache" in link.get('href') and "youtube" not in link.get('href') and "pdf" not in link.get('href')]
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

# # Example usage:
# text_to_check = "Your input text here."
# results = fingerprinting_algorithm(text_to_check, n=3)
# for result in results:
#     similarity, url, sentence = result
#     print(f"Sentence: {sentence}\nSimilarity: {similarity}\nURL: {url}\n")
