from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
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
    Recursively reads all files named README using UnstructuredMarkdownLoader and returns the parsed files.

    Args:
        directory (str): The root directory to search for README files.

    Returns:
        list: A list of parsed README contents as strings.
    """
    readme_contents = []
    readme_paths = get_readme_paths(directory)
    for file_path in readme_paths:
        try:
            loader = UnstructuredMarkdownLoader(file_path, mode='elements')
            documents = loader.load()
            for doc in documents:
                readme_contents.append(doc.page_content)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return readme_contents

# Example usage:
readmes = load_all_readmes("/home/ekuris/Desktop/repos/nfv_ansible_tests")
print(readmes)

