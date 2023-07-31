import os
import re
from dotenv import load_dotenv

# Retrieval
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper

# Prompting
from langchain.prompts import PromptTemplate

# LLM response
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Creating files
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.agents.agent_toolkits import FileManagementToolkit
from tempfile import TemporaryDirectory

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

response_test = {
    "Quantum Mechanics": {
        "Background Knowledge": {
            "Classical Physics": [
                "Newton's Laws of Motion",
                "Law of Universal Gravitation",
                "Maxwell's Equations"
            ],
            "Wave-Particle Duality": [
                "Double-Slit Experiment",
                "Interference",
                "Diffraction"
            ],
            "Probability Theory": [
                "Probability Distributions",
                "Conditional Probability",
                "Bayes' Theorem"
            ],
            "Linear Algebra": [
                "Vectors",
                "Matrices",
                "Eigenvalues and Eigenvectors"
            ]
        },
        "Mathematical Formulations": {
            "Wave Function": [
                "Schrodinger Equation",
                "Time-Independent Schrodinger Equation",
                "Time-Dependent Schrodinger Equation"
            ],
            "Hilbert Space": [
                "Basis States",
                "Inner Product",
                "Operators"
            ],
            "Quantum States and Observables": [
                "Superposition",
                "Measurement",
                "Expectation Values"
            ],
            "Quantum Operators": [
                "Hermitian Operators",
                "Unitary Operators",
                "Commutation Relations"
            ],
            "Quantum Dynamics": [
                "Time Evolution",
                "Hamiltonian",
                "Time-Independent Perturbation Theory"
            ]
        },
        "Interpretations of Quantum Mechanics": {
            "Copenhagen Interpretation": [
                "Wave Function Collapse",
                "Born Rule"
            ],
            "Many-Worlds Interpretation": [
                "Parallel Universes",
                "Quantum Decoherence"
            ],
            "Bohmian Mechanics": [
                "Pilot Wave Theory",
                "Deterministic Trajectories"
            ],
            "Consistent Histories Interpretation": [
                "Quantum Histories",
                "Decoherent Histories"
            ],
            "Objective Collapse Theories": [
                "Gravitationally Induced Collapse",
                "Spontaneous Localization"
            ]
        },
        "Applications in Quantum Physics": {
            "Quantum Chemistry": [
                "Molecular Orbitals",
                "Electronic Structure",
                "Chemical Reactions"
            ],
            "Quantum Field Theory": [
                "Quantum Electrodynamics",
                "Quantum Chromodynamics",
                "Electroweak Theory"
            ],
            "Quantum Technology": [
                "Quantum Computing",
                "Quantum Cryptography",
                "Quantum Sensing"
            ],
            "Quantum Information Science": [
                "Quantum Entanglement",
                "Quantum Teleportation",
                "Quantum Error Correction"
            ]
        },
        "Foundational Issues": {
            "Measurement Problem": [
                "Observer Effect",
                "Schrödinger's Cat"
            ],
            "Nonlocality and Bell's Theorem": [
                "EPR Paradox",
                "Bell Inequalities"
            ],
            "Quantum Entanglement": [
                "Entanglement Swapping",
                "Quantum Teleportation"
            ],
            "Quantum Paradoxes": [
                "Quantum Zeno Effect",
                "Quantum Cheshire Cat"
            ],
            "Quantum Computing and Quantum Information": [
                "Quantum Algorithms",
                "Quantum Error Correction"
            ]
        }
    }
}

# Temporary directory for llm
working_directory = TemporaryDirectory()
file_management_toolkit = FileManagementToolkit(root_dir=working_directory.name)
print(working_directory.name)

tools = FileManagementToolkit(
    root_dir=str(working_directory.name),
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()

read_tool, write_tool, list_tool = tools

def generate_files(response):

    def generate_md_files(name, content):
        #print(name, content)
        if isinstance(content, dict):  # If content is a dictionary
            md_content = ", ".join(f"[[{k}]]" for k in content)

            # Write the content to the markdown file
            write_tool.run({"file_path": f"{name}.md", "text": md_content})

    #         for k, v in content.items():
    #             generate_md_files(k, v)
    #     elif isinstance(content, list):  # If content is a list
    #         md_content = "\n".join(f"[[{item}]]" for item in content)
    #     else:
    #         return

    #     # Write the content to the markdown file
    #     write_tool.run({"file_path": f"{name}.md", "text": md_content})

    # Start the process from the root of the response
    for k, v in response.items():
        generate_md_files(k, v)

if __name__ == "__main__":
    generate_files(response_test)