import json


# parse the JSON file located at file_path
def parse_json(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)


# convert to fixture
def to_fixture(pk, source, content):
    return {
        "model": "redos_study.post",
        "pk": pk,
        "fields": {
            "source": source,
            "content": content,            
        }
    }




def process(source, parsed_data, pk=0):
    fixtures = []
    # iterate over 
    for sample in parsed_data:
        pk += 1
        content = json.dumps(sample)
        content = sample
        fixture = to_fixture(pk, source, content)
        fixtures.append(fixture)
        
        

    with open(f'/Users/joanna/Documents/Portfolio/GitHub/S2E-Lab/coding_website/fixtures/{source}_fixtures.json', 'w') as outfile:
        # save to json but formatted with tabs
        json.dump(fixtures, outfile, indent=4)


# if main
if __name__ == '__main__':
    so_data = parse_json('../data/SO_merged.json')
    process("StackOverflow", so_data["items"])

    github_data = parse_json('../data/Github_merged.json')
    process("GitHub", github_data, len(so_data["items"]) + 1)
