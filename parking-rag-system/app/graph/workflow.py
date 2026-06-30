from langgraph.graph import (
    StateGraph,
    END
)

from app.graph.graph_state import (
    ParkingGraphState
)

from app.graph.graph_nodes import (

    user_node,

    reservation_node,

    approval_node,

    mcp_node,

    storage_node
)


workflow = StateGraph(
    ParkingGraphState
)


workflow.add_node(
    "user",
    user_node
)

workflow.add_node(
    "reservation",
    reservation_node
)

workflow.add_node(
    "approval",
    approval_node
)

workflow.add_node(
    "mcp",
    mcp_node
)

workflow.add_node(
    "storage",
    storage_node
)


workflow.set_entry_point(
    "user"
)

workflow.add_edge(
    "user",
    "reservation"
)

workflow.add_edge(
    "reservation",
    "approval"
)

def route_after_approval(
    state
):

    if (
        state["status"]
        == "approved"
    ):

        return "mcp"

    return END

workflow.add_conditional_edges(
    "approval",
    route_after_approval
)

workflow.add_edge(
    "mcp",
    "storage"
)

workflow.add_edge(
    "storage",
    END
)


graph = workflow.compile()