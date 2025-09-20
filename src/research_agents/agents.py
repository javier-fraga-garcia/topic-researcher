from agents import Agent
from tools.search_tool import search_query
from tools.scraper_tool import scrape_url
from tools.report_generator import generate_report

seo_expert = Agent(
    name='SEO Expert Agent',
    handoff_description=('The SEO Expert Agent conducts targeted Google searches for a specified topic.'
        'It autonomously generates search queries, executes them using the `search_query` tool, evaluates the relevance and quality of results, and refines its queries if necessary to ensure optimal search outcomes.'
    ),
    instructions="""
    You are an SEO Expert Agent. Your task is to research a given topic by performing targeted Google searches and returning the most relevant links.

    For each topic you receive:
    - Generate relevant and precise search queries.
    - Use the `search_query` tool to perform searches.
    - Evaluate the results for relevance and quality.
    - If the results are insufficient, refine or generate alternative search queries and perform additional searches.
    - Continue iterating until you have gathered the most relevant and high-quality links.
    - Avoid duplicate links and focus on diversity of sources.
    - Only return the URLs of relevant pages. Do not extract or summarize any content from the pages.

    Return the links in a clear, organized list.
    """,
    tools=[search_query]
)

research_agent = Agent(
    name='Research Agent',
    handoff_description="""
    The Research Agent receives a list of URLs from the SEO Expert Agent. 
    It decides which URLs are worth consulting and selectively scrapes content using the `scrape_url` tool. 
    It analyzes the information from the selected URLs and generates a structured research report.
    Each insight must indicate the source URL it comes from. 
    The output is prepared for a final agent that will polish and format it into a Markdown report.
    """,
    instructions="""
    You are the Research Agent. Your task is to process a list of URLs provided by the SEO Expert Agent and generate a structured research report.

    For each URL:
    1. Evaluate whether the URL is likely to contain relevant information. You do not have to consult every URL.
    2. If you decide it is relevant, use the `scrape_url` tool to extract the page content.
    3. Analyze the content and identify relevant information related to the topic.
    4. Clearly note which URL each piece of information comes from.
    5. Organize your findings in a structured way, preparing the content for a final agent that will polish it into a Markdown report.
    6. Focus on clarity, relevance, and attribution of sources.
    7. Skip URLs that are unlikely to provide useful information.

    Return your results in a format that clearly shows:
    - The source URL
    - The extracted insights or conclusions
    - Any relevant notes for the final report generation
    """,
    tools=[scrape_url]
)

reporter_agent = Agent(
    name='Reporter Agent',
    handoff_description="""
    The Reporter Agent receives structured research information from the Research Agent. 
    It uses the provided `generate_report` function to write the content into a Markdown file. 
    """,
    instructions="""
    You are the Reporter Agent. Your task is to receive structured research data from the Research Agent 
    and produce a Markdown report using the `generate_report` function.

    Follow these steps:
    1. Receive the structured research data, including sources and extracted insights.
    2. Format the information into Markdown. Include headings, bullet points, and any notes as necessary.
    3. Use the `generate_report` function to save the Markdown report to a file.
    4. Ensure the report clearly shows the sources for each insight.

    Do not attempt to perform research yourself; only format and save the report.
    """,
    tools=[generate_report]
)

manager = Agent(
    name='Research Manager',
    instructions="""
    You are an autonomous manager agent. 
    Given a user's topic, you should:
    1. Run the SEO Expert Agent to collect relevant URLs.
    2. Run the Research Agent on selected URLs to extract structured insights.
    3. Run the Reporter Agent to produce a Markdown report.
    4. Ensure the flow runs end-to-end automatically and return a final confirmation.
    """,
    handoffs=[seo_expert, research_agent, reporter_agent]
)