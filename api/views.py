from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from huggingface_hub import login
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
import json
import torch
from glob import glob
from dotenv import load_dotenv
from .chain import Model, Chain, Memory, MultiUserMemory


load_dotenv()

documents = []
usersMemory = MultiUserMemory()


def main():
    login(token=os.environ['HuggingFace_key'], add_to_git_credential=True)
    
    category_dirs = glob("api/knowledge-base/*")
    for c_dir in category_dirs:
        loader = DirectoryLoader(path=c_dir, glob="*.txt", loader_cls=TextLoader)
        documents.extend(loader.load())

    # Chunk
    # splitter = CharacterTextSplitter(chunk_size=1800, chunk_overlap=400)
    # documents = splitter.split_documents(documents)

    cuda_available = torch.cuda.is_available()

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": 'cuda' if cuda_available else 'cpu'},
        encode_kwargs={"normalize_embeddings": False}
    )

    vecDir = 'knowledgeDB'
    if os.path.exists(vecDir): 
        Chroma(persist_directory=vecDir, embedding_function=embedding).delete_collection()
    vecStore = Chroma.from_documents(documents=documents, embedding=embedding, persist_directory=vecDir)
    
    llm_model = Model(cuda=cuda_available)
    global pipeline
    pipeline = Chain(model=llm_model, retreiver=vecStore.as_retriever())


def ragChat(request):
    text = request.POST['text']

    try:
        id = request.POST['session-id']
    except Exception as e: 
        id = False
    
    if id:
        if usersMemory.check_memory(id): 
            mem = usersMemory[id]
        else:
            mem = Memory(system_prompt='You are a chat bot for VIC Bank. You should assist the users with their queries.')
        answer = pipeline.invoke(text, mem)
        usersMemory[id] = mem
    else: 
        answer = pipeline.invoke(text, system_prompt='You are a chat bot for VIC Bank. You should assist the users with their queries.')

    return JsonResponse({'answer': answer})


main()
