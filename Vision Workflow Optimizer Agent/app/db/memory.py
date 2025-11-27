from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

# In a production app, you would replace these with SQLite/Postgres implementations
# that inherit from the abstract base classes provided by the SDK.
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

async def get_services():
    return session_service, memory_service