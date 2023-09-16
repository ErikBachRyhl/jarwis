# Run this to create a mindmap in obsidian vault "research"

from src.skeleton import generate_response, Query
from src.file_creator import generate_files

if __name__ == "__main__":
    query = Query(topic="Noethers Theorem")

    response = generate_response(query)
    
    print(f"Generating files with response: {response}")
    generate_files(response)
