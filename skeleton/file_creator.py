import time

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

response_test = {"Quantum Mechanics": {"Background Knowledge": {"Classical Physics": ["Newtonian Mechanics", "Electromagnetism", "Thermodynamics"], "Wave-Particle Duality": ["Double-Slit Experiment", "Wave-Particle Duality of Electromagnetic Radiation", "Wave-Particle Duality of Matter"], "Quantization": ["Quantum States", "Energy Levels", "Quantum Numbers"], "Uncertainty Principle": ["Position-Momentum Uncertainty", "Energy-Time Uncertainty", "Generalized Uncertainty Principle"]}, "Foundational Concepts": {"Wave Functions": ["Probability Amplitude", "Normalization", "Superposition", "Wave Function Collapse"], "Operators and Observables": ["Hermitian Operators", "Eigenvalues and Eigenvectors", "Expectation Values"], "Quantum States and Measurements": ["State Vectors", "Measurement Postulates", "Projection Postulate"], "Time Evolution of Quantum Systems": ["Schrodinger Equation", "Time-Dependent Schrodinger Equation", "Time-Independent Schrodinger Equation"], "Entanglement": ["Bell State", "Entanglement Swapping", "Quantum Teleportation"]}, "Quantum Mechanics in One Dimension": {"Particle in a Box": ["Infinite Square Well", "Finite Square Well", "Tunneling"], "Harmonic Oscillator": ["Quantization of Energy Levels", "Wave Functions", "Hermite Polynomials"], "Quantum Tunneling": ["Barrier Penetration", "Tunneling Probability"]}, "Angular Momentum and Spin": {"Angular Momentum Operators": ["Orbital Angular Momentum", "Spin Angular Momentum"], "Quantization of Angular Momentum": ["Spherical Harmonics", "Clebsch-Gordan Coefficients", "Angular Momentum Addition"], "Electron Spin": ["Pauli Matrices", "Spin Operators", "Spin-Orbit Interaction"]}, "Time-Independent Perturbation Theory": {"First-Order Perturbation Theory": ["Energy Shift", "Wave Function Correction"], "Second-Order Perturbation Theory": ["Degenerate Perturbation Theory", "Non-Degenerate Perturbation Theory", "Fine Structure of Hydrogen Atom"], "Variational Method": ["Trial Wave Function", "Variational Principle"]}, "Scattering Theory": {"Scattering Cross Section": ["Rutherford Scattering", "Differential Cross Section", "Total Cross Section"], "Partial Wave Analysis": ["Scattering Amplitude", "Partial Wave Expansion", "Partial Wave Analysis"], "Born Approximation": ["First Born Approximation", "Second Born Approximation", "Born Series"]}, "Quantum Mechanics of Identical Particles": {"Symmetry and Exchange": ["Bosons and Fermions", "Permutation Symmetry", "Exchange Interaction"], "Identical Particle Systems": ["Symmetric and Anti-Symmetric Wave Functions", "Pauli Exclusion Principle", "Hund's Rules"], "Quantum Statistics": ["Bose-Einstein Statistics", "Fermi-Dirac Statistics", "Maxwell-Boltzmann Statistics"]}, "Quantum Mechanics in Three Dimensions": {"Hydrogen Atom": ["Radial Equation", "Angular Equation", "Spherical Harmonics"], "Angular Momentum Coupling": ["Clebsch-Gordan Coefficients", "Wigner-Eckart Theorem", "Russell-Saunders Coupling"], "Central Potentials": ["Spherically Symmetric Potentials", "Scattering States", "Bound States"]}, "Quantum Mechanics and Electromagnetism": {"Quantum Electrodynamics": ["Quantization of Electromagnetic Field", "Feynman Diagrams", "Renormalization"], "Interaction of Matter with Radiation": ["Absorption and Emission of Photons", "Selection Rules", "Spontaneous and Stimulated Emission"], "Coherent States": ["Coherent States of Harmonic Oscillator", "Photon Number States", "Squeezed States"]}, "Quantum Mechanics and Statistical Mechanics": {"Density Operator": ["Statistical Ensemble", "Mixed States", "Pure States"], "Quantum Statistical Mechanics": ["Canonical Ensemble", "Grand Canonical Ensemble", "Quantum Phase Transitions"], "Quantum Entropy": ["von Neumann Entropy", "Quantum Mutual Information", "Quantum Entanglement Entropy"]}, "Interpretations of Quantum Mechanics": {"Copenhagen Interpretation": ["Wave Function Collapse", "Measurement Problem", "Observer Effect"], "Many-Worlds Interpretation": ["Parallel Universes", "Superposition of Branches", "Quantum Immortality"], "Bohmian Mechanics": ["Pilot Wave Theory", "Determinism and Non-Locality", "Quantum Potential"], "Decoherence Theory": ["Environment-Induced Decoherence", "Quantum-Classical Boundary", "Emergence of Classical Reality"]}, "Applications of Quantum Mechanics": {"Quantum Computing": ["Quantum Gates", "Quantum Algorithms", "Quantum Error Correction"], "Quantum Cryptography": ["Quantum Key Distribution", "Eavesdropping Detection", "Security in Quantum Cryptography"], "Quantum Sensing and Metrology": ["Quantum Metrology", "Quantum Sensors", "Quantum Imaging"], "Quantum Communication": ["Quantum Teleportation", "Quantum Teleportation Network", "Quantum Repeaters"], "Quantum Simulation": ["Digital Quantum Simulation", "Analog Quantum Simulation", "Applications in Condensed Matter Physics"]}}}

# Temporary directory for llm
working_directory = "/Users/erik/Documents/Obsidian/jArvIs"
file_management_toolkit = FileManagementToolkit(root_dir=working_directory)

tools = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()

read_tool, write_tool, list_tool = tools

def generate_files(response):
    topic = next(iter(response)).replace(" ", "")

    def generate_md_files(name, content, immediate_parent):
        time.sleep(.25)

        if isinstance(content, dict):  # If content is a dictionary
            md_content = ", ".join(f"[[{k}]]" for k in content)

            # Write the content to the markdown file
            write_tool.run({"file_path": f"{name}.md", "text": f"Topic: #{topic}\n\n\n\nParents: [[{immediate_parent}]]\n\nChildren: {md_content}"})

            for k, v in content.items():
                generate_md_files(k, v, name)

        elif isinstance(content, list):  # If content is a list
            md_content = "\n".join(f"[[{item}]]" for item in content)
            # Write the content to the markdown file
            write_tool.run({"file_path": f"{name}.md", "text": f"Topic: #{topic}\n\n\n\nParents: [[{immediate_parent}]]\n\nChildren: {md_content}"})

            for subject in content:
                write_tool.run({"file_path": f"{subject}.md", "text": f"Topic: #{topic}\n\n\n\nParents: [[{name}]]\n\nBottom of tree"})
        else:
            return

    # Start the process from the root of the response
    try:
        for k, v in response.items():
            generate_md_files(k, v, "")
    except ValueError as e:
        print("Error:", str(e))

if __name__ == "__main__":
    generate_files(response_test)