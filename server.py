from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sovereign_chassis.core.governor import PersistentSovereignGovernor

app = FastAPI(title="Sovereign Chassis Gateway", version="5.0.0")
governor = PersistentSovereignGovernor(allowed_tools=["db_query", "metrics_fetch"])

class ActionRequest(BaseModel):
    tool_name: str
    payload: str

@app.post("/chassis/execute")
async def execute_action(req: ActionRequest):
    try:
        result = governor.evaluate_and_transact(req.tool_name, req.payload)
        return {"status": "CHASSIS_SETTLED", "settlement": result}
    except PermissionError as p:
        raise HTTPException(status_code=403, detail=str(p))
    except ValueError as v:
        raise HTTPException(status_code=422, detail=str(v))
    except RuntimeError as r:
        raise HTTPException(status_code=402, detail=str(r))

@app.get("/chassis/wallet")
def get_wallet():
    return {"balance_sats": governor.get_wallet_balance()}
