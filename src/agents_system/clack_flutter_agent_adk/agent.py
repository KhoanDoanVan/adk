
from google.adk.agents import LlmAgent
from sub_agents.reader_agent.agent import reader_agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

def get_skills() -> str:
  """
  Returns a list of essential skills for a Flutter Developer.
  """

  return """
  Flutter Developer Skills:
  - Dart programming language proficiency
  - Flutter SDK and widget system
  - State management (e.g., Provider, Riverpod, Bloc)
  - REST API integration and HTTP requests
  - Firebase services (Auth, Firestore, Messaging, Storage)
  - Git version control and GitHub collaboration
  - Responsive design for Android & iOS
  - Platform channels for native integration
  - Navigation and routing (Navigator 1.0 / 2.0)
  - Asynchronous programming with Future & Stream
  - Custom UI animations and transitions
  - Unit, widget, and integration testing
  - CI/CD tools (e.g., Codemagic, GitHub Actions)
  - Publishing apps to Google Play and App Store
  """

# CREATE AGENT
def create_agent() -> LlmAgent:
  """Constructs the ADK agent for Clack"""
  return LlmAgent(
    model="gemini-2.5-flash-preview-05-20",
    name="Clack_Agent",
    instruction="""
    You are **Clack's Personal Assistant** 🧑‍💻 for Flutter.  
    Your job is to help users with:
    - Viewing or analyzing Dart (Flutter) code
    - Listing developer skills

    ---

    ### 🧠 Core Responsibilities:

    1. **📚 Skill Listing**  
      - When the user asks what you know or can do, use the `get_skills` tool to list Flutter developer capabilities.

    2. **📂 Reading Dart Files**  
      - If a user says “show me” or “read” a Dart file, delegate to the `reader_agent`.

    ---

    ### 💬 Communication Style:
    - Be professional and technical.
    - Always keep answers concise.
    - Only respond to mobile development–related tasks. For unrelated topics, say:  
      _“I can only assist with Flutter development.”_

    ---

    ### 💡 Example Prompts You Should Handle:

    - “List all Flutter developer skills.”
    - “What’s inside `main.dart`?”

    Always use the correct tools and sub-agents, then return the result clearly.
    """,
    sub_agents=[reader_agent],
    tools=[get_skills],
  )