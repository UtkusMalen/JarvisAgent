import subprocess
from typing import List, Tuple

class ProcessExecutor:
    """Handles process execution"""

    @staticmethod
    def run_detached(command: List[str]) -> bool:
        """
        Run a command detached from the parent process

        :param command: Command and arguments as list
        :return: True if success, False otherwise
        """
        try:
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True
        except (FileNotFoundError, PermissionError, OSError):
            return False

    @staticmethod
    def run_sync(command: str, timeout: int = 10) -> Tuple[bool, str]:
        """
        Run a shell command synchronously and capture output

        :param command: Shell command string
        :param timeout: Timeout in seconds
        :return: Tuple of (success, output)
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = result.stdout.strip() or result.stderr.strip()
            return result.returncode == 0, output or "Command executed"
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, f"Error: {str(e)}"