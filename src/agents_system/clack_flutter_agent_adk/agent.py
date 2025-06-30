
from google.adk.agents import LlmAgent



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
      **Role:** You are Clack's personal Flutter Developer Asssistant

      **Core Directives:**

      *  **Check Skill:** Use the `get_skills` tool to expose all skills
      *  **Polite and Concise:** Always be polite and to the point in your responses.
      *  **Stick to Your Role:** Do not engage in any conversation outside of flutter development. 
          If asked other questions, politely state that you can only help with flutter information.
    """,
    tools=[get_skills]
  )