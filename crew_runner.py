from crewai import Agent, Task, Crew, LLM
# from crewai_tools import TavilySearchTool
import os

def run_travel_planner(country, current_year):
    
    ## Initialize LLM
    llm = LLM(
        model="groq/llama-3.1-8b-instant",
        temperature=0.5,
        max_completion_tokens=1024,
        stream=True
    )

    # tavily_tool = TavilySearchTool(
    #     api_key = os.environ.get("TAVILY_API_KEY"),
    #     include_answer = True,
    #     max_results = 5
    # )

    budget_travel_agent = Agent(
        role='Budget-Friendly Travel Planning Expert',
        goal='Create cost-effective itineraries, cheap stays, public transport options based on the given country.',
        backstory='A travel expert specialized in budget trips.',
        llm=llm,
        # tools=[tavily_tool],
        verbose=False
    )

    luxury_travel_agent = Agent(
        role='Luxury Travel Concierge',
        goal='Design high-end, premium travel itineraries.',
        backstory='A luxury concierge specializing in premium experiences.',
        llm=llm,
        # tools=[tavily_tool],
        verbose=False
    )

    budget_task = Task(
        description=f'Conduct detailed research about traveling in {country} in the year {current_year}. **Create a complete, standalone markdown travel report** focused on budget-friendly options, including cheap hostels/guesthouses, public transport routes, low-cost street food/markets, and free/low-price attractions. The report must be a detailed guide for a budget traveler.',
        expected_output="A **complete markdown-formatted travel report** for budget travelers in 3-5 sections (e.g., Accommodation, Transport, Food, Activities). Do not use code block markers ('```').",
        agent=budget_travel_agent,
        output_file="output/Budget Stay.md",
        dependencies=[]
    )

    luxury_task = Task(
        description=f'Conduct detailed research about traveling in {country} in the year {current_year}. **Create a complete, standalone markdown travel report** focused on luxury options, including 5-star hotels/resorts, private transport (car services, private flights), fine dining, and exclusive/premium activities and tours. The report must be a detailed guide for a luxury traveler.',
        expected_output="A **complete markdown-formatted travel report** for luxury travelers in 3-5 sections (e.g., Accommodation, Transport, Food, Activities). Do not use code block markers ('```').",
        agent=luxury_travel_agent,
        output_file="output/Luxury Stay.md",
        dependencies=[]
    )

    crew = Crew(
        agents=[budget_travel_agent, luxury_travel_agent],
        tasks=[budget_task, luxury_task],
        verbose=False
    )

    inputs = {"country": country, "current_year": current_year}
    result = crew.kickoff(inputs=inputs)

    reports = {}
    for file in ["output/Budget Stay.md",  "output/Luxury Stay.md"]:
        with open(file, "r") as f:
            reports[file.split('/')[-1]] = f.read()
    
    return reports