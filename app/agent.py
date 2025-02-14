from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import MemorySaver
from app.common.schemas import Shirt
from app.tools import get_faq_info, customize_order, log_support_request
from app.prompts import system_prompt
from app.common.utils import load_api_key


class State(AgentState):
    order: Shirt


class Agent:
    def __init__(self):
        self.api_key = load_api_key()
        
        self.tools = [customize_order, get_faq_info, log_support_request]
        self.tool_node = ToolNode(self.tools)
        
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(self.tools)
        
        self.workflow = StateGraph(state_schema=State)
        
        self.workflow.add_node("agent", self.call_model)
        self.workflow.add_node("tools", self.tool_node)
        
        self.workflow.add_edge(START, "agent")
        self.workflow.add_conditional_edges("agent", self.should_continue, ["tools", END])
        self.workflow.add_edge("tools", "agent")
        
        self.memory = MemorySaver()
        
        self.agent = self.workflow.compile(checkpointer=self.memory)
    
    def should_continue(self, state: State):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    def call_model(self, state: State):
        # Check if it's the first interaction; add an initial welcome message.
        if not state["messages"]:
            state["messages"].append(
                AIMessage(content="Hi, I am the TeeCustomizer Ordering Assistant! Let's make your own customizable shirt! What color should it be?")
            )
        
        # Add the system prompt and the existing conversation messages.
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        
        # Call the language model.
        response = self.model.invoke(messages)
        
        # Return the updated state with the response message.
        return {"messages": state["messages"] + [response]}
    
    def run(self, input_state: dict, config: dict) -> dict:
        """
        Run the compiled agent with the given input state and configuration.
        The input_state should have at least a "messages" key.
        """
        return self.agent.invoke(input_state, config=config)