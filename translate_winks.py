import json
from deep_translator import GoogleTranslator


wink_path = "./winks"
for wink_n in range(1,9):
    with open(f"{wink_path}/wink_{wink_n}.json", "r") as f:
        wink_data = json.load(f)

    print(f"Translating day {wink_n}")

    wink_data["translated_userWritings"] = []
    i = 0

    # wink_data["userWritings"] = wink_data["userWritings"].split('>\n\n<') # use if writings are not list

    for write in wink_data["userWritings"]:
        i += 1
        print(f"Translating writing number {i}")
        translated_text = GoogleTranslator(source='auto', target='en').translate(write)
        wink_data["translated_userWritings"].append(translated_text)

    wink_data["translated_userFeedbackForChapter"] = []
    i = 0

    #for write in wink_data["userFeedbackForChapter"]:
    #    i += 1
    #    print(f"Translating feedback number {i}")
    #    translated_text = GoogleTranslator(source='auto', target='en').translate(write)
    #    wink_data["translated_userFeedbackForChapter"].append(translated_text)

    with open(f"{wink_path}/proc_wink_{wink_n}.json", "w") as f:
        json.dump(wink_data, f)
