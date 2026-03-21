import { useRef } from 'react'
import { Canvas } from '@react-three/fiber'
import { ScrollControls } from '@react-three/drei'
import Scene from './Scene'
import './App.css'

// ── Seeded pseudo-random — deterministic mock, no snapshot flakiness ─────────

function seededRand(seed) {
  let s = seed >>> 0
  return () => {
    s = (Math.imul(1664525, s) + 1013904223) >>> 0
    return s / 0xffffffff
  }
}

// ── Mock data — shapes match MEG PRD §13 API contracts ──────────────────────

const MOCK = {
  approvalQueue: [
    {
      market_id: 'MKT-0441',
      outcome: 'YES',
      composite_score: 0.78,
      suggested_size_usdc: 150,
      trap_warning: false,
    },
    {
      market_id: 'MKT-0389',
      outcome: 'NO',
      composite_score: 0.62,
      suggested_size_usdc: 80,
      trap_warning: true,
    },
    {
      market_id: 'MKT-0512',
      outcome: 'YES',
      composite_score: 0.71,
      suggested_size_usdc: 120,
      trap_warning: false,
    },
  ],
  signalFeed: [
    {
      signal_id: 'SIG-0441',
      market_id: 'MKT-0441',
      composite_score: 0.78,
      status: 'QUALIFIED',
      fired_at: '2026-03-20T14:22:00Z',
    },
    {
      signal_id: 'SIG-0440',
      market_id: 'MKT-0387',
      composite_score: 0.55,
      status: 'FILTERED',
      fired_at: '2026-03-20T14:18:00Z',
    },
    {
      signal_id: 'SIG-0439',
      market_id: 'MKT-0389',
      composite_score: 0.62,
      status: 'QUALIFIED',
      fired_at: '2026-03-20T14:10:00Z',
    },
    {
      signal_id: 'SIG-0438',
      market_id: 'MKT-0201',
      composite_score: 0.43,
      status: 'FILTERED',
      fired_at: '2026-03-20T13:55:00Z',
    },
  ],
  systemStatus: {
    is_paused: false,
    paper_trading: true,
    last_block_processed: 68234891,
    daily_pnl_usdc: 47.32,
  },
  positions: [
    {
      market_id: 'MKT-0441',
      outcome: 'YES',
      entry_price: 0.52,
      current_price: 0.61,
      unrealized_pnl_pct: 17.3,
    },
    {
      market_id: 'MKT-0389',
      outcome: 'NO',
      entry_price: 0.38,
      current_price: 0.35,
      unrealized_pnl_pct: -7.9,
    },
  ],
  pnlHistory: (() => {
    const rand = seededRand(42)
    let v = 0
    return Array.from({ length: 30 }, () => {
      v += (rand() - 0.46) * 15
      return parseFloat(v.toFixed(2))
    })
  })(),
}

// ── SVG P&L line chart — no chart libraries ──────────────────────────────────

function PnLChart({ data }) {
  const W = 280
  const H = 80
  const PAD = 4
  const min = Math.min(...data)
  const max = Math.max(...data)
  const range = max - min || 1

  const pts = data.map((v, i) => ({
    x: PAD + (i / (data.length - 1)) * (W - PAD * 2),
    y: PAD + (1 - (v - min) / range) * (H - PAD * 2),
  }))

  const linePath = pts
    .map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`)
    .join(' ')

  const fillPath =
    linePath +
    ` L ${pts[pts.length - 1].x.toFixed(1)} ${H} L ${pts[0].x.toFixed(1)} ${H} Z`

  const finalPnl = data[data.length - 1]
  const color = finalPnl >= 0 ? '#00ff88' : '#ff4466'

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="pnl-chart" preserveAspectRatio="none">
      <defs>
        <linearGradient id="pnl-fill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.25" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      <path d={fillPath} fill="url(#pnl-fill)" />
      <path
        d={linePath}
        fill="none"
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

// ── Root ─────────────────────────────────────────────────────────────────────

export default function App() {
  // One ref array for all 5 panel DOM nodes.
  // PanelController inside the Canvas updates opacity directly — zero re-renders.
  const panelRefs = useRef([null, null, null, null, null])

  return (
    <div className="app">
      {/* ── Full-screen R3F canvas ── */}
      <Canvas
        gl={{ antialias: true }}
        camera={{ fov: 45, near: 0.1, far: 200, position: [0, 0, 40] }}
      >
        <ScrollControls pages={5} damping={0.25}>
          <Scene panelRefs={panelRefs} />
        </ScrollControls>
      </Canvas>

      {/* ── Panel 1: Approval Queue — LEFT ── */}
      <div
        ref={(el) => (panelRefs.current[0] = el)}
        className="panel panel-left"
        style={{ opacity: 0 }}
      >
        <div className="panel-header">
          <span className="panel-tag">§ 01 · MOUTH</span>
          <h2 className="panel-title">Approval Queue</h2>
        </div>
        <div className="panel-body">
          {MOCK.approvalQueue.map((p) => (
            <div key={p.market_id} className={`trade-row${p.trap_warning ? ' trap' : ''}`}>
              <div className="row-head">
                <span className="market-id">{p.market_id}</span>
                <span className={`badge outcome-${p.outcome}`}>{p.outcome}</span>
                {p.trap_warning && <span className="trap-badge">⚠ TRAP</span>}
              </div>
              <div className="row-metrics">
                <div className="metric">
                  <span className="metric-label">Score</span>
                  <span className="metric-value accent">
                    {(p.composite_score * 100).toFixed(0)}
                  </span>
                </div>
                <div className="metric">
                  <span className="metric-label">Size</span>
                  <span className="metric-value">${p.suggested_size_usdc}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Panel 2: Signal Feed — RIGHT ── */}
      <div
        ref={(el) => (panelRefs.current[1] = el)}
        className="panel panel-right"
        style={{ opacity: 0 }}
      >
        <div className="panel-header">
          <span className="panel-tag">§ 02 · EYE</span>
          <h2 className="panel-title">Signal Feed</h2>
        </div>
        <div className="panel-body">
          {MOCK.signalFeed.map((s) => (
            <div key={s.signal_id} className="signal-row">
              <div className="row-head">
                <span className="signal-id">{s.signal_id}</span>
                <span className={`badge status-${s.status}`}>{s.status}</span>
              </div>
              <div className="row-head" style={{ marginTop: 4 }}>
                <span className="market-id">{s.market_id}</span>
                <span className="metric-value accent">
                  {(s.composite_score * 100).toFixed(0)}
                </span>
              </div>
              <div className="signal-time">
                {new Date(s.fired_at).toLocaleTimeString()}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Panel 3: System Status — LEFT ── */}
      <div
        ref={(el) => (panelRefs.current[2] = el)}
        className="panel panel-left"
        style={{ opacity: 0 }}
      >
        <div className="panel-header">
          <span className="panel-tag">§ 03 · BRAIN</span>
          <h2 className="panel-title">System Status</h2>
        </div>
        <div className="panel-body">
          <div className="status-grid">
            <div className="status-item">
              <span className="metric-label">Pipeline</span>
              <span className={`status-val ${MOCK.systemStatus.is_paused ? 'warn' : 'pos'}`}>
                {MOCK.systemStatus.is_paused ? 'PAUSED' : 'LIVE'}
              </span>
            </div>
            <div className="status-item">
              <span className="metric-label">Mode</span>
              <span className="status-val accent">
                {MOCK.systemStatus.paper_trading ? 'PAPER' : 'LIVE'}
              </span>
            </div>
            <div className="status-item">
              <span className="metric-label">Last Block</span>
              <span className="metric-value">
                {MOCK.systemStatus.last_block_processed.toLocaleString()}
              </span>
            </div>
            <div className="status-item">
              <span className="metric-label">Daily P&L</span>
              <span
                className={`metric-value ${MOCK.systemStatus.daily_pnl_usdc >= 0 ? 'pos' : 'neg'}`}
              >
                {MOCK.systemStatus.daily_pnl_usdc >= 0 ? '+' : ''}$
                {MOCK.systemStatus.daily_pnl_usdc.toFixed(2)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* ── Panel 4: Open Positions — RIGHT ── */}
      <div
        ref={(el) => (panelRefs.current[3] = el)}
        className="panel panel-right"
        style={{ opacity: 0 }}
      >
        <div className="panel-header">
          <span className="panel-tag">§ 04 · FIN</span>
          <h2 className="panel-title">Open Positions</h2>
        </div>
        <div className="panel-body">
          {MOCK.positions.map((p) => (
            <div key={`${p.market_id}-${p.outcome}`} className="position-row">
              <div className="row-head">
                <span className="market-id">{p.market_id}</span>
                <span className={`badge outcome-${p.outcome}`}>{p.outcome}</span>
              </div>
              <div className="row-metrics">
                <div className="metric">
                  <span className="metric-label">Entry</span>
                  <span className="metric-value">{p.entry_price.toFixed(2)}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Current</span>
                  <span className="metric-value">{p.current_price.toFixed(2)}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Unrealized</span>
                  <span
                    className={`metric-value ${p.unrealized_pnl_pct >= 0 ? 'pos' : 'neg'}`}
                  >
                    {p.unrealized_pnl_pct >= 0 ? '+' : ''}
                    {p.unrealized_pnl_pct.toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Panel 5: P&L History — LEFT ── */}
      <div
        ref={(el) => (panelRefs.current[4] = el)}
        className="panel panel-left"
        style={{ opacity: 0 }}
      >
        <div className="panel-header">
          <span className="panel-tag">§ 05 · TAIL</span>
          <h2 className="panel-title">P&L History</h2>
        </div>
        <div className="panel-body">
          <div className="pnl-summary">
            <span className="metric-label">30-Day Cumulative</span>
            <span
              className={`metric-value lg ${MOCK.pnlHistory[MOCK.pnlHistory.length - 1] >= 0 ? 'pos' : 'neg'}`}
            >
              {MOCK.pnlHistory[MOCK.pnlHistory.length - 1] >= 0 ? '+' : ''}$
              {MOCK.pnlHistory[MOCK.pnlHistory.length - 1].toFixed(2)}
            </span>
          </div>
          <PnLChart data={MOCK.pnlHistory} />
        </div>
      </div>
    </div>
  )
}
