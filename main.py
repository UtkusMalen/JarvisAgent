import sys

from agent import JarvisAgent
from config import Config


class JarvisInterface:
    """Command-line interface for Jarvis"""

    def __init__(self, agent: JarvisAgent):
        self.agent = agent

    @staticmethod
    def print_welcome() -> None:
        print("=" * 60)
        print("Jarvis MCP Agent")
        print("=" * 60)
        print("Type your command. Examples:")
        print("  -  'open browser'")
        print("  -  'search for python tutorials'")
        print("  -  'what time is it?'")
        print("  -  'open my documents folder'")
        print("Type 'exit' or 'quit' to close\n")

    def run(self) -> None:
        """Run the main interaction loop"""
        self.print_welcome()

        while True:
            try:
                user_input = input("\n You> ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("Goodbye!")
                    break

                response = self.agent.process_command(user_input)
                print(f"\n Jarvis> {response}")

            except (KeyboardInterrupt, EOFError):
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\n Error: {str(e)}")

def main() -> None:
    """Main entry point"""
    try:
        config = Config.from_env()
        agent = JarvisAgent(config)
        interface = JarvisInterface(agent)
        interface.run()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
