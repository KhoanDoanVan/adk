from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools.tool_context import ToolContext
from sub_agents.refactor_agent.agent import refactor_agent

def get_ios_skills() -> str:
  """
  Returns a list of essential skills for a native iOS Developer (Swift).
  """
  return """
  iOS Developer Skills:
  - Proficiency in Swift and SwiftUI
  - UIKit framework and Auto Layout
  - Combine framework for reactive programming
  - Core Data for local persistence
  - RESTful API integration (URLSession, Codable)
  - Firebase services (Authentication, Firestore, Messaging, Storage)
  - Git version control and GitHub/Bitbucket collaboration
  - App lifecycle and scene management
  - Async/Await and concurrency handling
  - Custom animations and gesture handling
  - Unit tests, UI tests, and XCTest framework
  - CoreLocation and MapKit
  - App Store publishing & TestFlight management
  - Dependency management (Swift Package Manager, CocoaPods)
  """

def create_agent() -> LlmAgent:
  """
  Constructs the ADK agent for Simon (iOS Personal Assistant)
  """
  return LlmAgent(
    model="gemini-2.5-flash-preview-05-20",
    name="Simon_Agent",
    instruction="""
    You are **Simon's Personal Assistant** 🧑‍💻 for iOS Development.

    You help Simon with:
    - Reviewing or refactoring Swift/iOS code
    - Listing essential iOS developer skills

    ---

    ### 📌 Capabilities:

    1. **🧠 List Skills**
        - When asked about your knowledge or skills, call `get_ios_skills()`.

    2. **🛠️ Refactor Swift Code**
        - If a prompt involves refactoring or analyzing Swift code, use `refactor_agent`.

    ---

    ### 💬 Style Guide:
    - Stay focused on iOS development (Swift/SwiftUI).
    - Answer in a concise and technical tone.
    - For off-topic queries, reply:  
      _“I can only assist with iOS development.”_

    ---
    """,
    sub_agents=[refactor_agent],
    tools=[get_ios_skills],
  )