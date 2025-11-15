from crewai import Agent, Task, Crew, LLM

def run_travel_planner(country, current_year):
    # Initialize LLM
    llm = LLM(
        model="groq/llama-3.1-8b-instant",
        temperature=0.5,
        max_completion_tokens=1024,
        stream=False  # Stream False for Flask to return complete result
    )

    # Define agents
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

    # Define tasks
    budget_task = Task(
        description=f'Conduct detailed research about traveling in {country}. Focus on budget-friendly options including cheap accommodations, public transport, low-cost food, and free/low-price attractions. Make sure suggestions match the current year: {current_year}.',
        expected_output=f"A list with 5 bullet points outlining the most relevant and helpful budget travel insights for {country}. No code block markers ('```').",
        agent=budget_travel_agent,
        output_file="output/Budget Stay.md"
    )

    intermediate_task = Task(
        description='Review the budget research and expand each bullet point into a full, well-structured mid-range travel section. Provide balanced recommendations, including 3-star hotels, comfortable transport, and a mix of activities.',
        expected_output="A complete markdown-formatted travel report with full sections based on the 5 insights. No code block markers ('```').",
        agent=intermediate_travel_agent,
        output_file="output/Mid Stay.md",
        dependencies=[budget_task]
    )

    luxury_task = Task(
        description='Review all previous context and create an expanded luxury version of the travel plan. Include high-end stays, premium experiences, exclusive activities, fine dining options, and private transport recommendations.',
        expected_output="A luxury travel report in markdown format, with fully detailed sections for premium travelers. No code block markers ('```').",
        agent=luxury_travel_agent,
        output_file="output/Luxury Stay.md",
        dependencies=[intermediate_task, budget_task]
    )

    # Initialize crew
    crew = Crew(
        agents=[budget_travel_agent, intermediate_travel_agent, luxury_travel_agent],
        tasks=[budget_task, intermediate_task, luxury_task],
        verbose=False
    )

    inputs = {"country": country, "current_year": current_year}
    result = crew.kickoff(inputs=inputs)

    # Read all outputs
    reports = {}
    for file in ["output/Budget Stay.md", "output/Mid Stay.md", "output/Luxury Stay.md"]:
        with open(file, "r") as f:
            reports[file.split('/')[-1]] = f.read()
    
    return reports
