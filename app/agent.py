from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import MemorySaver
from app.common.schemas import Shirt
from app.tools.customer_support import log_support_request
from app.tools.faq import get_faq_info
from app.tools.order_customization import customize_order, check_order_status
from app.prompts import system_prompt
from app.common.utils import load_api_key, create_new_shirt
from uuid import uuid4


class State(AgentState):
    order: Shirt
    id: str

def create_agent_state() -> State:
    state = State()

    state["messages"] = []
    state["order"] = create_new_shirt()
    state["id"] = str(uuid4())
    return state

def build_tool_node(tools: list) -> ToolNode:
    tools = tools
    tool_node = ToolNode(tools)
    return tool_node

def initialize_model(api_key: str, tools: list, 
                        model="gpt-4o-mini", temperature=0) -> ChatOpenAI:
    model = ChatOpenAI(model=model,
                        temperature=temperature,
                        api_key=api_key).bind_tools(tools)
    return model

tools = [log_support_request, get_faq_info, customize_order, check_order_status]
tool_node = build_tool_node(tools)
model = initialize_model(api_key=load_api_key(), tools=tools)

class Agent:
    def __init__(self):
        self.agent = self._build_agent(tool_node)

    def _build_agent(self, tool_node: ToolNode) -> CompiledStateGraph:
        workflow = StateGraph(state_schema=State)
        
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", tool_node)
        
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent",
                                            self._should_continue,
                                            ["tools", END])
        workflow.add_edge("tools", "agent")
        
        memory = MemorySaver()
        agent = workflow.compile(checkpointer=memory)
        return agent
 
    def _should_continue(self, state: State):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    def _call_model(self, state: State):
        # Check if it's the first interaction; add an initial welcome message.
        if not state["messages"]:
            state["messages"].append(
                AIMessage(content=("Hi, I am the TeeCustomizer Ordering Assistant! Let's make your own customizable shirt! What color should it be?"))
                )
        
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = model.invoke(messages)
        return {"messages": state["messages"] + [response]}
    
    def run(self, input_state: dict, config: dict) -> dict:
        """
        Run the compiled agent with the given input state and configuration.
        The input_state should have at least a "messages" key.
        """
        return self.agent.invoke(input_state, config=config)