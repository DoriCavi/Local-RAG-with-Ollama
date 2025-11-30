from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
# import basics
import os
from dotenv import load_dotenv

# import streamlit
import streamlit as st

# import langchain
from langchain.agents import AgentExecutor
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_tool_calling_agent
from langchain import hub
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

def main():

    # source = "https://www.apple.com/ca/contact/pdf/accessibility_standards_policy.pdf"  # document per local path or URL
    source = "Apple Watch User Guide - 32.pdf"
    converter = DocumentConverter()
    result = converter.convert(source)
    entire_text = result.document.export_to_markdown()
    print(result.document.export_to_markdown())




    # Get the current project root directory (where your script is)
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Define PDF path relative to project root
    pdf_path = os.path.join(project_root, "Apple Watch User Guide.pdf")

    # Convert PDF to markdown and STORE the result
    markdown_text = result.document.export_to_markdown()  # ← Store in variable

    # Create output folder in project root
    output_dir = os.path.join(project_root, "markdown_output")
    os.makedirs(output_dir, exist_ok=True)

    # Extract just the PDF filename and change extension
    pdf_filename = os.path.basename(pdf_path)  # "your_document.pdf"
    markdown_filename = pdf_filename.replace(".pdf", ".md")  # "your_document.md"

    # Create full path: project_root/markdown_output/your_document.md
    output_filename = os.path.join(output_dir, markdown_filename)

    # Write to file
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(markdown_text)  # ← Use the stored variable

    print(f"Markdown saved to: {output_filename}")


    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )


    texts = text_splitter.create_documents([entire_text])




if __name__ == "__main__":
    main()