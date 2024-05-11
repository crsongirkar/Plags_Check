import requests
from bs4 import BeautifulSoup

from Plag_Check.Algorithms.fingerprint import split_into_sentences, generate_fingerprint, calculate_similarity

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDBkODI4NTItYjc4Zi00OWRhLTgzNTYtMWYwNDYxZjYwNGU1IiwidHlwZSI6ImFwaV90b2tlbiJ9.bK2f2Vrck6bwsMta6_E5CXuP-TrSo42uexsCyER4tSc'


def boyer_moore_search(text, pattern):
    def bad_character_heuristic(pattern):
        bad_char = {}
        pattern_length = len(pattern)

        for i in range(pattern_length - 1):
            bad_char[pattern[i]] = pattern_length - 1 - i

        return bad_char

    def match_suffix(pattern, suffix):
        pattern_length = len(pattern)
        j = pattern_length - 1

        while j >= 0 and pattern[j] == suffix[j]:
            j -= 1

        return j

    text_length = len(text)
    pattern_length = len(pattern)
    bad_char = bad_character_heuristic(pattern)

    i = 0
    occurrences = []

    while i <= text_length - pattern_length:
        j = pattern_length - 1

        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1

        if j < 0:
            # Pattern found, add occurrence index to the list
            occurrences.append(i)

            # Move the pattern based on bad character heuristic
            bad_char_shift = bad_char.get(text[i + j], pattern_length)
            suffix_shift = pattern_length - 1 - match_suffix(pattern, pattern[j:])

            i += max(bad_char_shift, suffix_shift)
        else:
            # Move the pattern to align the last character of the pattern with the mismatched character in the text
            i += max(1, j - bad_char.get(text[i + j], -1))

    return occurrences

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

# Example usage:
# text_to_search = "Your input text here."  # Replace with your actual text
# pattern_to_search = "Pattern to search"  # Replace with your actual pattern
# occurrences = boyer_moore_search(text_to_search, pattern_to_search)
# print("Occurrences:", occurrences)
#
# query_to_search = "Your search query"  # Replace with your actual query
# urls_found = extract_urls(query_to_search)
# print("Extracted URLs:", urls_found)


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

