import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QGroupBox,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QTabWidget,
    QComboBox,
    QMessageBox,
)
from PyQt6.QtCore import Qt
import re # For splitting comma-separated strings


# Helper function to format strings or lists of strings for code generation
def format_string_list_for_code(input_str: str) -> str:
    """
    Formats a comma or newline-separated string into a Python list string.
    Example: "item1, item2\nitem3" -> "['item1', 'item2', 'item3']"
    Returns "[]" for empty or whitespace-only input.
    """
    if not input_str.strip():
        return "[]"
    # Handles both comma-separated and newline-separated items
    items = [item.strip() for item in re.split(r'[,\n]', input_str) if item.strip()]
    return f"{[item for item in items]}"

def format_single_string_for_code(input_str: str) -> str:
    """
    Formats a single string for Python code, using triple quotes for multiline strings.
    """
    return f'"""{input_str}"""' if '\n' in input_str else f'"{input_str}"'


class SkillEntryWidget(QWidget):
    """
    A widget for entering the details of a single Agent Skill.
    Allows adding ID, name, description, tags, and examples for a skill.
    Includes a button to remove itself from its parent layout.
    """
    def __init__(self, parent_layout: QVBoxLayout):
        super().__init__()
        self.parent_layout = parent_layout
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components for the skill entry widget."""
        layout = QFormLayout()
        self.setLayout(layout)

        self.id_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.description_edit = QTextEdit()
        self.tags_edit = QLineEdit()
        self.examples_edit = QTextEdit()
        remove_skill_button = QPushButton("Remove Skill")
        remove_skill_button.clicked.connect(self.remove_self)

        layout.addRow("ID (*):", self.id_edit) # Skill ID, required
        layout.addRow("Name (*):", self.name_edit) # Skill Name, required
        layout.addRow("Description:", self.description_edit)
        layout.addRow("Tags (comma-separated):", self.tags_edit)
        layout.addRow("Examples (multi-line or comma-separated):", self.examples_edit)
        layout.addWidget(remove_skill_button)

    def remove_self(self):
        self.setParent(None)
        self.parent_layout.removeWidget(self)
        # Optionally, explicitly delete the widget if necessary,
        # though setParent(None) usually handles this for Qt.
        self.deleteLater()

    def get_data(self) -> dict:
        """
        Retrieves the skill data entered in the widget.
        Returns a dictionary with keys: id, name, description, tags, examples.
        Tags and examples are formatted as Python list strings.
        """
        return {
            "id": self.id_edit.text().strip(),
            "name": self.name_edit.text().strip(),
            "description": self.description_edit.toPlainText().strip(),
            "tags": format_string_list_for_code(self.tags_edit.text()),
            "examples": format_string_list_for_code(self.examples_edit.toPlainText()),
        }


class AgentCardWidget(QWidget):
    """
    A widget for configuring the main Agent Card attributes, capabilities, and skills.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components for the Agent Card configuration tab."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Main Agent Card Attributes ---
        main_attributes_group = QGroupBox("Main Agent Card Attributes")
        main_attributes_layout = QFormLayout()
        main_attributes_group.setLayout(main_attributes_layout)

        self.name_edit = QLineEdit()
        self.url_edit = QLineEdit()
        self.version_edit = QLineEdit()
        self.description_edit = QTextEdit()
        self.default_input_modes_edit = QLineEdit()
        self.default_output_modes_edit = QLineEdit()

        main_attributes_layout.addRow("Name (*):", self.name_edit)
        main_attributes_layout.addRow("URL (*):", self.url_edit)
        main_attributes_layout.addRow("Version:", self.version_edit)
        main_attributes_layout.addRow("Description:", self.description_edit)
        main_attributes_layout.addRow("Default Input Modes (comma-separated):", self.default_input_modes_edit)
        main_attributes_layout.addRow("Default Output Modes (comma-separated):", self.default_output_modes_edit)
        main_layout.addWidget(main_attributes_group)

        # Agent Capabilities
        capabilities_group = QGroupBox("Agent Capabilities")
        capabilities_layout = QFormLayout() # Or QHBoxLayout
        capabilities_group.setLayout(capabilities_layout)

        self.streaming_checkbox = QCheckBox("Streaming")
        self.push_notifications_checkbox = QCheckBox("Push Notifications")

        capabilities_layout.addRow(self.streaming_checkbox)
        capabilities_layout.addRow(self.push_notifications_checkbox)
        main_layout.addWidget(capabilities_group)

        # Agent Skills
        skills_group = QGroupBox("Agent Skills")
        self.skills_main_layout = QVBoxLayout() # Made self to access later
        skills_group.setLayout(self.skills_main_layout)

        add_skill_button = QPushButton("Add Skill")
        add_skill_button.clicked.connect(self.add_skill_ui)
        self.skills_main_layout.addWidget(add_skill_button)

        self.skills_scroll_area = QScrollArea()
        self.skills_scroll_area.setWidgetResizable(True)
        self.skills_widget_container = QWidget()
        self.skills_layout = QVBoxLayout(self.skills_widget_container) # This is the layout to add SkillEntryWidgets
        self.skills_widget_container.setLayout(self.skills_layout)
        self.skills_scroll_area.setWidget(self.skills_widget_container)

        self.skills_main_layout.addWidget(self.skills_scroll_area) # Corrected: add scroll_area to skills_main_layout
        main_layout.addWidget(skills_group)

    def add_skill_ui(self):
        skill_widget = SkillEntryWidget(self.skills_layout)
        self.skills_layout.addWidget(skill_widget)

    def get_data(self) -> dict:
        """
        Retrieves all data entered for the Agent Card.
        Returns a dictionary containing name, description, url, version,
        defaultInputModes, defaultOutputModes, capabilities (dict), and skills (list of dicts).
        """
        skills_data = []
        # Iterate through dynamically added SkillEntryWidget instances
        for i in range(self.skills_layout.count()):
            widget = self.skills_layout.itemAt(i).widget()
            if isinstance(widget, SkillEntryWidget):
                skills_data.append(widget.get_data())

        return {
            "name": self.name_edit.text().strip(),
            "description": self.description_edit.toPlainText().strip(),
            "url": self.url_edit.text().strip(),
            "version": self.version_edit.text().strip(),
            "defaultInputModes": format_string_list_for_code(self.default_input_modes_edit.text()),
            "defaultOutputModes": format_string_list_for_code(self.default_output_modes_edit.text()),
            "capabilities": {
                "streaming": self.streaming_checkbox.isChecked(),
                "pushNotifications": self.push_notifications_checkbox.isChecked(),
            },
            "skills": skills_data,
        }


class ExtendedAgentCardWidget(QWidget):
    """
    A widget for configuring the Extended Agent Card, allowing overrides for
    name, description, version, and addition of new skills.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components for the Extended Agent Card configuration tab."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Overridable Attributes ---
        overridable_attributes_group = QGroupBox("Extended Agent Card Attributes (Overrides)")
        overridable_attributes_layout = QFormLayout()
        overridable_attributes_group.setLayout(overridable_attributes_layout)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Inherits from Agent Card if empty")
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Inherits from Agent Card if empty")
        self.version_edit = QLineEdit()
        self.version_edit.setPlaceholderText("Inherits from Agent Card if empty")

        overridable_attributes_layout.addRow("Name:", self.name_edit)
        overridable_attributes_layout.addRow("Description:", self.description_edit)
        overridable_attributes_layout.addRow("Version:", self.version_edit)
        main_layout.addWidget(overridable_attributes_group)

        # Extended Agent Skills
        extended_skills_group = QGroupBox("Extended Agent Skills (Additive)")
        self.extended_skills_main_layout = QVBoxLayout() # Made self
        extended_skills_group.setLayout(self.extended_skills_main_layout)

        add_extended_skill_button = QPushButton("Add Skill to Extended Card")
        add_extended_skill_button.clicked.connect(self.add_extended_skill_ui)
        self.extended_skills_main_layout.addWidget(add_extended_skill_button)

        self.extended_skills_scroll_area = QScrollArea()
        self.extended_skills_scroll_area.setWidgetResizable(True)
        self.extended_skills_widget_container = QWidget()
        self.extended_skills_layout = QVBoxLayout(self.extended_skills_widget_container)
        self.extended_skills_widget_container.setLayout(self.extended_skills_layout)
        self.extended_skills_scroll_area.setWidget(self.extended_skills_widget_container)

        self.extended_skills_main_layout.addWidget(self.extended_skills_scroll_area) # Corrected
        main_layout.addWidget(extended_skills_group)

    def add_extended_skill_ui(self):
        skill_widget = SkillEntryWidget(self.extended_skills_layout)
        self.extended_skills_layout.addWidget(skill_widget)

    def get_data(self) -> dict:
        """
        Retrieves all data entered for the Extended Agent Card.
        Returns a dictionary containing name, description, version (which can be empty
        if inheriting from base card), and a list of additional skills.
        """
        skills_data = []
        # Iterate through dynamically added SkillEntryWidget instances
        for i in range(self.extended_skills_layout.count()):
            widget = self.extended_skills_layout.itemAt(i).widget()
            if isinstance(widget, SkillEntryWidget):
                skills_data.append(widget.get_data())

        return {
            "name": self.name_edit.text().strip(),
            "description": self.description_edit.toPlainText().strip(),
            "version": self.version_edit.text().strip(),
            "skills": skills_data,
        }


class ServerConfigWidget(QWidget):
    """
    A widget for configuring server-related settings, specifically for
    `DefaultRequestHandler` (Agent Executor, Task Store) and placeholders
    for `A2AStarletteApplication` references.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components for the Server Configuration tab."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- DefaultRequestHandler Configuration ---
        request_handler_group = QGroupBox("Request Handler Configuration (`DefaultRequestHandler`)")
        request_handler_layout = QFormLayout()
        request_handler_group.setLayout(request_handler_layout)

        self.agent_executor_edit = QLineEdit()
        self.agent_executor_edit.setPlaceholderText("e.g., MyAgentExecutor")
        request_handler_layout.addRow("Agent Executor Class Name (*):", self.agent_executor_edit) # Required

        self.task_store_combo = QComboBox()
        self.task_store_combo.addItems(["InMemoryTaskStore", "Custom"])
        request_handler_layout.addRow("Task Store:", self.task_store_combo)

        self.custom_task_store_edit = QLineEdit() # For custom task store class path
        self.custom_task_store_edit.setPlaceholderText("e.g., my_module.CustomTaskStore")
        self.custom_task_store_edit.setVisible(False) # Initially hidden
        # Show custom_task_store_edit only if "Custom" is selected in combo box
        request_handler_layout.addRow("Custom Task Store Class (* if Custom selected):", self.custom_task_store_edit)
        self.task_store_combo.currentTextChanged.connect(
            lambda text: self.custom_task_store_edit.setVisible(text == "Custom")
        )

        main_layout.addWidget(request_handler_group)

        # --- A2AStarletteApplication Configuration (Informational Placeholders) ---
        app_config_group = QGroupBox("Server Application Configuration (`A2AStarletteApplication`)")
        app_config_layout = QFormLayout()
        app_config_group.setLayout(app_config_layout)

        self.agent_card_ref_edit = QLineEdit()
        self.agent_card_ref_edit.setPlaceholderText("Handled by code generation")
        self.agent_card_ref_edit.setReadOnly(True)
        app_config_layout.addRow("Agent Card Reference:", self.agent_card_ref_edit)

        self.http_handler_ref_edit = QLineEdit()
        self.http_handler_ref_edit.setPlaceholderText("Handled by code generation")
        self.http_handler_ref_edit.setReadOnly(True)
        app_config_layout.addRow("HTTP Handler Reference:", self.http_handler_ref_edit)

        self.extended_agent_card_ref_edit = QLineEdit()
        self.extended_agent_card_ref_edit.setPlaceholderText("Handled by code generation")
        self.extended_agent_card_ref_edit.setReadOnly(True)
        app_config_layout.addRow("Extended Agent Card Reference:", self.extended_agent_card_ref_edit)

        main_layout.addWidget(app_config_group)
        main_layout.addStretch()

    def get_data(self) -> dict:
        """
        Retrieves server configuration data.
        Returns a dictionary with 'agent_executor_class_name' and 'task_store'
        (which could be a predefined option or a custom class path).
        """
        task_store_option = self.task_store_combo.currentText()
        if task_store_option == "Custom": # If custom, get the path from the dedicated QLineEdit
            task_store_val = self.custom_task_store_edit.text().strip()
        else:
            task_store_val = task_store_option
        return {
            "agent_executor_class_name": self.agent_executor_edit.text().strip(),
            "task_store": task_store_val,
        }


class RelationshipEntryWidget(QWidget):
    """
    A widget for entering the details of a single agent relationship (name and URL).
    Includes a button to remove itself.
    """
    def __init__(self, parent_layout: QVBoxLayout):
        super().__init__()
        self.parent_layout = parent_layout
        self.init_ui()

    def init_ui(self):
        """Initializes the UI for a single relationship entry."""
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.name_label = QLabel("Agent Name:")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g., Weather Agent")

        self.url_label = QLabel("Agent URL:")
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("e.g., http://localhost:8001/")

        self.remove_button = QPushButton("Remove Relationship")
        self.remove_button.clicked.connect(self.remove_self)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.remove_button)

    def remove_self(self):
        self.setParent(None)
        self.parent_layout.removeWidget(self)
        self.deleteLater()

    def get_data(self) -> dict:
        """
        Retrieves data for this relationship entry.
        Returns a dictionary with 'name' and 'url'.
        """
        return {
            "name": self.name_edit.text().strip(),
            "url": self.url_edit.text().strip(),
        }


class AgentRelationshipsWidget(QWidget):
    """
    A widget for managing a list of known agent relationships.
    Allows dynamic addition and removal of relationship entries.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initializes the UI for the Agent Relationships tab."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        group_box = QGroupBox("Known Agent Relationships")
        self.group_box_layout = QVBoxLayout() # Made self
        group_box.setLayout(self.group_box_layout)
        main_layout.addWidget(group_box)

        add_relationship_button = QPushButton("Add Relationship")
        add_relationship_button.clicked.connect(self.add_relationship_ui)
        self.group_box_layout.addWidget(add_relationship_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget_container = QWidget()
        self.relationships_layout = QVBoxLayout(self.scroll_widget_container)
        self.scroll_widget_container.setLayout(self.relationships_layout)
        self.scroll_area.setWidget(self.scroll_widget_container)

        self.group_box_layout.addWidget(self.scroll_area) # Corrected

    def add_relationship_ui(self):
        relationship_widget = RelationshipEntryWidget(self.relationships_layout)
        self.relationships_layout.addWidget(relationship_widget)

    def get_data(self) -> dict:
        """
        Retrieves all defined agent relationships.
        Returns a dictionary with a 'relationships' key, containing a list
        of relationship dictionaries (each with 'name' and 'url').
        """
        relationships_data = []
        # Iterate through dynamically added RelationshipEntryWidget instances
        for i in range(self.relationships_layout.count()):
            widget = self.relationships_layout.itemAt(i).widget()
            if isinstance(widget, RelationshipEntryWidget):
                relationships_data.append(widget.get_data())
        return {"relationships": relationships_data}


class MainWindow(QMainWindow):
    """
    The main application window for the A2A Agent Configuration GUI Tool.
    It hosts various configuration tabs and the code generation functionality.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initializes the main window UI, including tabs and buttons."""
        self.setWindowTitle("A2A Agent Configuration Tool")
        self.setGeometry(100, 100, 900, 750) # Adjusted window size

        # Central widget and main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_v_layout = QVBoxLayout(main_widget) # Main vertical layout for tabs and button

        self.tab_widget = QTabWidget() # Tab widget to hold different configuration sections
        self.main_v_layout.addWidget(self.tab_widget)

        # --- Create instances of the configuration tab widgets ---
        self.agent_card_widget = AgentCardWidget()
        self.extended_agent_card_widget = ExtendedAgentCardWidget()
        self.server_config_widget = ServerConfigWidget()
        self.agent_relationships_widget = AgentRelationshipsWidget()

        # Add config widgets as tabs
        self.tab_widget.addTab(self.agent_card_widget, "Agent Card")
        self.tab_widget.addTab(self.extended_agent_card_widget, "Extended Agent Card")
        self.tab_widget.addTab(self.server_config_widget, "Server Configuration")
        self.tab_widget.addTab(self.agent_relationships_widget, "Agent Relationships")

        # Generated Code Tab
        self.generated_code_text_edit = QTextEdit()
        self.generated_code_text_edit.setReadOnly(True)
        self.generated_code_text_edit.setFontFamily("Courier") # Monospaced font
        self.tab_widget.addTab(self.generated_code_text_edit, "Generated Code")

        # Generate Code Button
        self.generate_button = QPushButton("Generate Agent Code")
        self.generate_button.clicked.connect(self.handle_generate_code)
        self.main_v_layout.addWidget(self.generate_button) # Add button below the tab widget

    def handle_generate_code(self):
        """
        Handles the 'Generate Agent Code' button click.
        It retrieves data from all configuration tabs, performs validation,
        and if valid, generates the Python SDK code and displays it in the
        'Generated Code' tab.
        """
        # Retrieve data from all configuration widgets
        agent_card_data = self.agent_card_widget.get_data()
        extended_card_data = self.extended_agent_card_widget.get_data()
        server_data = self.server_config_widget.get_data()

        # --- Validation Checks ---
        if not agent_card_data['name']:
            QMessageBox.warning(self, "Validation Error", "Agent Card: Name is required.")
            return
        if not agent_card_data['url']:
            QMessageBox.warning(self, "Validation Error", "Agent Card: URL is required.")
            return

        # Validate skills in Agent Card
        for i, skill_data in enumerate(agent_card_data['skills']):
            if not skill_data['id']:
                QMessageBox.warning(self, "Validation Error", f"Agent Card - Skill #{i+1}: ID is required.")
                return
            if not skill_data['name']:
                QMessageBox.warning(self, "Validation Error", f"Agent Card - Skill #{i+1}: Name is required.")
                return

        # Validate skills in Extended Agent Card (if any)
        if extended_card_data['skills']:
            for i, skill_data in enumerate(extended_card_data['skills']):
                if not skill_data['id']:
                    QMessageBox.warning(self, "Validation Error", f"Extended Agent Card - Skill #{i+1}: ID is required.")
                    return
                if not skill_data['name']:
                    QMessageBox.warning(self, "Validation Error", f"Extended Agent Card - Skill #{i+1}: Name is required.")
                    return

        # Validate Server Configuration
        if not server_data['agent_executor_class_name']:
            QMessageBox.warning(self, "Validation Error", "Server Configuration: Agent Executor Class Name is required.")
            return

        # Validate custom task store path if "Custom" is selected
        if self.server_config_widget.task_store_combo.currentText() == "Custom" and not server_data['task_store']:
            QMessageBox.warning(self, "Validation Error", "Server Configuration: Custom Task Store Class is required when 'Custom' is selected.")
            return
        # --- End Validation Checks ---

        relationships_data = self.agent_relationships_widget.get_data() # Get relationships data after validation

        # --- Start Code Generation Logic ---
        code = []
        # Imports
        code.append("from a2a.sdk.public_api.agent import AgentCard, AgentSkill, AgentCapabilities, ExtendedAgentCard")
        code.append("from a2a.sdk.public_api.http import DefaultRequestHandler, A2AStarletteApplication")
        code.append("from a2a.sdk.public_api.task_store.memory import InMemoryTaskStore")

        # Dynamically add import for custom task store if specified
        task_store_path = server_data['task_store']
        if task_store_path != "InMemoryTaskStore" and task_store_path != "Custom" and "." in task_store_path:
            # Assumes path like 'my_module.MyCustomTaskStore'
            custom_task_store_module = task_store_path.rsplit('.', 1)[0]
            custom_task_store_class = task_store_path.rsplit('.', 1)[1]
            code.append(f"from {custom_task_store_module} import {custom_task_store_class}")
        # Note: If task_store_path is "Custom" but empty, validation would have caught it.
        # If it's "Custom" and filled, the above condition handles it.

        code.append("\n# --- Agent Capabilities Definition ---")
        code.append(f"agent_capabilities = AgentCapabilities(")
        code.append(f"    streaming={agent_card_data['capabilities']['streaming']},")
        code.append(f"    push_notifications={agent_card_data['capabilities']['pushNotifications']},")
        code.append(f")")

        code.append("\n# --- Main Agent Card Skills Definition ---")
        if agent_card_data['skills']:
            code.append("agent_skills = [")
            for skill in agent_card_data['skills']: # Loop through each skill's data
                code.append(f"    AgentSkill(")
                code.append(f"        id={format_single_string_for_code(skill['id'])},")
                code.append(f"        name={format_single_string_for_code(skill['name'])},")
                code.append(f"        description={format_single_string_for_code(skill['description'])},")
                code.append(f"        tags={skill['tags']},") # Already formatted as list string
                code.append(f"        examples={skill['examples']},") # Already formatted as list string
                code.append(f"    ),")
            code.append("]")
        else:
            code.append("agent_skills = []") # Empty list if no skills

        code.append("\n# --- Main Agent Card Definition ---")
        code.append(f"public_agent_card = AgentCard(")
        code.append(f"    name={format_single_string_for_code(agent_card_data['name'])},")
        code.append(f"    description={format_single_string_for_code(agent_card_data['description'])},")
        code.append(f"    url={format_single_string_for_code(agent_card_data['url'])},")
        code.append(f"    version={format_single_string_for_code(agent_card_data['version'])},")
        code.append(f"    default_input_modes={agent_card_data['defaultInputModes']},")
        code.append(f"    default_output_modes={agent_card_data['defaultOutputModes']},")
        code.append(f"    capabilities=agent_capabilities,")
        code.append(f"    skills=agent_skills,")
        code.append(f")")

        code.append("\n# --- Extended Agent Card Definition (if any overrides/additions) ---")
        extended_card_update_dict = {}
        # Populate update dictionary only with fields that have values
        if extended_card_data['name']:
            extended_card_update_dict['name'] = format_single_string_for_code(extended_card_data['name'])
        if extended_card_data['description']: # Description can be multi-line
            extended_card_update_dict['description'] = format_single_string_for_code(extended_card_data['description'])
        if extended_card_data['version']:
            extended_card_update_dict['version'] = format_single_string_for_code(extended_card_data['version'])

        update_str_parts = [f"{k}={v}" for k, v in extended_card_update_dict.items()]

        if extended_card_data['skills']: # If there are specific skills for the extended card
            code.append("extended_agent_skills = [") # Define them as a separate list
            for skill in extended_card_data['skills']:
                code.append(f"    AgentSkill(")
                code.append(f"        id={format_single_string_for_code(skill['id'])},")
                code.append(f"        name={format_single_string_for_code(skill['name'])},")
                code.append(f"        description={format_single_string_for_code(skill['description'])},")
                code.append(f"        tags={skill['tags']},")
                code.append(f"        examples={skill['examples']},")
                code.append(f"    ),")
            code.append("]")
            # Add these skills to the update dictionary for `from_agent_card`.
            # This assumes `ExtendedAgentCard.from_agent_card` (or its underlying `model_copy`)
            # can take 'skills' in the update dictionary to override/set them.
            update_str_parts.append("skills=extended_agent_skills")

        if update_str_parts: # If there's anything to update (attributes or skills)
            update_str = ", ".join(update_str_parts)
            # Uses from_agent_card with an update dictionary, standard for Pydantic models
            code.append(f"extended_public_agent_card = ExtendedAgentCard.from_agent_card(public_agent_card, {update_str})")
        else:
            # If no overrides or additional skills, it's essentially a copy or not needed.
            # For clarity, we'll set it to None if no specific extended features are defined.
            # Alternatively, could be `ExtendedAgentCard.from_agent_card(public_agent_card)` if an explicit copy is always desired.
            code.append("# No extended agent card attributes or skills defined to override/add.")
            code.append("extended_public_agent_card = None")

        code.append("\n# --- Request Handler Definition ---")
        task_store_val = server_data['task_store']
        task_store_instance_code = "None # Default or TODO: Specify Custom Task Store instance"
        if task_store_val == "InMemoryTaskStore":
            task_store_instance_code = "InMemoryTaskStore()"
        elif task_store_val != "Custom": # A specific custom path was provided
             # Assumes the custom task store class name is the last part of the path
            task_store_class_name = task_store_val.split('.')[-1]
            task_store_instance_code = f"{task_store_class_name}()"
        # If task_store_val is "Custom" but empty, validation should have caught it.
        # If it was "Custom" and filled, it's treated as a specific path above.

        agent_executor_class_name = server_data['agent_executor_class_name'] if server_data['agent_executor_class_name'] else "MyAgentExecutor"
        code.append(f"# TODO: Define your AgentExecutor class (e.g., {agent_executor_class_name})")
        code.append(f"http_handler = DefaultRequestHandler(")
        code.append(f"    agent_executor={agent_executor_class_name}(), # Assuming it's instantiated here")
        code.append(f"    task_store={task_store_instance_code},")
        code.append(f")")

        code.append("\n# --- Server Application Definition ---")
        code.append(f"app = A2AStarletteApplication(")
        code.append(f"    agent_card=public_agent_card,")
        code.append(f"    http_handler=http_handler,")
        code.append(f"    extended_agent_card=extended_public_agent_card, # Will be None if not defined")
        code.append(f")")

        code.append("\n# --- Defined Agent Relationships (Informational) ---")
        if relationships_data['relationships']:
            code.append("# {")
            for rel in relationships_data['relationships']:
                code.append(f"#    '{rel['name']}': '{rel['url']}',")
            code.append("# }")
        else:
            code.append("# No agent relationships defined.")

        # --- End Code Generation ---
        self.generated_code_text_edit.setPlainText("\n".join(code))
        self.tab_widget.setCurrentWidget(self.generated_code_text_edit) # Switch focus to the generated code tab
        # --- End Code Generation Logic ---


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
