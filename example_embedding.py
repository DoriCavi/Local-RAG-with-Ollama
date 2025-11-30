from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large",
)

text_to_embed = "LangChain is a framework for developing applications powered by large language models (LLMs)."

single_vector = embeddings.embed_query(text_to_embed)
print(str(single_vector))