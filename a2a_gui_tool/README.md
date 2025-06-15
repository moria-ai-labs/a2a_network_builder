# A2A Agent Configuration GUI Tool

## Overview

This tool provides a graphical user interface (GUI) for configuring A2A (Agent-to-Agent) agents using the `a2a-sdk`. It allows users to define an Agent Card, an optional Extended Agent Card, server settings, and known agent relationships, and then generates the corresponding Python SDK code.

## Features

*   **Comprehensive Configuration:** GUI tabs for defining:
    *   Agent Card (name, URL, version, description, capabilities, skills)
    *   Extended Agent Card (overrides for name, description, version, additional skills)
    *   Server Configuration (Agent Executor class, Task Store selection)
    *   Agent Relationships (list of known related agents and their URLs)
*   **Dynamic UI:** Easily add or remove skills and agent relationships.
*   **Input Validation:** Basic checks for required fields to guide the user.
*   **Code Generation:** Generates Python code compatible with the `a2a-sdk`, which can be used as a starting point for an agent implementation.
*   **User-Friendly Interface:** Organized into tabs for easy navigation.

## Requirements

*   Python 3.7+
*   PyQt6
*   a2a-sdk

All Python dependencies are listed in `requirements.txt`.

## Setup

1.  **Clone the repository (or download the files):**
    ```bash
    # If this were a git repository:
    # git clone <repository_url>
    # cd a2a_gui_tool
    # For now, assume files are in the 'a2a_gui_tool' directory.
    cd a2a_gui_tool
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Running the Application

Ensure you are in the `a2a_gui_tool` directory and your virtual environment (if used) is activated.

```bash
python main.py
```

## How to Use

1.  **Launch the application.**
2.  **Navigate through the tabs to configure your agent:**
    *   **Agent Card:** Define the primary details of your agent, including its name, URL, capabilities (streaming, push notifications), and skills. Skill IDs and Names are required.
    *   **Extended Agent Card:** Optionally, provide overrides for the agent's name, description, or version, and add skills specific to this extended profile. Skill IDs and Names are required if skills are added.
    *   **Server Configuration:** Specify the class name for your `AgentExecutor` (required) and choose a `TaskStore` (e.g., `InMemoryTaskStore` or provide a path for a custom one).
    *   **Agent Relationships:** List other agents that this agent might interact with by providing their names and URLs.
3.  **Generate Code:** Once all configurations are set, click the "Generate Agent Code" button at the bottom.
4.  **View Generated Code:** The "Generated Code" tab will open, displaying the Python SDK code based on your inputs. You can copy this code to use in your agent project.
    *   The generated code includes placeholders (e.g., for your `AgentExecutor` class implementation) that you'll need to fill in.

## Future Improvements/Notes

*   **Advanced Validation:** Implement more sophisticated input validation (e.g., URL format, class name conventions).
*   **Network Visualization:** A feature to visualize agent relationships was initially considered but is not part of the current version.
*   **Code Saving:** Add functionality to directly save the generated code to a `.py` file.
*   **Configuration Loading/Saving:** Allow users to save their GUI configurations to a file and load them back into the tool.
*   **Packaging:** The application could be packaged into a standalone executable using tools like PyInstaller for easier distribution.

This tool aims to simplify the initial setup and boilerplate code generation for A2A agents.
