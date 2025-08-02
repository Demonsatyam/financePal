from fastapi import APIRouter, HTTPException # ✅ FIXED: Added HTTPException to the import
from pydantic import BaseModel
from agents.graph_builder import agent_graph
from fastapi.responses import StreamingResponse
import json

router = APIRouter()

class ClaimQueryRequest(BaseModel):
    user_id: str
    query: str

@router.post("/claims/check-eligibility", summary="Adjudicate a claim using a LangGraph workflow")
async def check_claim_eligibility(request: ClaimQueryRequest):
    """
    Accepts a user ID and a natural language query, and uses a multi-agent
    system to determine claim eligibility. The final step's output is returned.
    """
    if not request.user_id or not request.query:
        raise HTTPException(status_code=400, detail="user_id and query fields are required.")

    # The input for the graph must match the state dictionary structure
    inputs = {"user_id": request.user_id, "query": request.query}
    
    # Invoke the graph and get the final state
    # .invoke() runs the whole graph and returns just the final output
    final_state = agent_graph.invoke(inputs)

    # Return the final decision from the state, checking for an error key first
    if "error" in final_state:
        # Check if the error came from our explicit error_handler node
        if "final_decision" in final_state and "reasoning" in final_state["final_decision"]:
             raise HTTPException(status_code=500, detail=final_state["final_decision"]["reasoning"])
        else:
            raise HTTPException(status_code=500, detail=str(final_state.get("error", "An unknown error occurred during graph execution.")))

    return final_state.get("final_decision", {"error": "Graph finished without a decision."})