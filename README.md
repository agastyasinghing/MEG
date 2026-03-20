# MEG — Megalodon Market Intelligence Engine

Real-time prediction market intelligence engine for Polymarket. Detects, scores, and surfaces trade signals from on-chain whale behavior — not blind copy-trading. Exploits the 4–12 hour window between whale entry and retail reaction.

## Architecture

```
Polygon RPC → Pre-Filter Gates → Signal Engine → Agent Core → Execution
                   ↓                   ↓               ↓
             Market Quality       Lead-Lag Score    Risk Gates
             Arb Exclusion        Kelly Sizing      Position Mgmt
             Intent Class.        Consensus Filter  Trap Detection
```

## Stack

Python 3.11 async · FastAPI · React/TypeScript · PostgreSQL · Redis · web3.py · Polymarket CLOB SDK

## Status

v1 paper trading. Full signal pipeline operational (phases 1–9). Dashboard in progress.
