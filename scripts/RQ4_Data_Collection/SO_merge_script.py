import json

# This script checks if the merged Stack Overflow JSON file contains any duplicate items.

# Load the JSON files
with open("../data/SO_evil_regex.json", "r") as file1, open("../data/SO_redos_regex.json", "r") as file2:
    data1 = json.load(file1)
    data2 = json.load(file2)

combined_items = data1['items'] + data2['items']

# Deduplication
deduplicated_items = []
question_ids = set()
answer_ids = set()

for item in combined_items:
    # Rule 1: Check for unique question_id
    if item['question_id'] not in question_ids:
        deduplicated_items.append(item)
        question_ids.add(item['question_id'])

        if item['item_type'] == 'answer':
            answer_ids.add(item['answer_id'])
    else:
        existing_item = next(
            (i for i in deduplicated_items if i['question_id'] == item['question_id']), None)

        # Rule 2: Differentiate between questions and answers
        if item['item_type'] != existing_item['item_type']:
            deduplicated_items.append(item)
            if item['item_type'] == 'answer':
                answer_ids.add(item['answer_id'])
        # Rule 3: Differentiate between answers with different answer_ids
        elif item['item_type'] == 'answer' and 'answer_id' in item and item['answer_id'] not in answer_ids:
            deduplicated_items.append(item)
            answer_ids.add(item['answer_id'])
        else:
            print(
                f"Found duplicate for question_id {item['question_id']} with same item_type '{item['item_type']}'.")
# Save the deduplicated list into a new JSON structure
merged_data = {
    'items': deduplicated_items
}

with open("../data/SO_merged.json", "w") as merged_file:
    json.dump(merged_data, merged_file, indent=4)

print("Merged data saved in 'SO_merged.json'")
