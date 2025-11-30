# import basics
import os
from dotenv import load_dotenv
# import streamlit
import streamlit as st
# import langchain
from langchain.agents import AgentExecutor
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_tool_calling_agent
from langchain import hub
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
import DocParsing
from langchain.schema import Document
from UI import questions
import UI
import shutil
load_dotenv()


def retrieve_documents(vector_store, embeddings, question, k=5):
    """Retrieve documents using similarity search by vector."""
    
    # Get embedding for question
    query_embedding = embeddings.embed_query(question)
    
    # Search by vector
    results = vector_store.similarity_search_by_vector(
        embedding=query_embedding,
        k=k
    )
    
    # Print results
    print(f"\nRetrieved {len(results)} documents for: '{question}'\n")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.page_content[:100]}... [{doc.metadata}]")
    
    return results


def answer_with_retrieved_docs(docs, llm, prompt, question):
    """Generate answer from retrieved documents."""
    
    # Format context
    # context = "\n\n".join([
    #     f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
    #     for doc in docs
    # ])

    context = "\n\n".join([doc.page_content.strip() for doc in docs])
    
    # DIAGNOSTIC: Print everything
    print("\n" + "="*80)
    print("DIAGNOSTIC INFO")
    print("="*80)
    print(f"Number of docs: {len(docs)}")
    print(f"Context length: {len(context)} characters")
    print(f"Question: {question}")
    print("\nFirst doc content:")
    print(docs[0].page_content[:300] if docs else "No docs")
    print("\nFormatted context preview:")
    print(context[:300])
    print("="*80)
    
    # Generate answer
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"context": context, "question": question})
    
    print("\nAnswer received:")
    print(answer)
    print("="*80 + "\n")
    
    # return chain.invoke({"context": context, "question": question})
    return answer


def setup_rag():
    # Embeddings
    embeddings = OllamaEmbeddings(model=os.getenv("EMBEDDING_MODEL"))
    
    
    db_path = os.getenv("DATABASE_LOCATION")
    if os.path.exists(db_path):
        print(f"Deleting old database at {db_path}")
        shutil.rmtree(db_path)


    # Vector store
    vector_store = Chroma(
        collection_name=os.getenv("COLLECTION_NAME"),
        embedding_function=embeddings,
        persist_directory=os.getenv(db_path), 
    )
    
    # Check if database already has documents
    existing_count = vector_store._collection.count()
    # print(f"📊 Existing documents in database: {existing_count}")
    
    if existing_count == 0:
        # print("\n⚠️ Database is empty. Adding documents...")
        
        # Read markdown file
        with open("markdown_output/Apple Watch User Guide.md", "r", encoding="utf-8") as f:
            markdown_content = f.read()


        # Create document
        doc = Document(
            page_content=markdown_content,
            metadata={"source": "Apple Watch User Guide.md"}
        )

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300, 
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", "! ", "? ", " "]
        )
        chunks = text_splitter.split_documents([doc])

        # print("\n📋 Sample chunks (first 5):")
        # for i, chunk in enumerate(chunks[:5]):
        #     print(f"\n--- Chunk {i+1} ---")
        #     print(chunk.page_content)
        #     print("-" * 40)



        print(f"Created {len(chunks)} chunks")


        # Add ALL chunks to vector store
        vector_store.add_documents(chunks)

        print(f"✅ Added {len(chunks)} chunks to database")
        print(f"Total documents in database: {vector_store._collection.count()}")
        
        # Peek at first few stored documents
        results = vector_store._collection.peek(limit=3)

        print("\n📄 First 3 documents in database:")
        for i in range(min(3, len(results["documents"]))):
            print(f"\nDocument {i+1}:")
            print(f"  Content:\n{results['documents'][i][:300]}...\n")
            print(f"  Metadata: {results['metadatas'][i]}")
    else:
        print("✅ Database already contains documents")
    
    # LLM
    llm = ChatOllama(model=os.getenv("CHAT_MODEL"), temperature=0.3)
    
    # Prompt
    prompt = PromptTemplate.from_template("""
    You are a knowledgeable assistant helping users with Apple Watch questions.

    Reference Information:
    {context}

    User Question:
    {question}

    Provide a clear, detailed answer based on the reference information above. Write naturally and be helpful.

    Answer:
    """)
    
    return vector_store, llm, prompt, embeddings


vector_store = None
llm = None
prompt = None
embeddings = None

def initialize_rag():
    global vector_store, llm, prompt, embeddings
    
    print("Setting up RAG system...")
    vector_store, llm, prompt, embeddings = setup_rag()
    print("✅ RAG system ready!")


def ask_question(question):
    if not vector_store or not llm:
        return "Error: RAG system not initialized"
    
    print(f"🔍 Processing: {question}")
    
    # Step 1: Retrieve documents
    docs = retrieve_documents(vector_store, embeddings, question, k=3)
    
    # Step 2: Generate answer
    answer = answer_with_retrieved_docs(docs, llm, prompt, question)
    
    print(f"✅ Answer generated")
    print(answer)
    return answer
    


def main():
    # DocParsing.main() 
    initialize_rag()
    # print("Setting up RAG system...")
    # vector_store, llm, prompt, embeddings = setup_rag()
    # print("\n✅ RAG system ready!\n")
    # print("=" * 60)

    demo = UI.create_demo(ask_question)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        inbrowser=True,
        share=False
    )

    # # Ask questions
    # questions = [
    #     # "What is Apple's accessibility policy?",
    #     # "What specific accessibility features does Apple provide?",
    #     # "What is the Training Schedule of apple canada",
    # "are people with Guide Dogs and Service Animals  allowed access to Apple Stores?",
    # "If a customer with a disability is accompanied by a support person, Apple Canada will ensure that ...."
    # ]
    # print(questions)
    
    for question in questions:
        print(f"\n{'='*60}")
        print(f"🔍 Question: {question}")
        print('='*60)
        
        # Step 1: Retrieve documents
        docs = retrieve_documents(vector_store, embeddings, question, k=3)
        
        # Step 2: Generate answer
        answer = answer_with_retrieved_docs(docs, llm, prompt, question)
        
        print(f"\n📝 Answer:\n{answer}\n")
        print("-" * 60)

if __name__ == "__main__":
    main()
