from fastapi import APIRouter, Path, Query
from agent import get_actions

router = APIRouter()


@router.get('/agent/{symbol}/actions')
def get_agent_actions(
        symbol: str = Path(..., title="Symbol name"),
        look_back: int = Query(..., title="Look back model parameter"),
        forward_days: int = Query(..., title="Forward days model parameter")):
    actions = get_actions(symbol, look_back, forward_days)
    return actions
