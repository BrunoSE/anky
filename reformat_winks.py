import json
from transformers import LlamaTokenizer
tokenizer = LlamaTokenizer.from_pretrained(PROMPT_FORMAT_ID, trust_remote_code=True)

def return_formatted_msgs(user_query, assistant_answer):
    msgs_ = [
    {"role": "user", "content" : f"{user_query}"},
    {"role": "assistant", "content" : f"{assistant_answer}"},
    ]
    return msgs_

data = []
wink_path = "./winks"

for wink_n in range(8,9):

    training_wink_data = []
    training_chapter_data = []

    with open(f"{wink_path}/proc_wink_{wink_n}.json", "r") as f:
        wink_data = json.load(f)
    
    prompt_to_user = wink_data["prompts"]["en"]
    for writing in wink_data["translated_userWritings"]:
        aux_msg = return_formatted_msgs(prompt_to_user, writing)
        training_wink_data.append(tokenizer.apply_chat_template(aux_msg, tokenize=False))

    super_prompt = wink_data["superPrompt"]
    chapter = wink_data["chapter"]

    aux_msg = return_formatted_msgs(super_prompt, chapter)
    training_chapter_data.append(tokenizer.apply_chat_template(aux_msg, tokenize=False))

    data.append({'wink_number': wink_n,
                 'training_wink_data': training_wink_data,
                 'training_chapter_data': training_chapter_data})


    with open(f"{wink_path}/training_data.json", "w") as f:
        json.dump(data, f)
