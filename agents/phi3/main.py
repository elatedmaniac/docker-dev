from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import Ollama
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os

app = FastAPI()

class Query(BaseModel):
    query: str

# Initialize Ollama model
llm = Ollama(base_url=os.getenv("OLLAMA_BASE_URL", "http://phi3:11434"), model="phi3")

# Initialize vector store (this is a simple example, you might want to persist this)
loader = TextLoader("data/")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings()
db = Chroma.from_documents(texts, embeddings)

# Create a retrieval tool
retriever = db.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

tools = [
    Tool(
        name="Local Knowledge Base",
        func=qa.run,
        description="Useful for when you need to answer questions about specific documents or information in the knowledge base."
    )
]

# Initialize agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

@app.post("/query")
async def query(query: Query):
    response = agent.run(query.query)
    return {"response": response}

@app.post("/rag")
async def rag(query: Query):
    response = qa.run(query.query)
    return {"response": response}