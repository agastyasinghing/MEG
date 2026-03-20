# MEG (Megalodon)
A real-time prediction market intelligence engine that tracks on-chain whale activity to generate scored trade signals on Polymarket.
# What It Does
MEG monitors the Polygon blockchain for large wallet trades, scores them through a multi-layer signal pipeline, and surfaces ranked trade proposals for human approval, combining on-chain data, statistical modeling, and risk management into a semi-autonomous trading system (complete autonomy in future update)
# Architecture
Polygon RPC → Pre-Filter Gates → Signal Engine → Agent Core → Execution

                    ↓                   ↓              ↓
                    
              Market Quality      Lead-Lag Score   Risk Gates
              
              Arb Exclusion       Kelly Sizing     Position Mgmt
              
              Intent Class.      Consensus Filter  Trap Detection
              
                                    + more           + more


# Signal Pipeline

Data Layer: Polygon RPC websocket feed, Polymarket CLOB client, wallet registry with reputation tracking

Pre-Filter (3 gates): market quality, arbitrage exclusion, intent classification

Signal Engine: 9 modules producing composite scores via lead-lag analysis, Kelly criterion sizing, consensus filtering, and contrarian detection

Agent Core:  risk gates, position management, trap detection, saturation monitoring

Execution: paper/live order routing with slippage guards and entry distance checks

# Status
Currently live in paper trading. Full v1 pipeline operational.

Signal architecture incorporates algorithms including information half-life modeling, proprietary decay functions not included in this repository.

v1.5, 2, 3 scoped out.
