
import uvicorn
import logging
import os
from dotenv import load_dotenv
from a2a.types import (
  AgentCapabilities,
  AgentSkill,
  AgentCard
)
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from agent import create_agent
from agent_executor import ClackAgentExecutor



load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# MISSING API KEY ERROR
class MissingAPIKeyError(Exception):
  """Exception for missing API Key"""
  pass


# MAIN
def main():
  """Starts the agent server"""
  host = "localhost"
  port = 10001

  try:
    # Check for API Key only if Vertext AI is not configured
    if not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
      if not os.getenv("GOOGLE_API_KEY"):
        raise MissingAPIKeyError(
          "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not set to TRUE. Please set GOOGLE_API_KEY or set GOOGLE_GENAI_USE_VERTEXAI to TRUE."
        )
      
    capabilities = AgentCapabilities(streaming=True)

    skill = AgentSkill(
      id="check_skill",
      name="Check Clack's Flutter Development Skills",
      description="Checks Clack's skills for flutter development on a given skills.",
      tags=["flutter_code", "read_flutter_file"],
      examples=["Does Clack can to write the UI Flutter code?"]
    )

    agent_card = AgentCard(
      name="Clack Agent",
      description="An agent that develop Flutter Crossplatform",
      url=f"http://{host}:{port}/",
      version="1.0.0",
      defaultInputModes=["text/plain"],
      defaultOutputModes=["text/plain"],
      capabilities=capabilities,
      skills=[skill]
    )

    adk_agent = create_agent()

    runner = Runner(
      app_name=agent_card.name,
      agent=adk_agent,
      artifact_service=InMemoryArtifactService(),
      session_service=InMemorySessionService(),
      memory_service=InMemoryMemoryService()
    )

    agent_executor = ClackAgentExecutor(runner=runner)

    request_handler = DefaultRequestHandler(
      agent_executor=agent_executor,
      task_store=InMemoryTaskStore()
    )

    server = A2AStarletteApplication(
      http_handler=request_handler,
      agent_card=agent_card
    )

    uvicorn.run(server.build(), host=host, port=port)
    

  except MissingAPIKeyError as e:
    logger.error(f"Error: {e}")
    exit(1)
  except Exception as e:
    logger.error(f"An Error occurred during server startup: {e}")
    exit(1)




if __name__ == "__main__":
  main()
