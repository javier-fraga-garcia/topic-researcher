import sys
import asyncio
from dotenv import load_dotenv
from agents import Runner
from research_agents.agents import manager

load_dotenv()


async def main():
    try:
        result = await Runner.run(manager, 'Quiero saber más sobre la soberanía tecnlógica europea')
        print(result.final_output)
    except Exception as e:
        print(2)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
