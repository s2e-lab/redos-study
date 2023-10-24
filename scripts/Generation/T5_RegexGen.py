import json
import tqdm
from transformers import pipeline

pipe = pipeline("text2text-generation",
                model="rymaju/KB13-t5-base-finetuned-en-to-regex", device_map="auto")

prompt_styles = ['raw', 'refined']
temperatures = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
token_size_limits = [128]


def t5_response(prompt, style, temperature, token_limit):
    if temperature == 0.0:
        temperature = 1e-5
    prompt_content = prompt["raw_prompt"] if style == 'raw' else prompt["refined_prompt"]
    response = pipe(prompt_content, num_return_sequences=10, early_stopping=True, do_sample=True,
                    temperature=temperature, max_length=token_limit)
    prompt['output'] = response
    return prompt


with open('./RegexEval.json') as f:
    data = json.load(f)

for style in prompt_styles:
    for temp in temperatures:
        for token_limit in token_size_limits:
            new_data = []
            print(
                f'Processing {style} prompts with temperature {temp} and token limit {token_limit}')
            for item in tqdm.tqdm(data[:10]):
                updated_item = t5_response(item, style, temp, token_limit)
                new_data.append(updated_item)

            filename = f'./Output/t5/T5_Output_{style}_{temp}_{token_limit}.json'
            with open(filename, "w") as f:
                json.dump(new_data, f, indent=4)
                print(f'Saved to {filename}')
