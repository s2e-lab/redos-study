import json

# This script checks if the merged Github JSON file contains any duplicate items.

with open('../data/pull_requests_regex_evil.json', 'r') as f1, open('../data/pull_requests_regex_redos.json', 'r') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

url_dict = {}
merged_data = []

for entry in data1 + data2:
    url = entry['url']
    if url not in url_dict:
        url_dict[url] = True
        merged_data.append(entry)
    else:
        print(f"Found duplicate for url {url}")

with open('../data/Github_merged.json', 'w') as mf:
    json.dump(merged_data, mf, indent=4)

print("Merged file saved as Github_merged.json")
