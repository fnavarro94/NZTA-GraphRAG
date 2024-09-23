import os
import sys
import logging
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from groq import Groq
from llama_index.core import (
    Settings,
    ServiceContext,
    StorageContext,
    PropertyGraphIndex,
)
from llama_index.llms.groq import Groq as GroqLlamaIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.indices.property_graph import VectorContextRetriever

# Load environment variables
load_dotenv()
print('loaded env vars')
# Retrieve API keys and credentials securely
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_URL = os.getenv('NEO4J_URL', 'bolt://localhost:7687')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'neo4j')

# Ensure all required environment variables are set
if not all([GROQ_API_KEY, NEO4J_USERNAME, NEO4J_PASSWORD]):
    raise EnvironmentError("Missing one or more required environment variables.")

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq client and LLM
client = Groq(api_key=GROQ_API_KEY)
llm = GroqLlamaIndex(
    model="llama3-groq-70b-8192-tool-use-preview",
    api_key=GROQ_API_KEY,
    temperature=0
)

# Configure LLM settings
Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
ServiceContext.llm = llm

# Set up Neo4j property graph store
property_graph_store = Neo4jPropertyGraphStore(
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    url=NEO4J_URL,
    database=NEO4J_DATABASE,
)
storage_context = StorageContext.from_defaults(property_graph_store=property_graph_store)

# Create property graph index
index = PropertyGraphIndex.from_existing(
    property_graph_store=property_graph_store,
    llm=llm,
    embed_model=Settings.embed_model,
)

# Initialize vector context retriever
vector_retriever = VectorContextRetriever(
    index.property_graph_store,
    embed_model=Settings.embed_model,
    include_text=True,
    similarity_top_k=3,
    path_depth=1,
)

# Set up query engine
index_query_engine = index.as_query_engine(sub_retrievers=[vector_retriever])

# Define query tool
query_tool = QueryEngineTool.from_defaults(
    index_query_engine,
    name="query_info_about_nzta_and_transportation_tool",
    description=(
        "Query the document database for answers specifically related to transport in New Zealand "
        "or to NZTA (New Zealand Transport Agency). The user's query must be given as input. "
        "Do not over-shorten the query; include all the details required by the user. "
        "Input the query in the form of a question. If the query provides a link to a website "
        "with the answer, please provide the link."
    ),
)

# Define mathematical functions
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return a * b

def add(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract two numbers and return the result."""
    return a - b

# Create function tools
multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)
subtract_tool = FunctionTool.from_defaults(fn=subtract)

# Initialize agent worker
agent_worker = FunctionCallingAgentWorker.from_tools(
    [multiply_tool, add_tool, subtract_tool, query_tool],
    llm=llm,
    verbose=True,
    allow_parallel_tool_calls=False,
    system_prompt=(
        "You are a helpful, chatty assistant that can use tools. "
        "Only use tools if necessary. Sometimes the user might just want to chat with you. "
        "Do not rely on your previous knowledge; if you don't know something, look it up with your query tool. "
        "Always prioritize the query tool for anything related to transport or NZTA. "
        "Do not ask permission or tell the user that you need to use the tool. Just go ahead and use it when needed!"
    ),
)

# Create agent runner
agent = AgentRunner(agent_worker)
print("Agent is ready to chat")

# Flask routes
@app.route('/')
def home():
    """Render the main page and initiate a new conversation ID if not present."""
    session_id = request.args.get('session_id', 'default')
    return render_template('index.html', session_id=session_id)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle incoming messages and send responses using the agent."""
    session_id = request.json.get('session_id', 'default')
    user_input = request.json['message']
    response = agent.chat(user_input).response
    print(agent.chat_history)
    return jsonify({'response': response})

if __name__ == '__main__':
    print("Flask app running on http://localhost:8080")
    app.run(debug=True, port=8080)
