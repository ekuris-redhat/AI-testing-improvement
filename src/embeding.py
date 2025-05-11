from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredMarkdownLoader
import os


def get_readme_paths(directory):
    """
    Recursively finds all README file paths in the given directory.

    Args:
        directory (str): The root directory to search for README files.

    Returns:
        list: A list of absolute paths to all README files found.
    """
    readme_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().startswith("readme"):
                readme_paths.append(os.path.join(root, file))
    return readme_paths


def load_all_readmes(directory):
    """
    Recursively reads all files named README using UnstructuredMarkdownLoader
    and returns the parsed files.

    Args:
        directory (str): The root directory to search for README files.

    Returns:
        list: A list of parsed README contents as strings.
    """
    readme_contents = []
    readme_paths = get_readme_paths(directory)
    for file_path in readme_paths:
        try:
            document = UnstructuredMarkdownLoader(
                file_path, mode='elements').load()
            readme_contents.extend(document)
            print(f"Loaded {file_path} with {len(document)} elements.")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return readme_contents


def embed_from_path(path):
    """
    Embeds the README files from the given path and returns a retriever.

    Args:
        path (str): The root directory to search for README files.

    Returns:
        FAISS: A FAISS vector store retriever.
    """
    documents = load_all_readmes(path)
    return FAISS.from_documents(documents, OpenAIEmbeddings()).as_retriever()
