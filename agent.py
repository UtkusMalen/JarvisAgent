from google import genai
from google.genai import types

from config import Config
from tools.registry import ToolRegistry


class JarvisAgent:
    """Main agent for processing command using Gemini"""

    def __init__(self, config: Config):
        self.config = config
        self.client = genai.Client(api_key=config.api_key)
        self.tool_registry = ToolRegistry(config.command_timeout)

    def _create_tools(self) -> list:
        """Create tools configuration for Gemini"""
        return [types.Tool(
            function_declarations=self.tool_registry.get_function_declarations()
        )]

    def process_command(self, user_input: str) -> str:
        """
        Process user command using gemini
        :param user_input: User's natural language command
        :return: Agent's response
        """
        try:
            # Generate initial response
            response = self.client.models.generate_content(
                model=self.config.model_name,
                contents=user_input,
                config=types.GenerateContentConfig(
                    tools=self._create_tools(),
                    system_instruction=self.config.system_instruction
                )
            )

            return self._handle_response(user_input, response)

        except Exception as e:
            return f"Error processing command: {str(e)}"

    def _handle_response(self, user_input: str, response) -> str:
        """Handle Gemini's response and execute functions if needed"""
        if not response.candidates or not response.candidates[0].content.parts:
            return "I'm not sure how to help with that"

        for part in response.candidates[0].content.parts:
            # Handle function calls
            if hasattr(part, 'function_call') and part.function_call:
                return self._handle_function_call(user_input, response, part.function_call)

            # Handle text response
            if hasattr(part, 'text') and part.text:
                return part.text

        return "I'm not sure how to help with that"

    def _handle_function_call(self, user_input: str, initial_response, func_call) -> str:
        """Execute function and get final response from Gemini"""
        func_name = func_call.name
        func_args = dict(func_call.args)

        print(f"[Executing: {func_name}({func_args})]")

        # Execute the function
        result = self.tool_registry.execute(func_name, **func_args)

        # Send function result back to model
        try:
            response = self.client.models.generate_content(
                model=self.config.model_name,
                contents=[
                    user_input,
                    initial_response.candidates[0].content,
                    types.Content(
                        parts=[types.Part(
                            function_response=types.FunctionResponse(
                                name=func_name,
                                response={"result": result}
                            )
                        )]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=self.config.system_instruction
                )
            )

            return response.text

        except Exception as e:
            return f"Error getting final response: {str(e)}"