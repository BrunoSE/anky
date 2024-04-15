import json
training_wink_data = []
training_chapter_data = []

wink_path = "./winks"
for wink_n in range(8,9):
    with open(f"{wink_path}/proc_wink_{wink_n}.json", "r") as f:
        wink_data = json.load(f)
    
    prompt_to_user = wink_data["prompts"]["en"]
    aux = ''
    for writing in wink_data["translated_userWritings"]:
        aux = prompt_to_user + 
        training_wink_data.append()
        aux = ''