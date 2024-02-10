import json

# This script checks if the merged Github JSON file contains any duplicate items.

def test_unique_urls(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    url_set = set()

    for entry in data:
        url = entry['url']
        if url in url_set:
            print(f"Duplicate URL found: {url}")
            return
        url_set.add(url)

    print("All URLs are unique!")


filename = '../data/Github_merged.json'
test_unique_urls(filename)
