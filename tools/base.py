from abc import ABC, abstractmethod
from google.genai import types

class BaseTool(ABC):
    """Abstract base class for all tools"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description"""
        pass

    @abstractmethod
    def get_function_declaration(self) -> types.FunctionDeclaration:
        """Get the function declaration for Gemini API"""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Execute the tool with given arguments"""
        pass