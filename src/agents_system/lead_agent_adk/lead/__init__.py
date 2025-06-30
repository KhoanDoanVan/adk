
from agent import LeadAgent
import asyncio

def _get_initialized_lead_agent_sync():
  """Synchronously creates and initializes the Lead Agent"""

  async def _async_main():
    # HARDCODED URLs for the role agents
    role_agent_urls = [
      "http://localhost:1001", # FLUTTER,
      "http://localhost:1002", # IOS,
      "http://localhost:1003" # ANDROID
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


lead_agent = _get_initialized_lead_agent_sync()