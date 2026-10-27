import httpx

class SovereignAgentSDK:
    def __init__(self, gateway_url: str = "http://127.0.0.1:8004"):
        self.url = gateway_url

    def invoke_tool(self, tool_name: str, payload: str):
        with httpx.Client() as client:
            resp = client.post(f"{self.url}/chassis/execute", json={"tool_name": tool_name, "payload": payload})
            return resp.status_code, resp.json()
