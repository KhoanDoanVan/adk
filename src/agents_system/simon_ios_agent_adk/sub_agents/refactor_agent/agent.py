


from google.adk.agents import LlmAgent




refactor_agent = LlmAgent(
  name="reader_agent",
  model="gemini-2.5-flash-preview-05-20",
  description="Reader agent to extract and display Flutter (Dart) file contents.",
  instruction="""
  You are the Refactor Agent for an AI Mobile Developer assistant.

  Your job is to receive flutter code and refactor that flutter code to iOS code(Swift Language)

  If haven't received any Flutter code, then return error message
  """,
  output_key="ios_file_data"
)