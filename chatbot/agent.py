from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from chatbot.schemas import CustomerSupportAgentState
from typing import Union, Any, List, Optional
from chatbot.exceptions import InvalidMessageHistory


class CustomerSupportAgent:
    def __init__(
            self,
            model: Union[ChatOpenAI, Any],
            tools: List[Tool],
            memory: Optional[MemorySaver] = None
            ) -> None:
        self.model = model
        self.tools = tools
        self.memory = memory

    def compile_agent(self) -> None:
        workflow = StateGraph(state_schema=CustomerSupportAgentState)

        self.model = self.model.bind_tools(self.tools)
        tool_node = ToolNode(self.tools)
        
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", tool_node)
        
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", self._should_continue,
                                       ["tools", END])
        workflow.add_edge("tools", "agent")
        
        self.agent = workflow.compile(checkpointer=self.memory)
 
    def _should_continue(self, state: CustomerSupportAgentState) -> CustomerSupportAgentState:
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return END

    def _call_model(self, state: CustomerSupportAgentState) -> CustomerSupportAgentState:
        message_history = state["messages"]
        if not message_history:
            raise InvalidMessageHistory("The message history was not initialized properly.")
        
        response = self.model.invoke(message_history)

        updated_message_history = message_history + [response]
        state["messages"] = updated_message_history
        return state
    
    def run(self, input_state: CustomerSupportAgentState, config: dict) -> CustomerSupportAgentState:
        return self.agent.invoke(input=input_state, config=config)