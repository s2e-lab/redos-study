import json
import tqdm
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Setting the default device to CUDA
torch.set_default_device('cuda')

# Loading the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-1_5", trust_remote_code=True, torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/phi-1_5", trust_remote_code=True, torch_dtype="auto")

# Define the different configurations
prompt_styles = ['raw', 'refined']
temperatures = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
token_size_limits = [64, 128, 256, 512]


def phi_response(prompt, style, temperature, token_limit, tokenizer, model):
    # Decide on the prompt style
    prompt_content = prompt["raw_prompt"] if style == 'raw' else prompt["refined_prompt"]
    prompt_content += "Generate a RegEx for this description. \nAnswer:"
    inputs = tokenizer(prompt_content, return_tensors="pt",
                       max_length=token_limit, truncation=True)
    x = inputs['input_ids']
    x = x.expand(10, -1)
    generated_tokens = model.generate(
        x,
        temperature=temperature,
        max_length=token_limit,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
    )
    prompt["phi_output"] = []
    for i in range(10):
        prompt["phi_output"].append({})
        output = generated_tokens[i].cpu().squeeze()
        prompt["phi_output"][i]["text"] = tokenizer.decode(
            output, skip_special_tokens=True).split(prompt_content)[-1]

    return prompt


with open('.RegexEval.json') as f:
    data = json.load(f)

# Loop through each combination of settings and only process the first 10 items in data
for style in prompt_styles:
    for temp in temperatures:
        for token_limit in token_size_limits:
            new_data = []
            print(
                f'Processing {style} prompts with temperature {temp} and token limit {token_limit}')
            for item in tqdm.tqdm(data[:10]):
                updated_item = phi_response(
                    item, style, temp, token_limit, tokenizer, model)
                new_data.append(updated_item)

            # Save to a JSON file with a filename indicating the parameters
            filename = f'./Output/phi15/Phi_Output_{style}_{temp}_{token_limit}.json'
            with open(filename, "w") as f:
                json.dump(new_data, f, indent=4)
                print(f'Saved to {filename}')
