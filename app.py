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

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
#model="gpt-3.5-turbo-16k-0613"
llm = ChatOpenAI(openai_api_key=openai_api_key)

template = """You are a helpful research assistant and teacher. 
I would like you to help me understand how topics relate to each other and the strcuture of knowledge.
I will provide you with the name of a topic and some information on the topic from wikipedia. 
Based on the wikipedia description of the topic, your goal is to write a list of related topics / subtopics / necessary techniques or methods to be learned in order to fully grasp and understand a complex topic.
The list should be formatted with the following steps as below:

1/ Wrap each topic like this: [[TOPIC NAME]]
2/ Return a nested dictionary which contains the heirarchy of the topics.

Here is an example of a correctly formatted list:
{{"MAIN TOPIC": {{
    "SUB TOPIC 1": ["SUB 1 SUB TOPIC 1", "SUB 1 SUB TOPIC 2"],
    "SUB TOPIC 2": ["SUB 2 SUB TOPIC 1", "SUB 2 SUB TOPIC 2", "SUB 2 SUB TOPIC 3"],
    "SUB TOPIC 3": ["SUB 3 SUB TOPIC 1"]
    }}
}}

Here is an example response on "General Relativity" following above rules:
{{
    "General Relativity": {{
        "Background Knowledge": {{
            "Special Relativity": [
                "Lorentz Transformations", 
                "Time Dilation", 
                "Length Contraction",
                "Minkowski Space-Time"
            ],
            "Newton's Law of Universal Gravitation": [
                "Gravity Force",
                "Gravitational Constant",
                "Inverse Square Law"
            ],
            "Differential Geometry": [
                "Manifolds", 
                "Metric Tensor", 
                "Christoffel Symbols",
                "Geodesics",
                "Riemann Curvature Tensor"
            ],
            "Tensor Calculus": [
                "Tensor Basics", 
                "Contravariant and Covariant Tensors", 
                "Tensor Operations",
                "Metric Tensor",
                "Ricci Curvature"
            ]
        }},
        "Basics of General Relativity": {{
            "Spacetime": [
                "Event", 
                "Worldline", 
                "Light Cone"
            ],
            "Einstein Field Equations": [
                "Energy-Momentum Tensor", 
                "Einstein's Field Equations Solutions"
            ],
            "Curvature of Spacetime": [
                "Geodesic Deviation",
                "Geodetic Effect",
                "Frame-Dragging"
            ],
            "Energy-Momentum Tensor": [
                "Stress-Energy Tensor",
                "Perfect Fluid"
            ]
        }},
        "Predictions and Experimental Tests": {{
            "Gravitational Time Dilation": [
                "Hafele–Keating Experiment"
            ],
            "Gravitational Lensing": [
                "Einstein Cross",
                "Einstein Ring"
            ],
            "Gravitational Redshift of Light": [
                "Pound–Rebka Experiment"
            ],
            "Shapiro Time Delay": [
                "Radar Echo Delay Tests"
            ],
            "Singularities/Black Holes": [
                "Event Horizon",
                "Schwarzschild Radius",
                "Hawking Radiation",
                "Interiors of Black Holes"
            ]
        }},
        "Applications in Cosmology": {{
            "Big Bang Theory": [
                "Cosmic Inflation", 
                "Timeline of the Big Bang"
            ],
            "Cosmic Microwave Background Radiation": [
                "Discovery of CMB", 
                "CMB Spectrum",
                "CMB Anisotropies"
            ],
            "Expansion of the Universe": [
                "Hubble's Law",
                "Dark Energy",
                "Fate of the Universe"
            ]
        }},
        "Astrophysical Implications": {{
            "Black Holes": [
                "Schwarzschild Black Holes",
                "Kerr Black Holes",
                "Black Hole Thermodynamics"
            ],
            "Microquasars and Active Galactic Nuclei": [
                "Accretion Disk",
                "Astrophysical Jets"
            ],
            "Gravitational Waves": [
                "Detection by LIGO",
                "Gravitational Wave Astronomy",
                "Sources of Gravitational Waves"
            ],
            "Gravitational Lensing": [
                "Strong Lensing",
                "Weak Lensing",
                "Microlensing"
            ],
            "Expanding Universe Models": [
                "Friedmann-Lemaître-Robertson-Walker metric",
                "Observational Evidence"
            ]
        }},
        "Unresolved Issues": {{
            "Quantum Gravity": [
                "String Theory",
                "Loop Quantum Gravity"
            ],
            "Unification with Other Fundamental Forces": [
                "Grand Unified Theory",
                "Theory of Everything"
            ]
        }},
        "Philosophical and Theoretical Implications": {{
            "Concept of Time": [
                "Arrow of Time",
                "Block Universe"
            ],
            "Concept of Space": [
                "Absolute vs Relative Space"
            ],
            "The Nature of Gravity": [
                "Problem of Time",
                "Quantum Gravity"
            ],
            "Interpretations of General Relativity": [
                "Hole Argument",
                "Einstein's Equivalence Principle"
            ]
        }}
    }}
}}

Here is your topic name: {topic}
Wikipedia exerpt on {topic}:
{wiki_info}

Begin!
"""

# def extract_topics(text):
#     # Regular expression pattern for matching the topic syntax
#     pattern = re.compile(r'\[\[(.*?)(?:\|(.*?))?\]\]')
    
#     # Find all matches in the text
#     matches = pattern.findall(text)
    
#     # Extract the topic names and add them to the list
#     topics = [match[0] for match in matches]
    
#     return topics

# Put together prompt
prompt = PromptTemplate(
    input_variables=["topic", "wiki_info"], 
    template=template
)

# Query chatGPT
chain = LLMChain(
    llm=llm,
    prompt=prompt
)

name = "Quantum Mechanics"
    
def generate_response(topic_name):
    wiki_info = wikipedia.run(topic_name)
    response = chain.run(topic=topic_name, wiki_info=wiki_info)
    return response

#response = generate_response(name)

# Temporary directory for llm
working_directory = TemporaryDirectory()
file_management_toolkit = FileManagementToolkit(root_dir=working_directory.name)

tools = FileManagementToolkit(
    root_dir=str(working_directory.name),
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()

read_tool, write_tool, list_tool = tools

def generate_files(response):

    def generate_md_files(name, content):
        if isinstance(content, dict):  # If content is a dictionary
            md_content = ", ".join(f"[[{k}]]" for k in content)
            for k, v in content.items():
                generate_md_files(k, v)
        elif isinstance(content, list):  # If content is a list
            md_content = "\n".join(f"[[{item}]]" for item in content)
        else:
            return

        # Write the content to the markdown file
        write_tool.run({"file_path": f"{name}.md", "text": md_content})

    # Start the process from the root of the response
    for k, v in response.items():
        generate_md_files(k, v)


response = generate_response("Quantum Mechanics")
print(response)
generate_files(response)
