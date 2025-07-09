

from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext
import os



def read_flutter_file(dart_file_name: str, tool_context: ToolContext) -> dict:
  """
  Reads the contents of a Flutter (Dart) file and returns it as a dictionary.
  
  Args:
    file_path (str): Path to the Dart file. Defaults to '../docs/main.dart'.
  
  Returns:
    dict: A dictionary with filename and its contents.
  """

  if not os.path.exists(f"/Volumes/MacDrive_Ex/Code/MultiAgents/adk_system/src/agents_system/clack_flutter_agent_adk/sub_agents/reader_agent/docs/{dart_file_name}"):
    return {
      "error": f"File not found: {dart_file_name}"
    }

  try:
    with open(f"/Volumes/MacDrive_Ex/Code/MultiAgents/adk_system/src/agents_system/clack_flutter_agent_adk/sub_agents/reader_agent/docs/{dart_file_name}", "r", encoding="utf-8") as f:
      content = f.read()

    data = {
      "file": f"/Volumes/MacDrive_Ex/Code/MultiAgents/adk_system/src/agents_system/clack_flutter_agent_adk/sub_agents/reader_agent/docs/{dart_file_name}",
      "content": content
    }


    tool_context.state["flutter_file_data"] = content

    return data
  
  except Exception as e:
    return {
      "error": str(e)
    }


reader_agent = LlmAgent(
  name="reader_agent",
  model="gemini-2.5-flash-preview-05-20",
  description="Reader agent to extract and display Flutter (Dart) file contents.",
  instruction="""
  You are the Reader Agent for an AI Mobile Developer assistant.

  Your job is to read and return the contents of a specified Dart file used in a Flutter project.
  You use the tool `read_flutter_file` to open and extract content from the file.
  The tool requires a name of file `dart_file_name`

  Expect the file name to be provided via `dart_file_name` in your tool context state.
  If the file is not found, return a helpful error message.
  """,
  tools=[read_flutter_file],
  output_key="flutter_file_data"
)