import sys
import asyncio
import argparse
from dotenv import load_dotenv
from agents import Runner, trace
from research_agents.agents import seo_expert_agent, research_agent, reporter_agent

load_dotenv()


async def main():
    parser = argparse.ArgumentParser("AI Topic Researcher")
    parser.add_argument(
        "-t", "--topic", type=str, required=True, help="The topic to research"
    )
    args = parser.parse_args()
    topic = args.topic

    try:
        with trace("Research Workflow"):
            print("\n[1/3] Running SEO Expert Agent...")
            seo_results = await Runner.run(seo_expert_agent, topic)

            print("SEO Expert Agent finished execution")

            print("\n[2/3] Running Research Agent...")
            research_results = await Runner.run(
                research_agent, seo_results.final_output
            )

            print("Research Agent finished execution")

            print("\n[3/3] Running Reporter Agent...")
            await Runner.run(reporter_agent, research_results.final_output)

            print("Reporter Agent finished execution")
            print("\n Process completed successfully!\n")
            sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
