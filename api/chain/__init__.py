import os
import time
from typing import Optional
from glob import glob
import torch
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)





class Model:
    def __init__(
        self, model: str = "meta-llama/Llama-3.2-3B-Instruct", cuda: bool = False
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.cuda = cuda
        if self.cuda:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model, device_map="auto", quantization_config=bnb_config
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(model)

    def generate(self, prompt):
        encoded = self.tokenizer.apply_chat_template(prompt, return_tensors="pt")
        prompt_len = encoded.shape[1]
        if self.cuda:
            encoded = encoded.to("cuda")
            res = self.model.generate(encoded, max_new_tokens=5000)
        else:
            res = self.model.generate(encoded, max_new_tokens=5000)
        answer = self.tokenizer.batch_decode(res[:, prompt_len:], skip_special_tokens=True)[0]
        return answer.replace('assistant\n\n', '')



class Memory:
    def __init__(self, system_prompt: str = None, max_context: int = None):
        self.system = {"role": "system", "content": system_prompt}
        self.user = []
        self.assistant = []
        self.max_context = max_context

    def apply_chat_template(self, user_prompt: str):
        prompt = []
        for user, assitant in zip(self.user, self.assistant):
            prompt.append({"role": "user", "content": user})
            prompt.append({"role": "assistant", "content": assitant})

        if self.max_context:
            if len(prompt) > (self.max_context * 2):
                prompt = prompt[(-1 * (self.max_context * 2)) :]

        prompt.insert(0, self.system)
        prompt.append({"role": "user", "content": user_prompt})
        return prompt

    def add_entry(self, user: str, assistant: str):
        self.user.append(user)
        self.assistant.append(assistant)



class Chain:
    def __init__(self, model: Model = None, retreiver=None):
        self.model = model
        self.retreiver = retreiver

    def get_context(self, user_prompt):
        documents = self.retreiver.get_relevant_documents(user_prompt)
        context = "Use the following pieces of context to answer the user's query. The following context is provided RAG system and not by the user. The context is not shown to the user so dont tell the user that context is provided. If you don't know the answer, just say that you don't know and tell to contact the bank support, don't try to make up an answer.\n"
        context += "\nContext:\n"
        i = 1
        for doc in documents:
            context += f"Content {i}:\n"
            context += doc.page_content + "\n\n"
            i += 1
        return context

    def invoke(self, user_prompt: str, memory: Optional[Memory] = None, system_prompt: str = None):
        context = self.get_context(user_prompt)
        prompt = context
        prompt += f"User Query:\n  {user_prompt.strip()}"

        if isinstance(memory, Memory):
            chat_prompt = memory.apply_chat_template(prompt)
        else: 
            chat_prompt = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        result = self.model.generate(chat_prompt)

        if isinstance(memory, Memory):
            memory.add_entry(user=prompt, assistant=result)
        return result



class MultiUserMemory:
    def __init__(self):
        self.buffer = {}
        self.limit = 600  # In Seconds
    
    def check_limit(self):
        current_time = time.time()
        for id in self.buffer.keys():
            diff = current_time - self.buffer[id]['last_updated']
            if diff > self.limit:
                del self.buffer[id]

    def check(self, id: str):
        if id in self.buffer.keys():
            return True 
        else: 
            return False

    def __getitem__(self, id: str):
        return self.buffer[id]['object']
    
    def __setitem__(self, id: str, mem: Memory):
        self.buffer[id] = {
            'object': mem,
            'last_updated': time.time()
        }
        self.check_limit()
