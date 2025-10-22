from typing import Optional

from google.genai import types

from tools.base import BaseTool
from utils import ProcessExecutor

class FileManagerTool(BaseTool):
    """Tool for file manager operations"""

    def __init__(self):
        self.executor = ProcessExecutor()

    @property
    def name(self) -> str:
        return "open_file_manager"

    @property
    def description(self) -> str:
        return "Opens the Dolphin file manager. Can optionally open a specific dir"

    def get_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "path": types.Schema(
                        type=types.Type.STRING,
                        description="Optional directory path to open. Defaults to home dir"
                    )
                }
            )
        )

    def execute(self, path: Optional[str] = None) -> str:
        command = ['dolphin', path] if path else ['dolphin']
        if self.executor.run_detached(command):
            return f"Opening file manager{' at ' + path if path else ''}"
        return "Failed to open file manager"

class TextEditorTool(BaseTool):
    """Tool for text editor operations"""

    def __init__(self):
        self.executor = ProcessExecutor()

    @property
    def name(self) -> str:
        return "open_text_editor"

    @property
    def description(self) -> str:
        return "Opens Kate text editor. Can optionally open a specific file"

    def get_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Optional file path to open in editor"
                    )
                }
            )
        )

    def execute(self, file_path: Optional[str] = None) -> str:
        command = ['kate', file_path] if file_path else ['kate']
        if self.executor.run_detached(command):
            return f"Opening Kate editor{' with ' + file_path if file_path else ''}"
        return "Failed to open text editor"