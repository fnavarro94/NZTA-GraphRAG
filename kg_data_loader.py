from groq import Groq
from llama_index.core import Settings, ServiceContext, StorageContext, SimpleDirectoryReader
from llama_index.llms.groq import Groq as Groq_llamaindex
#from llama_index.llms.ollama import Ollama as Ollama_llamaindex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.graph_stores.neo4j import Neo4jGraphStore, Neo4jPropertyGraphStore
from milvus import default_server
from dotenv import load_dotenv
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor, SimpleLLMPathExtractor, ImplicitPathExtractor, DynamicLLMPathExtractor
import os
import shutil
import time
from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor, SimpleLLMPathExtractor, ImplicitPathExtractor
from llama_index.core import KnowledgeGraphIndex, SimpleDirectoryReader
import nest_asyncio

load_dotenv()

# Retrieve API keys and credentials securely
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_URL = os.getenv('NEO4J_URL', 'bolt://localhost:7687')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'neo4j')


client = Groq(api_key = GROQ_API_KEY)

llm = Groq_llamaindex(model="llama3-groq-70b-8192-tool-use-preview",
                       api_key=GROQ_API_KEY,
                       temperature=0)


Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

StorageContext.llm = llm
ServiceContext.llm = llm


property_graph_store = Neo4jPropertyGraphStore(
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    url=NEO4J_URL,
    database=NEO4J_DATABASE,
)
storage_context = StorageContext.from_defaults(property_graph_store=property_graph_store)





nest_asyncio.apply()


# Initialize directories, batch size, wait time, and skip count

source_dir = "transport_data/sample_files/nzta/simple_files"
target_dir = "transport_data/sample_files/nzta/temp_files"
batch_size = 1
wait_minutes = 1  # Specify the wait time in minutes
skip_files = 0  # Number of files to skip

# Create the target directory if it does not exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
    

# Start by deleting anything under temp_files but not the directory itself
if os.path.exists(target_dir):
    for file_name in os.listdir(target_dir):
        file_path = os.path.join(target_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            shutil.rmtree(file_path)

# Read the list of already processed files
processed_files = set()
if os.path.exists("processed_files_text.txt"):
    with open("processed_files_test.txt", "r") as f:
        processed_files = set(line.strip() for line in f)

# List all files in the source directory
full_file_list = os.listdir(source_dir)

# Filter out files that have already been processed
full_file_list = [file for file in full_file_list if file not in processed_files]

# Optionally, skip the first 'k' files
if skip_files > 0:
    full_file_list = full_file_list[skip_files:]

# Calculate the number of batches needed
num_batches = len(full_file_list) // batch_size + (1 if len(full_file_list) % batch_size > 0 else 0)

for i in range(num_batches):
    # Determine the start and end indices for the current batch
    start_idx = i * batch_size
    end_idx = min(start_idx + batch_size, len(full_file_list))

    # Get the current batch of files
    current_batch = full_file_list[start_idx:end_idx]
    print(f"Processing batch {i+1}/{num_batches}: {current_batch}")

    # Copy the current batch of files to the target directory
    for file_name in current_batch:
        shutil.copy(os.path.join(source_dir, file_name), os.path.join(target_dir, file_name))

    # Process the current batch of files
    graph_documents = SimpleDirectoryReader(target_dir).load_data()
    
    extract_prompt = (
    "Extract up to {max_knowledge_triplets} knowledge triplets from the given text. "
    "Each triplet should be in the form of (head, relation, tail) with their respective types and properties.\n"
    "---------------------\n"
    "INITIAL ONTOLOGY:\n"
    "Entity Types: {allowed_entity_types}\n"
    "Entity Properties: {allowed_entity_properties}\n"
    "Relation Types: {allowed_relation_types}\n"
    "Relation Properties: {allowed_relation_properties}\n"
    "\n"
    "Use these types as a starting point, but introduce new types if necessary based on the context.\n"
    "\n"
    "GUIDELINES:\n"
    "- Output in JSON format: [{{'head': '', 'head_type': '', 'head_props': {{...}}, 'relation': '', 'relation_props': {{...}}, 'tail': '', 'tail_type': '', 'tail_props': {{...}}}}]\n"
    "- Use the most complete form for entities (e.g., 'New Zealand Transport Agency' instead of abbreviations)\n"
    "For any reference to the New Zealand Transport Agency, including variations such as 'NZ Transport Agency Waka Kotahi', ‘NZ Transport Agency,’ ‘National Transport Agency,’ ‘Waka Kotahi,’ or any similar phrasing, create the entity node as 'New Zealand Transport Agency.' Ensure all variations of this entity are consistently mapped to 'New Zealand Transport Agency' in the output.\n"
    "- Do not create entities like 'request' or 'response' as they appear frequently and do not contribute to meaningful graph structure.\n"
    "- Do not create entities that are numbers, prices, or non-essential terms (e.g., dates unless critical to the meaning).\n"
    "- Keep entities concise (3-5 words max).\n"
    "- Break down complex phrases into multiple triplets for better granularity.\n"
    "- Ensure the knowledge graph is coherent and easily understandable.\n"
    "- Ensure that all property values are primitive types (e.g., String, Integer, Float, Boolean) or arrays of these types. Do not use maps or other complex structures.\n"
    "---------------------\n"
    "EXAMPLE:\n"
    "Text: The New Zealand Transport Agency approved the funding for road maintenance on State Highway 1.\n"
    "Wellington City Council is collaborating with the New Zealand Transport Agency on improving road safety initiatives.\n"
    "Output:\n"
    "[{{'head': 'New Zealand Transport Agency', 'head_type': 'AGENCY', 'head_props': {{'prop1': 'val', ...}}, "
    "'relation': 'APPROVES', 'relation_props': {{'prop1': 'val', ...}}, "
    "'tail': 'funding for road maintenance', 'tail_type': 'FUNDING_DECISION', 'tail_props': {{'prop1': 'val', ...}}}},\n"
    " {{'head': 'Wellington City Council', 'head_type': 'ORGANIZATION', 'head_props': {{'prop1': 'val', ...}}, "
    "'relation': 'COLLABORATES_WITH', 'relation_props': {{'prop1': 'val', ...}}, "
    "'tail': 'New Zealand Transport Agency', 'tail_type': 'AGENCY', 'tail_props': {{'prop1': 'val', ...}}}},\n"
    " {{'head': 'road safety initiatives', 'head_type': 'PROJECT', 'head_props': {{'prop1': 'val', ...}}, "
    "'relation': 'IMPROVES', 'relation_props': {{'prop1': 'val', ...}}, "
    "'tail': 'State Highway 1', 'tail_type': 'INFRASTRUCTURE', 'tail_props': {{'prop1': 'val', ...}}}}]\n"
    "---------------------\n"
    "Text: {text}\n"
    "Output:\n"
)

    Settings.chunk_size = 512
    Settings.chunk_overlap = 20



    kg_extractor = DynamicLLMPathExtractor(
    llm=llm,
    extract_prompt=extract_prompt,
    max_triplets_per_chunk=15,
    
    num_workers=4,
    # Let the LLM infer entities and their labels (types) on the fly
    allowed_entity_types=['People', 'Organizations', 'Locations', 'Processes', 'Agreements', 'Buildings', 'Streets', 'Projects', 'Events','Policies', 'Rules', 'Laws'],
    # Let the LLM infer relationships on the fly
    allowed_relation_types=None,
    # LLM will generate any entity properties, set `None` to skip property generation (will be faster without)
    allowed_relation_props=[],
    # LLM will generate any relation properties, set `None` to skip property generation (will be faster without)
    allowed_entity_props=[],
    )

    graph_index = PropertyGraphIndex.from_documents(
    graph_documents,
    property_graph_store=property_graph_store,
    storage_context=storage_context,
    kg_extractors=[kg_extractor],
    embed_kg_nodes=True,
    show_progress=True)

    # Record the processed files immediately after processing
    with open("processed_files_test.txt", "a") as f:
        for file_name in current_batch:
            f.write(f"{file_name}\n")
            f.flush()  # Ensure data is written to disk
    print('Recorded processed files in processed_files.txt')

    # Wait for the specified number of minutes
    time.sleep(wait_minutes * 60)

    # Delete the processed files from the target directory
    for file_name in current_batch:
        os.remove(os.path.join(target_dir, file_name))

    print(f"Batch {i+1}/{num_batches} processed and cleaned up.\n")

print("All files processed. Processed files list updated in 'processed_files.txt'.")



