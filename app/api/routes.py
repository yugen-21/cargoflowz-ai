from fastapi import APIRouter, Query, Body, HTTPException
from typing import List, Dict, Any
from app.services.matcher import get_contacts_by_location
from app.services.mistral_ranking import get_top_response_ids

router = APIRouter()

@router.get("/match", summary="Get matching contacts by location")
def match_contacts(location: str = Query(..., description="Location to match against CSV")):
    results = get_contacts_by_location(location)
    return results


@router.post("/rank-top5", response_model=List[int])
async def rank_top_5_responses(
    responses: List[Dict[str, Any]] = Body(..., description="List of freight response JSON objects")
):
    try:
        if not isinstance(responses, list):
            raise ValueError("Expected a list of response objects")

        top_ids: List[int] = get_top_response_ids(responses)

        # ✅ Ensure it's only a list of integers
        if not all(isinstance(i, int) for i in top_ids):
            raise ValueError("Invalid format returned by Mistral — expected list of integers")

        return top_ids

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
