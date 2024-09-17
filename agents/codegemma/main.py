from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import Ollama
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader  # Use the correct TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread, Lock

app = FastAPI()

class Query(BaseModel):
    query: str

# Initialize Ollama model
llm = Ollama(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://codegemma:11434"),
    model="codegemma"
)

# Initialize vector store components
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
embeddings = HuggingFaceEmbeddings()
db_lock = Lock()  # Lock to manage concurrent access to the vector store

# Initialize the vector store
def initialize_vector_store():
    if os.path.exists("vectorstore"):
        # Load existing vector store
        db = Chroma(persist_directory="vectorstore", embedding_function=embeddings)
    else:
        # Create new vector store
        db = Chroma(persist_directory="vectorstore", embedding_function=embeddings)
        if os.path.exists("data"):
            documents = []
            for filename in os.listdir("data"):
                filepath = os.path.join("data", filename)
                if os.path.isfile(filepath):
                    loader = TextLoader(filepath)
                    documents.extend(loader.load())
            texts = text_splitter.split_documents(documents)
            db.add_documents(texts)
            db.persist()
    return db

db = initialize_vector_store()
retriever = db.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Create a retrieval tool
tools = [
    Tool(
        name="Code Knowledge Base",
        func=qa.run,
        description="Useful for answering questions about coding, programming languages, or software development."
    )
]

# Initialize agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Define the event handler for new files
class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filepath = event.src_path
            print(f"New file detected: {filepath}")
            self.process_new_file(filepath)

    def process_new_file(self, filepath):
        with db_lock:
            # Load and process the new file
            loader = TextLoader(filepath)
            documents = loader.load()
            texts = text_splitter.split_documents(documents)
            db.add_documents(texts)
            db.persist()
            print(f"Added {len(texts)} new documents to the vector store.")

# Start the directory watcher in a separate thread
def start_watcher():
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path="data", recursive=False)
    observer.start()
    print("Started directory watcher.")
    try:
        while True:
            # Keep the thread alive
            observer.join(timeout=1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Run the watcher in the background when the app starts
@app.on_event("startup")
def on_startup():
    watcher_thread = Thread(target=start_watcher, daemon=True)
    watcher_thread.start()

@app.post("/query")
async def query(query: Query):
    with db_lock:
        response = agent.run(query.query)
    return {"response": response}

@app.post("/rag")
async def rag(query: Query):
    with db_lock:
        response = qa.run(query.query)
    return {"response": response}
