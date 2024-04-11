from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

wink_path = "./winks"
wink_n = 8
with open(f"{wink_path}/proc_wink_{wink_n}.json", "r") as f:
    wink_data = json.load(f)

writings = ""
i = 0

for write in wink_data["translatedWink"]:
    i += 1
    writings += f"Day {wink_n} - Writing piece number {i}\n"
    writings += write
    writings += '\n'

model_path = "../LLMs/noushermes2/nous-hermes-2-mixtral-8x7b-dpo.Q4_K_M.gguf"
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

n_gpu_layers = 20  # The number of layers to put on the GPU. The rest will be on the CPU. If you don't know how many layers there are, you can use -1 to move all to GPU.
n_batch = 32768  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
n_ctx = 32768 # context window
max_tokens= 1024 # max tokens to generate with LLM
stopwords = ['Query:', 'Answer:', 'Assistant:', 'Human:', 'human:', 'assisstant:', 'answer:', 'query:']
last_n_tokens_size = 512 # window for repeat penalty, default 64
repeat_penalty = 1.1 # 1.1
temperature = 0.2 # 0.8
top_p = 0.95 # 0.95
top_k = 40 # 40

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx=n_ctx,
    max_tokens=max_tokens,
    stop=stopwords,
    callback_manager=callback_manager,
    last_n_tokens_size = last_n_tokens_size,
    repeat_penalty = repeat_penalty,
    temperature = temperature,
    top_p = top_p,
    top_k = top_k,
    verbose=True,  # Verbose is required to pass to the callback manager
    streaming=True
)


output_parser = StrOutputParser() # stringify the answer
prompt = ChatPromptTemplate.from_messages([
     ("system", """You are a world famous fantasy writer with decades of experience and a history of writing amazing book chapters. You are part of a organized collective writing experiment. Use the following writings as inspiration for your story, try to absorb the sentiments, emotional thoughts, meditations.
     
     {writings}

     You are a world famous fantasy writer with decades of experience and a history of writing amazing book chapters. You are part of a organized collective writing experiment. Use the previous writings as inspiration for your story, try to absorb the sentiments, emotional thoughts, meditations."""),
     ("user", "{input}"),
     ("assistant", "Chapter 1. Birth\n"),
 ])
chain = prompt | llm | output_parser
answer = chain.invoke({
        "writings": writings,
        "input": "Write the first chapter of a book. This first chapter talks about the fantasy world of the ankyverse, where gods and mortals beings co-exist. Feel free to adopt a writing style that tells important events through the lens of characters."
        })
