import json

# Load the merged JSON file
with open("../data/SO_merged.json", "r") as merged_file:
    data = json.load(merged_file)

items = data['items']

valid = True

for index, item in enumerate(items):
    # Rule 1: Check for unique question_id
    similar_items = [i for i in items if i['question_id']
                     == item['question_id'] and i != item]
    for similar_item in similar_items:
        # Rule 2: Check if item_type is the same
        if similar_item['item_type'] == item['item_type']:
            # Rule 3: Differentiate between answers with different answer_ids
            if item['item_type'] == 'answer' and ('answer_id' not in item or 'answer_id' not in similar_item or item['answer_id'] == similar_item['answer_id']):
                valid = False
                print(
                    f"Found duplicate for question_id {item['question_id']} with same item_type 'answer' and answer_id.")
                break

if valid:
    print("All items in the merged JSON match the criteria!")
else:
    print("There are items that do not match the criteria.")
