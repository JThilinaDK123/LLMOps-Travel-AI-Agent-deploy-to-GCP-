from crewai import Agent, Task, Crew, LLM
from datetime import datetime
from dotenv import load_dotenv
import requests
import os
from tavily import TavilyClient
from crewai.tools import tool

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool("tavily_search_tool")
def tavily_search_tool(query: str):
    """
    Search for real-time information such as hotels, flights,
    weather, and currency using Tavily Search API.
    """
    result = tavily.search(query=query, max_results=1)
    return result


def run_travel_planner(country, current_time=None):

    if current_time is None:
        current_time = datetime.now()

    ## Initialize LLM
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=400,
        stream=False,
    )

    ## Agent 1 — Accommodation Finder
    stay_agent = Agent(
        role="Accommodation Finder",
        goal=(
            f"Return a list of top 10 accommodations (hotels) in {country}. "
            "Do not include prices."
        ),
        backstory=(
            "You provide accurate accommodation names for travelers. No prices or summaries.  Do NOT include thoughts, reasoning steps, or explanations."
        ),
        llm=llm,
        verbose=False
    )

    ## Agent 2 — Temperature Checker
    weather_agent = Agent(
        role="Weather Reporter",
        goal=(
            f"Return the current temperature in Celsius for {country} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}."
        ),
        backstory=(
            "You fetch the latest temperature using a weather API. Only return the number + unit.  Do NOT include thoughts, reasoning steps, or explanations. "
        ),
        tools=[tavily_search_tool], 
        llm=llm,
        verbose=False
    )

    ## Agent 3 — Airlines Finder
    airlines_agent = Agent(
        role="Airlines Expert",
        goal=(
            f"Return a list of 10 frequently travel airlines that operate flights to {country} as of {current_time.strftime('%Y-%m-%d %H:%M:%S')}."
        ),
        backstory=(
            "You provide airline names only. No flight prices, schedules, or summaries.  Do NOT include thoughts, reasoning steps, or explanations. "
        ),
        llm=llm,
        verbose=False
    )

    ## Agent 4 — Local Attractions Finder
    attractions_agent = Agent(
        role="Local Attractions Expert",
        goal=(
            f"Return a list of top 10 tourist attractions in {country}."
        ),
        backstory=(
            "You provide a concise list of popular tourist attractions or must-see places. No descriptions or rankings.  Do NOT include thoughts, reasoning steps, or explanations. "
        ),
        llm=llm,
        verbose=False
    )

    ## Agent 5 — Currency & Exchange Rate Checker
    currency_agent = Agent(
        role="Currency Expert",
        goal=(
            f"Return the list of current exchange rate against USD, GBP, EURO, INR of {country}"
        ),
        backstory=(
            "Provide only the currency name/code and exchange rate number. Do NOT include thoughts, reasoning steps, or explanations. "
        ),
        tools=[tavily_search_tool], 
        llm=llm,
        verbose=False
    )

    ## Tasks
    stay_task = Task(
        description=f"List hotels in {country}.",
        expected_output="Markdown list of accommodation names only.  Do not include thoughts or reasoning.",
        agent=stay_agent,
        output_file="output/Stays.md"
    )

    temp_task = Task(
        description=f"Return the current temperature in {country} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}.",
        expected_output="Single line: temperature in Celsius (In 5 main cities in Markdown list).  Do not include thoughts or reasoning.",
        agent=weather_agent,
        output_file="output/Temperature.md"
    )

    airlines_task = Task(
        description=f"List airlines flying to {country} as of {current_time.strftime('%Y-%m-%d %H:%M:%S')}.",
        expected_output="Markdown list of airline names.  Do not include thoughts or reasoning.",
        agent=airlines_agent,
        output_file="output/Airlines.md"
    )

    attractions_task = Task(
        description=f"List top tourist attractions in {country}.",
        expected_output="Markdown list of attractions.  Do not include thoughts or reasoning.",
        agent=attractions_agent,
        output_file="output/Attractions.md"
    )

    currency_task = Task(
        description=f"Provide the currency and exchange rate of {country} against USD, GBP, EURO, INR",
        expected_output="Markdown list of Currency code and rate only.  Do not include thoughts or reasoning.",
        agent=currency_agent,
        output_file="output/Currency.md"
    )

    ## Crew
    crew = Crew(
        agents=[stay_agent, weather_agent, airlines_agent, attractions_agent, currency_agent],
        tasks=[stay_task, temp_task, airlines_task, attractions_task, currency_task],
        verbose=False
    )

    inputs = {"country": country, "current_time": current_time.strftime('%Y-%m-%d %H:%M:%S')}
    crew.kickoff(inputs=inputs)

    ## Read reports
    reports = {}
    for file in ["output/Stays.md", "output/Temperature.md", "output/Airlines.md", 
                 "output/Attractions.md", "output/Currency.md"]:
        with open(file, "r") as f:
            reports[file.split('/')[-1]] = f.read()

    return reports
