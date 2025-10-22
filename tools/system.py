import os
from datetime import datetime
from typing import Optional

from google.genai import types

from tools.base import BaseTool
from utils import ProcessExecutor


class TerminalTool(BaseTool):
    """Tool for terminal operations"""

    def __init__(self):
        self.executor = ProcessExecutor()

    @property
    def name(self) -> str:
        return "open_terminal"

    @property
    def description(self) -> str:
        return "Opens a new Konsole terminal window. Can optionally execute a command in it"

    def get_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "command": types.Schema(
                        type=types.Type.STRING,
                        description="Optional command to execute in the terminal (e.g., 'neofetch', 'htop', 'python3'"
                    )
                }
            )
        )

    def execute(self, command: Optional[str] = None) -> str:
        if command:
            if self.executor.run_detached(['konsole', '-e', 'bash', '-c', f'{command}; exec bash']):
                return f"Opening Konsole terminal and running: {command}"
            return "Failed to open terminal"

        if self.executor.run_detached(['konsole']):
            return "Opening Konsole terminal"
        return "Failed to open terminal"

class CalculatorTool(BaseTool):
    """Tool for calculator operations"""

    def __init__(self):
        self.executor = ProcessExecutor()

    @property
    def name(self) -> str:
        return "open_calculator"

    @property
    def description(self) -> str:
        return "Opens a KCalc calculator app"

    def get_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(type=types.Type.OBJECT, properties={})
        )

    def execute(self) -> str:
        if self.executor.run_detached(['kcalc']):
            return "Opening KCalc calculator"
        return "Failed to open calculator"

class SystemMonitorTool(BaseTool):
    """Tool for system monitor operations"""

    def __init__(self):
        self.executor = ProcessExecutor()

    @property
    def name(self) -> str:
        return "open_system_monitor"

    @property
    def description(self) -> str:
        return "Opens the system monitor to view CPU, memory and process information"

    def get_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(type=types.Type.OBJECT, properties={})
        )

    def execute(self) -> str:
        if self.executor.run_detached(['plasma-systemmonitor']):
            return "Opening system monitor"
        if self.executor.run_detached(['ksysguard']):
            return "Opening system monitor"
        return "Failed to open system monitor"

class ShellCommandTool(BaseTool):
    """Tool for executing shell commands"""

    def __init__(self, timeout: int = 10):
        self.executor = ProcessExecutor()
        self.timeout = timeout

    @property
    def name(self) -> str:
        return "execute_shell_command"

    @property
    def description(self) -> str:
        return "Executes a shell command. Use carefully and only for safe operations"

    def get_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "command": types.Schema(
                        type=types.Type.STRING,
                        description="The shell command to execute"
                    )
                },
                required=["command"]
            )
        )

    def execute(self, command) -> str:
        success, output = self.executor.run_sync(command, self.timeout)
        return output

class SystemInfoTool(BaseTool):
    """Tool getting system information"""

    @property
    def name(self) -> str:
        return "get_system_info"

    @property
    def description(self) -> str:
        return "Gets system information like date, time, username or hostname"

    def get_function_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "info_type": types.Schema(
                        type=types.Type.STRING,
                        description="Type of info: 'time', 'date', 'username', 'hostname', 'all'"
                    )
                },
                required=["info_type"]
            )
        )

    def execute(self, info_type: str) -> str:
        info_map = {
            "time": lambda: datetime.now().strftime("%H:%M:%S"),
            "date": lambda: datetime.now().strftime("%Y-%m-%d"),
            "username": lambda: os.environ.get("USER", "unknown"),
            "hostname": lambda: os.uname().nodename,
            "all": lambda: (
                f"Time: {datetime.now().strftime('%H:%M:%S')}, "
                f"Date: {datetime.now().strftime('%Y-%m-%d')}, "
                f"User: {os.environ.get('USER', 'unknown')}, "
                f"Host: {os.uname().nodename}"
            )
        }

        handler = info_map.get(info_type)
        if handler:
            try:
                return handler()
            except Exception as e:
                return f"Error getting system info: {str(e)}"
        return f"Unknown info type: {info_type}"