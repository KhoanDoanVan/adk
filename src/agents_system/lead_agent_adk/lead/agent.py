
from datetime import datetime
from dotenv import load_dotenv
import nest_asyncio
from .remote_agent_connection import RemoteAgentConnection
from a2a.types import (
  AgentCard,
  SendMessageRequest,
  SendMessageResponse,
  MessageSendParams,
  SendMessageSuccessResponse,
  Task
)
from a2a.client import (
  A2ACardResolver
)
from google.adk import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.tools.tool_context import ToolContext
from typing import (List)
import httpx
import json
import uuid
import asyncio


load_dotenv()

nest_asyncio.apply()


# LEAD AGENT
class LeadAgent:
  """The Lead Agent"""

  """
  INIT
  """
  def __init__(self):
    self._remote_agent_connections: dict[str, RemoteAgentConnection] = {}
    self.cards: dict[str, AgentCard] = {}
    self.agents: str = ""
    self._agent = self.create_lead_agent()
    self._user_id = "lead_agent"
    self._runner = Runner(
      app_name=self._agent.name,
      agent=self._agent,
      artifact_service=InMemoryArtifactService(),
      session_service=InMemorySessionService(),
      memory_service=InMemoryMemoryService()
    )


  """
  ASYNCHRONOUSLY INITIALIZED COMPONENTS
  """
  async def _async_init_components(self, remote_agent_addresses: List[str]):
    async with httpx.AsyncClient(timeout=30) as client:
      for address in remote_agent_addresses:

        card_resolver = A2ACardResolver(client, address)
        try:
          card = await card_resolver.get_agent_card()
          remote_connection = RemoteAgentConnection(
            agent_card=card,
            agent_url=address
          )
          self._remote_agent_connections[card.name] = remote_connection
          self.cards[card.name] = card
        except httpx.ConnectError as e:
          print(f"ERROR: Failed to get agent card from {address}: {e}")
        except Exception as e:
          print(f"ERROR: Failed to initialized connection for {address}: {e}")

    agent_info = [
      json.dumps(
        {
          "name": card.name,
          "description": card.description
        }
      )
      for card in self.cards.values()
    ]

    print("agent_info", agent_info)
    self.agents = "\n".join(agent_info) if agent_info else "No Agents Available"


  @classmethod
  async def create(
    cls,
    remote_agent_addresses: List[str]
  ):
    instance = cls()
    await instance._async_init_components(remote_agent_addresses=remote_agent_addresses)
    return instance


  """
  CREATE LEAD AGENT
  """
  def create_lead_agent(self) -> Agent:
    return Agent(
      model="gemini-2.5-flash-preview-05-20",
      name="Lead_Agent",
      instruction=self.lead_instructions,
      description="This Lead Agent orchestrates mobile team",
      tools=[self.send_message],
      output_key="data_conversation"
    )


  """
  LEAD INSTRUCTIONS
  """
  def lead_instructions(self, context: ReadonlyContext) -> str:
    return f"""
    **Role:** You are the Lead Agent, an expert mobile development for hifpt application. Your primary function is to coordinate with role agents to find a suitable to handle mobile issues.
    
    **Core Directives:**

    * **Get Skill of Agents:** When asked to get skills of agent, then use the `send_message` tool to ask that agents for get skill of their
      *   Make sure you pass in the official name of the role agent for each message request.
    * **Convert Code:** When asked to convert code, then use the `send_message` tool to ask propriate agent
    * **Readability:** Make sure to respond in a concise and easy to read format (bullet points are good).

    **Today's Date (YYYY-MM-DD):** {datetime.now().strftime("%Y-%m-%d")}

    <Available Agents>
    {self.agents}
    </Available Agents>
    """
  


  """
  SEND MESSAGE
  """
  async def send_message(self, agent_name: str, task: str, tool_context: ToolContext):
    """
    Send a task to a remote role agent
    """

    if agent_name not in self._remote_agent_connections:
      raise ValueError(f"Agent {agent_name} not found")
    
    client = self._remote_agent_connections[agent_name]

    if not client:
      raise ValueError(f"Client not available for {agent_name}")
    
    # Simplified task and context ID management
    state = tool_context.state
    task_id = state.get("task_id", str(uuid.uuid4()))
    context_id = state.get("context_id", str(uuid.uuid4()))
    message_id = str(uuid.uuid4())

    payload = {
      "message": {
        "role": "user",
        "parts": [
          {
            "type": "text",
            "text": task
          }
        ],
        "messageId": message_id,
        "taskId": task_id,
        "contextId": context_id
      }
    }

    message_request = SendMessageRequest(id=message_id, params=MessageSendParams.model_validate(payload))

    send_response: SendMessageResponse = await client.send_message(message_request=message_request)
    print("send_response:", send_response)


    if not isinstance(
      send_response.root,
      SendMessageSuccessResponse
    ) or not isinstance(send_response.root.result, Task):
      print("received a non-success or non-task response. Cannot procced.")
      return
    

    response_content = send_response.root.model_dump_json(exclude_none=True)
    json_content = json.loads(response_content)

    resp = []

    if json_content.get("result", {}).get("artifacts"):
      for artifact in json_content["result"]["artifacts"]:
        if artifact.get("parts"):
          resp.extend(artifact["parts"])

    return resp





def _get_initialized_lead_agent_sync():
  """Synchronously creates and initializes the Lead Agent"""

  async def _async_main():
    # HARDCODED URLs for the role agents
    role_agent_urls = [
      "http://localhost:10001", # FLUTTER,
      "http://localhost:10002", # IOS,
      "http://localhost:10003" # ANDROID
    ]

    print("Initializing Lead Agent...")
    lead_agent_instance = await LeadAgent.create(
      remote_agent_addresses=role_agent_urls
    )

    print("Lead Agent initialized successfully!!!")
    return lead_agent_instance.create_lead_agent()
  
  try:
    return asyncio.run(_async_main())
  except RuntimeError as e:
    if "asyncio.run() cannot be called from a running event loop" in str(e):
      print(
        f"Warning: Could not initialized LeadAgent with asyncio.run(): {e}"
        "This can happen if an event loop is already running (e.g., in Jupyter)"
        "Consider initializing LeadAgent within an async function in your application"
      )
    else:
      raise


root_agent = _get_initialized_lead_agent_sync()



