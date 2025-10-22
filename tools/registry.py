from typing import Dict, List
from google.genai import types
from .base import BaseTool
from .browser import BrowserTool, WebSearchTool
from .file_system import FileManagerTool, TextEditorTool
from .system import (
    TerminalTool, CalculatorTool, SystemMonitorTool,
    ShellCommandTool, SystemInfoTool
)

class ToolRegistry:
    """Registry for managing and accessing tools"""

    def __init__(self, command_timeout: int = 10):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools(command_timeout)

    def _register_default_tools(self, timeout: int) -> None:
        """Register all default tools"""
        default_tools = [
            BrowserTool(),
            WebSearchTool(),
            FileManagerTool(),
            TextEditorTool(),
            TerminalTool(),
            CalculatorTool(),
            SystemMonitorTool(),
            ShellCommandTool(timeout),
            SystemInfoTool()
        ]

        for tool in default_tools:
            self.register(tool)

    def register(self, tool: BaseTool) -> None:
        """Register a tool"""
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        """Get a tool by name"""
        return self._tools.get(name)

    def get_function_declarations(self) -> List[types.FunctionDeclaration]:
        """Get all function declarations for Gemini API"""
        return [tool.get_function_declaration() for tool in self._tools.values()]

    def execute(self, name: str, **kwargs) -> str:
        """Execute a tool by name"""
        tool = self.get(name)
        if not tool:
            return f"Unknown tool: {name}"
        return tool.execute(**kwargs)

