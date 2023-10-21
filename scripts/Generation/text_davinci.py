import json
import openai
from tqdm import tqdm
from tenacity import (retry, stop_after_attempt,
                      wait_random_exponential, )  # for exponential backoff
import time

with open("./config.json") as f:
    config_data = json.load(f)

OPENAI_KEY = config_data['OPENAI_KEY']
openai.organization = config_data['OPENAI_ORG']
openai.api_key = OPENAI_KEY

prompt_styles = ['raw', 'refined']
temperatures = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
token_size_limits = [64, 128, 256, 512]


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def davinci_response(prompt, style, temperature, token_limit):
    try:
        # Decide on the prompt style
        prompt_content = prompt["raw_prompt"] if style == 'raw' else prompt["refined_prompt"]
        prompt_content += "\nGenerate a RegEx for this description:\n\n"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_content,
            temperature=temperature,
            max_tokens=token_limit,
            n=10
        )
        prompt['output'] = response
        time.sleep(10)
        return prompt
    except Exception as e:
        print(e)
        prompt['output'] = str(e)
        time.sleep(30)
        return prompt


with open('./RegexEval.json') as f:
    data = json.load(f)

# Loop through each combination of settings and only process the first 10 items in data
for style in prompt_styles:
    for temp in temperatures:
        for token_limit in token_size_limits:
            new_data = []
            print(
                f'Processing {style} prompts with temperature {temp} and token limit {token_limit}')
            for item in tqdm(data[:10]):
                updated_item = davinci_response(item, style, temp, token_limit)
                new_data.append(updated_item)

            # Save to a JSON file with a filename indicating the parameters
            filename = f'./Output/textdavinci/davinci_Output_{style}_{temp}_{token_limit}.json'
            with open(filename, "w") as f:
                json.dump(new_data, f, indent=4)
                print(f'Saved to {filename}')
