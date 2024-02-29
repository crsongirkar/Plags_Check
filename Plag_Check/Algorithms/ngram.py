import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from nltk import ngrams, word_tokenize
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

def generate_ngrams(text, n):
    words = word_tokenize(text.lower())
    ngrams_list = list(ngrams(words, n))
    return [' '.join(gram) for gram in ngrams_list]

def calculate_similarity(sent1, sent2, n):
    ngrams1 = generate_ngrams(sent1, n)
    ngrams2 = generate_ngrams(sent2, n)

    common_ngrams = set(ngrams1) & set(ngrams2)
    all_ngrams = set(ngrams1) | set(ngrams2)

    jaccard_sim = len(common_ngrams) / len(all_ngrams) if all_ngrams else 0.0

    return jaccard_sim

def check_one_sentence(sent, n):
    ans = []
    urls = extract_urls(sent)
    for url in urls:
        website_text = get_text_from_url(url)
        if website_text:
            jaccard_sim = calculate_similarity(sent, website_text, n)
            ans.append([jaccard_sim, url])
    return ans

def get_best_match_for_sentence(sent, n):
    ans = check_one_sentence(sent, n)
    if ans:
        max_jaccard_similarity, max_url = max(ans, key=lambda x: x[0])
        return max_jaccard_similarity, max_url
    return 0, ''

def plagiarism_detection_algorithm(text, n=3):
    all_sentences = split_into_sentences(text)
    results = []
    for sentence in all_sentences:
        jaccard_similarity, url = get_best_match_for_sentence(sentence, n)
        results.append([jaccard_similarity, url, sentence])
    return results

# Example usage:
# text_to_check = "Your input text here."
# results = plagiarism_detection_algorithm(text_to_check, n=3)
# for result in results:
#     cos_similarity, jaccard_similarity, url, sentence = result
#     print(f"Sentence: {sentence}\nCosine Similarity: {cos_similarity}\nJaccard Similarity: {jaccard_similarity}\nURL: {url}\n")
