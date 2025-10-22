from typing import Optional

from google.genai import types

from tools.base import BaseTool
from utils import ProcessExecutor

class BrowserTool(BaseTool):
    """Tool for browser operations"""

    def __init__(self):
        self.executor = ProcessExecutor()

    @property
    def name(self) -> str:
        return "open_browser"

    @property
    def description(self) -> str:
        return "Opens the web browser. Can optionally open a specific URL"

    def get_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "url": types.Schema(
                        type=types.Type.STRING,
                        description="Optional URL to open. If not provided, opens browser homepage"
                    )
                }
            )
        )

    def execute(self, url: Optional[str] = None) -> str:
        if url:
            if self.executor.run_detached(['xdg-open', url]):
                return f"Opening browser at {url}"
            return f"Failed to open browser at {url}"

        if self.executor.run_detached(['firefox']):
            return "Opening Firefox browser"
        return "Failed to open browser"

class WebSearchTool(BaseTool):
    """Tool for web searching"""

    def __init__(self):
        self.executor = ProcessExecutor()

    @property
    def name(self) -> str:
        return "search_web"

    @property
    def description(self) -> str:
        return "Opens browser and searches for the given query on Google"

    def get_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "query": types.Schema(
                        type=types.Type.STRING,
                        description="The search query"
                    )
                },
                required=["query"]
            )
        )

    def execute(self, query: str) -> str:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        if self.executor.run_detached(['xdg-open', url]):
            return f"Searching for: {query}"
        return f"Failed to search for: {query}"