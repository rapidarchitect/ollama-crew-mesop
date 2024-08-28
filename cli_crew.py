from crewai import Agent, Task, Crew
from langchain_community.chat_models.ollama import ChatOllama
import os

# Set the OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = "NA"

# Initialize the language model (LLM) using the ChatOllama model hosted locally
llm = ChatOllama(model="llama3.1", base_url="http://localhost:11434")

# Define the prompt for the task
prompt = "benefits of using using the SOLID pattern in python"

# Create a Tech Writer agent responsible for writing the blog post
general_agent = Agent(
    role="Tech Writer",
    backstory="""You are a tech writer who is capable of writing
                tech blog post in depth.
              """,
    goal="Write and iterate a high quality blog post.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Create a Tech Researcher agent responsible for gathering relevant information
researcher = Agent(
    role="Tech Researcher",
    backstory="""You are a professional researcher for many technical topics.
                You are good at gathering keywords, key points and trends of
                the given topic
              """,
    goal="list keywords, key points and trend about for the given topic",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Define a task for the researcher to list key knowledge and trends for the topic
task = Task(
    description=f"""list keywords, key points,trends
                    for the following topic: {prompt}.
                    """,
    agent=researcher,
    expected_output="Keywords, Key Points and Trends.",
)

# Define a task for the Tech Writer to write the blog post based on the research outcomes
task2 = Task(
    description=f"""Based on the given research outcomes,
                    write a blog post of {prompt}.
                    """,
    agent=general_agent,
    expected_output="an article that is no more then 250 words",
)

# Create a Crew with both agents and tasks, and initiate the workflow
crew = Crew(agents=[general_agent, researcher], tasks=[task, task2], verbose=True)

# Execute the tasks and retrieve the result
result = crew.kickoff()

# Print the final result
print(result)
