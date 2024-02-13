# ReDoS Comprehension from LLM and Developer Forums
This repository contains the source code of the paper "Understanding Regular Expression Denial of Service (ReDoS): Insights from LLM-Generated Regexes and Developer Forums", accepted at the  32nd International Conference on Program Comprehension (ICPC 2024).

## Abstract
Regular expression Denial of Service (ReDoS) represents an algo-
rithmic complexity attack that exploits the processing of regular
expressions (regexes) to produce a denial-of-service attack. This
attack occurs when a regex’s evaluation time scales polynomially or
exponentially with input length, posing significant challenges for
software developers. The advent of Large Language Models (LLMs)
has revolutionized the generation of regexes from natural language
prompts, but not without its risks. Prior works showed that LLMs
can generate code with vulnerabilities and security smells. In this paper, we examined the correctness and security of regexes generated
by LLMs as well as the characteristics of LLM-generated vulner-
able regexes. Our study also examined ReDoS patterns in actual
software projects, aligning them with corresponding regex equiva-
lence classes and algorithmic complexity. Moreover, we analyzed
developer discussions on GitHub and StackOverflow, constructing
a taxonomy to investigate their experiences and perspectives on
ReDoS. In this study, we found that GPT-3.5 was the best LLM to
generate regexes that are both correct and secure. We also observed
that LLM-generated regexes mainly have polynomial ReDoS vulner-
ability patterns and it is consistent with vulnerable regexes found
in open-source projects. We also found that developers’ main discussions around insecure regexes are related to mitigation strategies
to remove vulnerable regexes.

## Project Structure
- Developers_Discussion_Data: Contains the data collected from GitHub and StackOverflow about ReDoS.
- scrips: Contains the scripts used to generate the data and the plots.
  - Generation: Contains the scripts used to generate the regexes from LLMs.
  - Evaluation: Contains the scripts used to evaluate the regexes and this results presented in the RQ1.
  - ReDoSAnalysis: Contains the scripts used to analyze the ReDoS patterns and the results presented in the RQ2.
  - RQ3_Analysis: Contains the scripts used to analyze the ReDoS in the real-world and the results presented in the RQ3.
  - RQ4_Data_Collection: Contains the scripts used to collect the data from GitHub and StackOverflow, used in RQ4.
  - Other scripts used to generate the fine-grained data and plots presented in the paper.

## Usage
### Installation

Run the following command to install the required packages:
```
conda create -n "redos_study"  python=3.9.4
conda activate redos_study
pip install -r requirements.txt
pip install torch torchvision torchaudio
pip install accelerate
```

### Generation
There are three Python files for three models: gpt35.py, Phi_RegexGen, and T5_Regexgen.py. You can run them to generate the regexes.



You will need an OpenAI API key for gpt35.py and have to create a **config.json** file as the **example.json** file. Update your API key in the **config.json** file.

*fix_gpt35.ipynb* will try to regenerate the regexes generated by GPT-3.5 if there is an error.

*gpt35_filter.ipynb* will filter additional text generated by GPT-3.5. 

*phi_filter.ipynb* will filter additional text generated by Phi model.

*ReDoSHunter_Input_Creation.ipynb* will create the input for [ReDoSHunter](https://github.com/yetingli/ReDoSHunter). Check the corresponding link about running it.

### Evaluation
**Compilation.ipynb** will compile the Regexes and tests with the corresponding tests. It will generate {Model_name}_{Prompt_type}_Output_Compiled_Result.json. Then, you can run **Pass_at_k_Evaluation.ipynb** to get the pass@k score.

**DFA_Equ_Evaluation.ipynb** will use *regex_dfa_equals.jar* to find out the DFA match and calculate the DFA-EQ@k score.


**EM_Evaluation.ipynb** will calculate the Exact match ratio.

### RQ4 Analysis
- Files with the name *[gG]ithub* or *stackoverflow|SO* are used to collect the data from GitHub and StackOverflow. 
- *SO_collect.py* and *Github_collect_regex_redos.py* are used to analyze the data collected from StackOverflow and GitHub, respectively.
- *Github_merge_script.py* and *SO_merge_script.py* are used to merge two types of data collected from GitHub and StackOverflow, respectively.
= *SO_diff_check.py* and *Github_diff_check.py* are used to check if the Stack Overflow or Github JSON file contains any duplicate items(contain `regex`, `evil` and `redos`).
