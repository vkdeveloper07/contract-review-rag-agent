from langgraph.graph import END, START, StateGraph

from contract_review.agent import nodes
from contract_review.agent.state import AgentState


def build_graph(collection):
    graph = StateGraph(AgentState)
    graph.add_node("input_guard", nodes.input_guard_node)
    graph.add_node("rewrite_query", nodes.rewrite_query_node)
    graph.add_node("retrieve", lambda state: nodes.retrieve_node(state, collection))
    graph.add_node("build_context", nodes.build_context_node)
    graph.add_node("generate", nodes.generate_node)
    graph.add_node("output_guard", nodes.output_guard_node)
    graph.add_node("refuse", nodes.refuse_node)
    graph.add_edge(START, "input_guard")
    graph.add_conditional_edges("input_guard", nodes.route_after_input, {"continue": "rewrite_query", "refuse": "refuse"})
    graph.add_edge("rewrite_query", "retrieve")
    graph.add_edge("retrieve", "build_context")
    graph.add_edge("build_context", "generate")
    graph.add_edge("generate", "output_guard")
    graph.add_conditional_edges("output_guard", nodes.route_after_output, {"end": END, "refuse": "refuse"})
    graph.add_edge("refuse", END)
    return graph.compile()
