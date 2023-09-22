import requests
import json

def search_questions(query):
    url = "https://api.stackexchange.com/2.2/search/excerpts"
    params = {
        "order": "desc",
        "sort": "activity",
        "pagesize": 100,
        # q - a free form text parameter, will match all question properties based on an undocumented algorithm
        # but it is how SO actually use for searching
        "q": query,
        "site": "stackoverflow",
    }
    all_items = []
    page = 1
    
    while True:
        params['page'] = page  # Set page parameter to the current page
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        all_items.extend(data.get('items', []))
        
        # Break out of the loop if there are no more items to fetch
        if not data.get('has_more', False):
            break
            
        page += 1  # Increment the page number for the next iteration
        
    return all_items


def append_to_json(data, filename):
    try:
        # Read existing data from the file
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_items = existing_data.get('items', [])
    except (FileNotFoundError, json.JSONDecodeError):
        existing_items = []
        
    # Append new items to the existing ones
    existing_items.extend(data)
    
    # Save the updated data back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({'items': existing_items}, f, ensure_ascii=False, indent=4)

query = "redos AND regex"
items = search_questions(query)
append_to_json(items, 'SO_redos_regex.json')
print("# of questions or answers in SO that contains redos and regex =", len(items))

query2 = "evil AND regex"
items2 = search_questions(query2)
append_to_json(items2, 'SO_evil_regex.json')
print("# of questions or answers in SO that contains evil and regex =", len(items2))