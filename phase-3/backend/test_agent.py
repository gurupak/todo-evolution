import asyncio
import os
from todo_api.config import settings
from todo_api.agent.todo_agent import todo_agent
from agents import Runner

os.environ["OPENAI_API_KEY"] = settings.openai_api_key

async def test():
    try:
        result = await Runner.run(
            todo_agent,
            [{"role": "user", "content": "hello"}],
            context={"user_id": "test123"}
        )
        print("SUCCESS:", result.final_output)
    except Exception as e:
        print("ERROR:", type(e).__name__, str(e))
        import traceback
        traceback.print_exc()

asyncio.run(test())
