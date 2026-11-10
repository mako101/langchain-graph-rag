from typing import Literal

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from pprint import pprint
from datetime import date

load_dotenv()

job_search_platforms = [
    "Indeed",
    "LinkedIn",
    "reed.co.uk",
    "totaljobs.com",
    "cv-library.co.uk",
    "www.jobserve.com",
]

class Source(BaseModel):
    name: str = Field(description="The name of the source")
    url: str = Field(description="The url of the source")


class JobListing(BaseModel):
    title: str = Field(description="The title of the job listing")
    company: str | None = Field(description="The company of the job listing")
    location: str | None = Field(description="The location of the job listing")
    job_type: Literal["Permanent", "Contract", "Unspecified"] | None = Field(
        description="The type of the job listing"
    )
    description: str = Field(description="The description of the job listing")
    salary: str | None = Field(description="""The salary of the job listing. This can be annual, hourly, daily, or unspecified""")
    currency: Literal["USD", "EUR", "GBP", "Unspecified"] | None= Field(
        description="The currency of the salary")
    source: Source = Field(description="The source of the job listing")
    date_posted: str | None  = Field(description="The date the job listing was posted")


class AgentResponse(BaseModel):
    job_listings: list[JobListing] = Field(description="The job listings found")

agent = create_agent(
    model="openai:gpt-6-luna",
    tools=[TavilySearch()],
    response_format=AgentResponse,
    system_prompt="""
    You are a job search assistant. 
    You are given a job search query and you need to search the web for the best job for the user.
    When returning structured data, use 'Unspecified' for any field that is not provided.
    """,
).with_config(run_name="tavily-job-search-agent-structured-output")


# Run the agent
response = agent.invoke(
    {"messages": [HumanMessage(
        content=f"""
        Search the following job platforms:
        {", ".join(job_search_platforms)}
        for software engineer jobs in UK, 
        posted within a month of {date.today()}, 
        that require LangChain as a skill.
        Retun up to 5 job listings.
        """)]}
)

# response_text = response['messages'][-1].content[0]['text']
# print(f"\n{response_text}\n")

job_listings = response['structured_response'].job_listings
pprint(job_listings)