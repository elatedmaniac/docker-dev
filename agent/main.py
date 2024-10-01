from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.agents import Tool, create_react_agent
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer
import os
import threading
from threading import Lock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = FastAPI()

class Query(BaseModel):
    query: str
    model: str  # Specify which model to use ('phi3' or 'codegemma')

# Initialize LLMs
ollama_phi3 = Ollama(
    base_url=os.getenv("OLLAMA_BASE_URL_PHI3", "http://phi3:11434"),
    model="phi3:3.8b"
)

ollama_codegemma = Ollama(
    base_url=os.getenv("OLLAMA_BASE_URL_CODEGEMMA", "http://codegemma:11434"),
    model="codegemma"
)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize vector store components
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
db_lock = Lock()  # Lock to manage concurrent access to the vector store

# Initialize the vector store
def initialize_vector_store():
    with db_lock:
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
                        # Use PyPDFLoader for PDF files
                        if filename.lower().endswith(".pdf"):
                            loader = PyPDFLoader(filepath)
                            documents.extend(loader.load())
                        else:
                            raise ValueError(f"Unsupported file format: {filename}")
                texts = text_splitter.split_documents(documents)
                db.add_documents(texts)
        return db

db = initialize_vector_store()
retriever = db.as_retriever()

# Initialize RetrievalQA for both models
qa_phi3 = RetrievalQA.from_chain_type(
    llm=ollama_phi3,
    chain_type="stuff",
    retriever=retriever
)

qa_codegemma = RetrievalQA.from_chain_type(
    llm=ollama_codegemma,
    chain_type="stuff",
    retriever=retriever
)

# Create retrieval tools for both models
tools_phi3 = [
    Tool(
        name="PDF Knowledge Base",
        func=qa_phi3.run,
        description="Useful for answering questions about documents, programming languages, or cybersecurity."
    )
]

tools_codegemma = [
    Tool(
        name="Code Knowledge Base",
        func=qa_codegemma.run,
        description="Useful for answering questions about coding, programming languages, or software development."
    )
]

# Define tool names for each agent
tool_names_phi3 = [tool.name for tool in tools_phi3]
tool_names_codegemma = [tool.name for tool in tools_codegemma]

# Create the prompt template
template = """You are a helpful assistant that uses the following tools to answer questions:
{tools}

When answering, you should follow this format:

Question: {input}
Thought: think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Now, begin!

{agent_scratchpad}"""

# Create the prompt templates for both agents
prompt_phi3 = PromptTemplate(
    template=template,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
).partial(tools=tools_phi3, tool_names=tool_names_phi3)

prompt_codegemma = PromptTemplate(
    template=template,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
).partial(tools=tools_codegemma, tool_names=tool_names_codegemma)

# Initialize agents for both models using create_react_agent
agent_executor_phi3 = create_react_agent(
    llm=ollama_phi3,
    tools=tools_phi3,
    prompt=prompt_phi3
)

agent_executor_codegemma = create_react_agent(
    llm=ollama_codegemma,
    tools=tools_codegemma,
    prompt=prompt_codegemma
)

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
            if filepath.lower().endswith(".pdf"):
                loader = PyPDFLoader(filepath)
                new_documents = loader.load()
                new_texts = text_splitter.split_documents(new_documents)
                db.add_documents(new_texts)
                print(f"New file processed and added to the vector store: {filepath}")
            else:
                print(f"Unsupported file format for file: {filepath}")

# Set up the file system observer
def start_file_observer():
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path="data", recursive=False)
    observer.start()
    print("Started file observer for 'data' directory.")
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Start the file observer in a separate thread
observer_thread = threading.Thread(target=start_file_observer, daemon=True)
observer_thread.start()

@app.post("/query")
def query_agent(query: Query):
    try:
        if query.model.lower() == "phi3":
            print(f"Querying phi3 model with query: {query.query}")
            response = agent_executor_phi3.invoke({query.query})
        elif query.model.lower() == "codegemma":
            response = agent_executor_codegemma.invoke({query.query})
        else:
            return {"error": "Invalid model specified. Choose 'phi3' or 'codegemma'."}
        return {"response": response}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
