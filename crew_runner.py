from crewai import Agent, Task, Crew, LLM

def run_travel_planner(country, current_year):
    
    ## Initialize LLM
    llm = LLM(
        model="groq/llama-3.1-8b-instant",
        temperature=0.5,
        max_completion_tokens=1024,
        stream=True
    )

    budget_travel_agent = Agent(
        role='Budget-Friendly Travel Planning Expert',
        goal='Create cost-effective itineraries, cheap stays, public transport options based on the given country.',
        backstory='A travel expert specialized in budget trips.',
        llm=llm,
        verbose=False
    )

    intermediate_travel_agent = Agent(
        role='Mid-Range Travel Planner',
        goal='Provide a comfortable itinerary with balanced cost and comfort.',
        backstory='A seasoned traveler designing efficient itineraries.',
        llm=llm,
        verbose=False
    )

    luxury_travel_agent = Agent(
        role='Luxury Travel Concierge',
        goal='Design high-end, premium travel itineraries.',
        backstory='A luxury concierge specializing in premium experiences.',
        llm=llm,
        verbose=False
    )

    budget_task = Task(
        description=f'Conduct detailed research about traveling in {country} in the year {current_year}. **Create a complete, standalone markdown travel report** focused on budget-friendly options, including cheap hostels/guesthouses, public transport routes, low-cost street food/markets, and free/low-price attractions. The report must be a detailed guide for a budget traveler.',
        expected_output="A **complete markdown-formatted travel report** for budget travelers in 3-5 sections (e.g., Accommodation, Transport, Food, Activities). Do not use code block markers ('```').",
        agent=budget_travel_agent,
        output_file="output/Budget Stay.md",
        dependencies=[]
    )

    intermediate_task = Task(
        description=f'Conduct detailed research about traveling in {country} in the year {current_year}. **Create a complete, standalone markdown travel report** focused on mid-range options, including 3-star hotels, comfortable transport (trains, domestic flights), a mix of local restaurants and mid-range dining, and popular paid attractions. The report must be a detailed guide for a mid-range traveler.',
        expected_output="A **complete markdown-formatted travel report** for mid-range travelers in 3-5 sections (e.g., Accommodation, Transport, Food, Activities). Do not use code block markers ('```').",
        agent=intermediate_travel_agent,
        output_file="output/Mid Stay.md",
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
        agents=[budget_travel_agent, intermediate_travel_agent, luxury_travel_agent],
        tasks=[budget_task, intermediate_task, luxury_task],
        verbose=False
    )

    inputs = {"country": country, "current_year": current_year}
    result = crew.kickoff(inputs=inputs)

    reports = {}
    for file in ["output/Budget Stay.md", "output/Mid Stay.md", "output/Luxury Stay.md"]:
        with open(file, "r") as f:
            reports[file.split('/')[-1]] = f.read()
    
    return reports