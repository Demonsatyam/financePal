from agents.graph_builder import agent_graph
from google.adk.langgraph_tool import LangGraphTool

LangGraphTool(graph=agent_graph).serve(name="insurance_adjudicator")
