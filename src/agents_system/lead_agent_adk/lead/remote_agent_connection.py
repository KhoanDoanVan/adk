
from dotenv import load_dotenv
from a2a.types import (
  AgentCard,
  SendMessageRequest,
  SendMessageResponse,
  Task,
  TaskArtifactUpdateEvent,
  TaskStatusUpdateEvent
)
from a2a.client import A2AClient
import httpx
from typing import Callable


load_dotenv()

TaskCallbackArg = Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent
TaskUpdateCallback = Callable[[TaskCallbackArg, AgentCard], Task]


# REMOTE AGENT CONNECTIONS
class RemoteAgentConnection:
  """
  A class to hold the connections to the remote agents
  """

  """
  INIT
  """
  def __init__(self, agent_card: AgentCard, agent_url: str):
    print(f"agent_card: {agent_card}")
    print(f"agent_url: {agent_url}")

    self._httpx_client = httpx.AsyncClient(timeout=30)
    self.agent_client = A2AClient(
      httpx_client=self._httpx_client,
      agent_card=agent_card,
      url=agent_url
    )
    self.card = agent_card
    self.conversation_name = None
    self.conversation = None
    self.pending_tasks = set()

  """
  GET AGENT CARD
  """
  def get_agent(self) -> AgentCard:
    return self.card
  

  """
  SEND MESSAGE
  """
  async def send_message(self, message_request: SendMessageRequest) -> SendMessageResponse:
    return await self.agent_client.send_message(message_request)








