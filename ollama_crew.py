from crewai import Crew, Process, Agent, Task
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict
import mesop as me
import mesop.labs as mel

llm = ChatOpenAI(
    model="llama3.1", openai_api_key="NA", base_url="http://localhost:11434/v1"
)


class MyCustomHandler(BaseCallbackHandler):
    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        state = me.state(State)
        state.agent_messages.append(f"## Assistant: \r{inputs['input']}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        state = me.state(State)
        state.agent_messages.append(f"## {self.agent_name}: \r{outputs['output']}")


writer = Agent(
    role="Tech Writer",
    backstory="""You are a tech writer who is capable of writing
                tech blog post in depth.
              """,
    goal="Write and iterate a high quality blog post.",
    llm=llm,
    verbose=False,
    allow_delegation=False,
    callbacks=[MyCustomHandler("Writer")],
)
researcher = Agent(
    role="Tech Researcher",
    backstory="""You are a professional researcher for many technical topics.
                You are good at gathering keywords, key points and trends of
                the given topic
              """,
    goal="list keywords, key points and trend about for the given topic",
    llm=llm,
    verbose=False,
    allow_delegation=False,
    callbacks=[MyCustomHandler("Researcher")],
)


def StartCrew(prompt):
    task1 = Task(
        description=f"""list keywords, key points,trends
                        for the following topic: {prompt}.
                        """,
        agent=researcher,
        expected_output="Keywords, Key Points and Trends.",
    )
    task2 = Task(
        description=f"""Based on the given research outcomes,
                        write a blog post of {prompt}.
                        """,
        agent=writer,
        expected_output="an article that is no more then 250 words",
    )

    project_crew = Crew(
        tasks=[task1, task2],
        agents=[researcher, writer],
        manager_llm=llm,
        process=Process.sequential,
    )

    result = project_crew.kickoff()

    return result


@me.stateclass
class State:
    agent_messages: list[str]


_DEFAULT_BORDER = me.Border.all(me.BorderSide(color="#e0e0e0", width=1, style="solid"))
_BOX_STYLE = me.Style(
    display="grid",
    border=_DEFAULT_BORDER,
    padding=me.Padding.all(15),
    overflow_y="scroll",
    box_shadow=("0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"),
)


@me.page(
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io"]
    ),
    path="/",
    title="Ollama with CrewAI on Mesop",
)
def app():
    state = me.state(State)
    with me.box():
        mel.text_to_text(
            StartCrew,
            title="Ollama Blog Generator",
        )
    with me.box(style=_BOX_STYLE):
        me.text(text="Crew Execution..", type="headline-6")
        for message in state.agent_messages:
            with me.box(style=_BOX_STYLE):
                me.markdown(message)
