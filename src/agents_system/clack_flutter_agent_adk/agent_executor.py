
import logging
from collections.abc import AsyncGenerator
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from google.adk.runners import Runner
from google.adk.events import Event
from google.genai import types
from a2a.server.tasks import TaskUpdater
from a2a.server.events.event_queue import EventQueue
from a2a.utils.errors import ServerError
from utils import (
  convert_a2a_parts_to_genai,
  convert_genai_parts_to_a2a
)
from a2a.types import (
  TaskState,
  UnsupportedOperationError
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# CLACK AGENT EXECUTOR
class ClackAgentExecutor(AgentExecutor):
  """An Agent Executor that runs Clack's ADK-based Agent"""

  def __init__(self, runner: Runner):
    self.runner = runner
    self.__running_sessions = {}


  # RUN
  def _run_agent(
      self, session_id, new_message: types.Content
  ) -> AsyncGenerator[Event, None]:
    
    return self.runner.run_async(
      session_id=session_id,
      user_id="clack_agent",
      new_message=new_message
    )
  
  # PROCESS
  async def _process_request(
      self,
      new_message: types.Content,
      session_id: str,
      task_updater: TaskUpdater
  ) -> None:
    
    session_obj = await self._upsert_session(session_id)
    session_id = session_obj.id

    async for event in self._run_agent(session_id=session_id, new_message=new_message):

      if event.is_final_response():
        parts = convert_genai_parts_to_a2a(
          event.content.parts if event.content and event.content.parts else []
        )
        logger.debug("Yielding update response: %s", parts)
        await task_updater.add_artifact(parts=parts)
        await task_updater.complete()
        break

      if not event.get_function_calls():
        logger.debug("Yielding update response")
        await task_updater.update_status(
          TaskState.working,
          message=task_updater.new_agent_message(
            convert_genai_parts_to_a2a(
              event.content.parts
              if event.content and event.content.parts
              else []
            )
          )
        )
      else:
        logger.debug("Skipping event")



  # EXECUTE
  async def execute(
      self,
      context: RequestContext,
      event_queue: EventQueue
  ):
    if not context.task_id or not context.context_id:
      raise ValueError("RequestContext must have task_id and context_id")
    if not context.message:
      raise ValueError("RequestContext must have a message")
    

    updater = TaskUpdater(
      event_queue,
      context.task_id,
      context.context_id
    )

    if not context.current_task:
      await updater.submit()

    await updater.start_work()

    await self._process_request(
      types.UserContent(
        parts=convert_a2a_parts_to_genai(context.message.parts)
      ),
      context.context_id,
      updater
    )
    

  # CANCEL
  async def cancel(self, context: RequestContext, event_queue: EventQueue):
    raise ServerError(
      error=UnsupportedOperationError()
    )
  

  # UPSERT (UPDATE OR CREATE NEW)
  async def _upsert_session(self, session_id: str):

    session = await self.runner.session_service.get_session(
      app_name=self.runner.app_name,
      user_id="clack_agent",
      session_id=session_id
    )

    if session is None:
      session = await self.runner.session_service.create_session(
        app_name=self.runner.app_name,
        user_id="clack_agent",
        session_id=session_id
      )

    if session is None:
      raise RuntimeError(f"Failed to get or create session: {session_id}")
    
    return session

