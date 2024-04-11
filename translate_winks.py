import json
from deep_translator import GoogleTranslator


wink_path = "./winks"
for wink_n in range(8,9):
    with open(f"{wink_path}/wink_{wink_n}.json", "r") as f:
        wink_data = json.load(f)
    wink_data["translatedWink"] = []
    print(f"Translating day {wink_n}")
    i = 0
    for write in wink_data["writingsForThisWink"]:
        i += 1
        print(f"Translating wink number {i}")
        
        translated_text = GoogleTranslator(source='auto', target='en').translate(write)

        wink_data["translatedWink"].append(translated_text)

    with open(f"{wink_path}/proc_wink_{wink_n}.json", "w") as f:
        json.dump(wink_data, f)
