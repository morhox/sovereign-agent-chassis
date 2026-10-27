# Sovereign Agent Chassis (SAC)

> **Deterministic Governance, Thermodynamic Regulation, and Cryptographic Settlement for Autonomous AI Agents.**

## The Problem
Modern AI agents are built on probabilistic foundations and given keys to APIs, execution environments, and financial wallets without intrinsic safety guardrails. When an agent enters a hallucination loop, it risks runaway execution, cascading errors, and catastrophic resource depletion. 

## The Solution: Sovereign Engineering
The **Sovereign Agent Chassis** introduces a closed-loop infrastructure layer that treats agents as untrusted economic actors:
1. **Deterministic Firewalls:** Strict policy enforcement before any tool execution.
2. **Thermodynamic Regulation (Active Inference):** Measuring semantic entropy in real-time. If uncertainty spikes, the system dynamically restricts actions or scales costs.
3. **Cryptographic Mesh:** Every action, state change, and settlement is cryptographically signed (HMAC-SHA256) for zero-trust multi-agent environments.
4. **Economic Accountability:** Integrated micro-payment simulation (L402-ready) enforcing solvency—agents pay for the computational and cognitive energy they consume.

## Architecture
- **Governor Core:** Evaluates inputs, calculates free energy, and manages persistence.
- **Sidecar Gateway:** FastAPI-based proxy handling secure middleware intercepts.
- **Agent SDK:** Lightweight wrapper integrating seamlessly into frameworks like LangChain, CrewAI, or custom loops.

## Quickstart (Local Development)
1. Clone the repository:
   ```bash
   git clone [https://github.com/morhox/sovereign-agent-chassis.git](https://github.com/morhox/sovereign-agent-chassis.git)
   cd sovereign-agent-chassis
2. Run the gateway server:
```bash
uvicorn gateway.server:app --reload --port 8004

