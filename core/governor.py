import re
import json
import sqlite3
import hmac
import hashlib
from typing import List, Dict, Any
from datetime import datetime, timezone

class PersistentSovereignGovernor:
    def __init__(self, allowed_tools: List[str], db_path: str = "gateway_state.db", signing_key: str = "CHASSIS_SECRET"):
        self.allowed_tools = allowed_tools
        self.signing_key = signing_key.encode('utf-8')
        self.db_path = db_path
        self.expected_priors = ["select", "analytics", "read", "status", "fetch", "query"]
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_wallet (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    balance_sats INTEGER NOT NULL
                )
            """)
            cursor.execute("INSERT OR IGNORE INTO agent_wallet (id, balance_sats) VALUES (1, 1000)")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    tool TEXT NOT NULL,
                    cost_sats INTEGER,
                    free_energy REAL,
                    signature_snippet TEXT NOT NULL
                )
            """)
            conn.commit()

    def get_wallet_balance(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance_sats FROM agent_wallet WHERE id = 1")
            return cursor.fetchone()[0]

    def update_wallet_balance(self, new_balance: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE agent_wallet SET balance_sats = ? WHERE id = 1", (new_balance,))
            conn.commit()

    def log_event(self, event_type: str, tool: str, cost: int, fe: float, sig: str, timestamp: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO audit_trail (timestamp, event_type, tool, cost_sats, free_energy, signature_snippet)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, event_type, tool, cost, fe, sig))
            conn.commit()

    def evaluate_and_transact(self, tool_name: str, payload: str) -> Dict[str, Any]:
        if tool_name not in self.allowed_tools:
            raise PermissionError(f"Tool '{tool_name}' is unauthorized.")

        words = re.findall(r'\b\w+\b', payload.lower())
        matches = sum(1 for w in words if w in self.expected_priors)
        mismatch_ratio = 1.0 - (matches / max(1, len(words)))
        free_energy = max(0.5, (mismatch_ratio * 4.0) + (len(set(words)) * 0.1))

        if free_energy > 3.0:
            raise ValueError(f"Thermodynamic Block: Free Energy ({free_energy:.2f}) exceeded threshold.")

        cost_sats = 10 + int(free_energy * 20)
        current_balance = self.get_wallet_balance()
        if current_balance < cost_sats:
            raise RuntimeError(f"Insufficient funds: Requires {cost_sats} sats, balance is {current_balance}.")

        new_balance = current_balance - cost_sats
        self.update_wallet_balance(new_balance)

        timestamp = datetime.now(timezone.utc).isoformat()
        receipt_data = {
            "tool": tool_name,
            "free_energy": round(free_energy, 2),
            "cost_paid_sats": cost_sats,
            "remaining_balance": new_balance,
            "timestamp": timestamp
        }
        
        serialized = json.dumps(receipt_data, sort_keys=True).encode('utf-8')
        signature = hmac.new(self.signing_key, serialized, hashlib.sha256).hexdigest()

        self.log_event("SETTLEMENT", tool_name, cost_sats, round(free_energy, 2), signature[:16] + "...", timestamp)
        return {"receipt": receipt_data, "payment_signature": signature}
