from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import os
from transformers import LlamaTokenizer

model_path = "/teamspace/studios/this_studio/LLMs/noushermes2/nous-hermes-2-mixtral-8x7b-dpo.Q5_0.gguf"
PROMPT_FORMAT_ID = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
tokenizer = LlamaTokenizer.from_pretrained(PROMPT_FORMAT_ID, trust_remote_code=True)

############################################################################################################

wink_path = "/teamspace/studios/this_studio/anky/winks"
wink_n = 18
with open(f"{wink_path}/proc_wink_{wink_n}.json", "r") as f:
    data = json.load(f)

############################################################################################################
writings = ""
i = 0

for write in data["translated_userWritings"]:
    i += 1
    writings += f"Wink {wink_n}. - Writing number {i}\n"
    writings += write
    writings += '\n'


############################################################################################################
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

n_gpu_layers = -1  # The number of layers to put on the GPU. The rest will be on the CPU. If you don't know how many layers there are, you can use -1 to move all to GPU.
n_batch = 32768  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
n_ctx = 32768 # context window
max_tokens=512 # max tokens to generate with LLM
stopwords = ['Human:', 'User:' ,'Query:', 'Answer:', 'Assistant:', 'AI:',
             'human:', 'user:' ,'query:', 'answer:', 'assistant:', 'ai:']
last_n_tokens_size = 4 # window for repeat penalty, default 64
repeat_penalty = 1.0 # 1.1
temperature = 1.0 # 0.8
top_p = 1.0 # 0.95
top_k = 0 # 40
min_p = 0.02

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx=n_ctx,
    max_tokens=max_tokens,
    stop=stopwords,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
    last_n_tokens_size = last_n_tokens_size,
    repeat_penalty = repeat_penalty,
    temperature = temperature,
    top_p = top_p,
    top_k = top_k,
    model_kwargs={
        'min-p': min_p,
    },
)

############################################################################################################
system_prompt = f"""You are a fantastic writer, a master of crafting amazing and creative stories.
Your mission is to distill the underlying essence that brings together all of the writings that will be given as context, called WINK, which were written as streams of consciousness by people that were answering the following question:
{data['prompts']['en']}
Now you will receive instructions from the user regarding writing a new chapter, and it is your imperative mission to write the next chapter following everything that it says, in terms of structure, style, characters and the interweaving with the story.
Inspire your writing on the WINK writings, on the teachings of Ramana Maharshi, and the writing style of David Foster Wallace, and have in mind that there are no boundaries for this process of writing. We are diving into the unknown.
So just dive into the unknown, and use this books as a vehicle to catalyze awe and tell us what it means to be human, through Anky's story.
"""

def return_formatted_msgs(input_query, system_prompt, writings=''):
    msgs_ = [
    {"role": "system", "content": f"{system_prompt}"},
    {"role": "assistant", "content" : "Understood, I am indeed great at writing, storytelling and fantasy."},
    {"role": "user", "content" : f"Here are previous book chapters:\n{writings}"},
    {"role": "assistant", "content" : "Thanks, I will put these to good use."},
    {"role": "user", "content" : f"{input_query}"}
    ]
    return msgs_

def update_messages(msgs, input_query, ai_answer):
    return msgs + [{"role": "user", "content" : f"{query}"},
                    {"role": "assistant", "content" : f"{ai_answer}"}]

############################################################################################################

messages = return_formatted_msgs(data['superPrompt'], writings=writings)

prompt = tokenizer.apply_chat_template(messages, tokenize=False)
messages = prompt + '<|im_start|>assistant\nChapter'
print("")
print("This is the formatted message input:")
print("")
print(messages)
print("")
print("Starting LLM invoke....")
print("")
result = llm.invoke(messages)
print(result.content)
