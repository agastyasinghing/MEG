import { useRef, useState, useEffect, useCallback } from 'react'
import { Canvas } from '@react-three/fiber'
import { ScrollControls } from '@react-three/drei'
import Scene from './Scene'
import megLogoSrc from './assets/meglogo.png'
import './App.css'

// ── Seeded pseudo-random — deterministic mock, no snapshot flakiness ─────────

function seededRand(seed) {
  let s = seed >>> 0
  return () => {
    s = (Math.imul(1664525, s) + 1013904223) >>> 0
    return s / 0xffffffff
  }
}

// ── API base ─────────────────────────────────────────────────────────────────

const API = '/api/v1'

// ── Mock / seed data — used as initial state before first API response ───────
// Shapes match MEG PRD §13 API contracts. Real API responses override these.
// Fields with no API equivalent (latency_ms, markets_active, telegram,
// systemState, pnlHistory) keep their mock values until backend endpoints exist.

const MOCK = {
  topBar: {
    status:          'LIVE',
    latency_ms:      12,
    markets_active:  847,
    telegram:        'CONNECTED',
  },
  primarySignal: {
    market_id:           'MKT-0441',
    market_name:         'BTC reaches $120k before July 2026',
    outcome:             'YES',
    composite_score:     0.78,
    confidence_pct:      78,
    edge_pct:            14.2,
    suggested_size_usdc: 150,
    fired_at:            '2026-03-20T14:22:00Z',
    lead_lag_hrs:        8.4,
    consensus:           'STRONG',
    trap_risk:           'LOW',
    whale_align:         'HIGH',
    whale_count:         3,
    trap_warning:        false,
  },
  approvalQueue: [
    {
      market_id:           'MKT-0441',
      market_name:         'BTC $120k before July',
      outcome:             'YES',
      composite_score:     0.78,
      suggested_size_usdc: 150,
      trap_warning:        false,
      urgency:             'high',
      status:              'TRACKING',
      time_ago:            '2m',
    },
    {
      market_id:           'MKT-0389',
      market_name:         'Fed rate cut in May',
      outcome:             'NO',
      composite_score:     0.62,
      suggested_size_usdc: 80,
      trap_warning:        true,
      urgency:             'normal',
      status:              'TRAP',
      time_ago:            '11m',
    },
    {
      market_id:           'MKT-0512',
      market_name:         'ETH outperforms BTC Q2',
      outcome:             'YES',
      composite_score:     0.71,
      suggested_size_usdc: 120,
      trap_warning:        false,
      urgency:             'normal',
      status:              'LOCKED',
      time_ago:            '18m',
    },
  ],
  signalFeed: [
    {
      signal_id:       'SIG-0441',
      market_id:       'MKT-0441',
      market_name:     'BTC $120k before July',
      outcome:         'YES',
      composite_score: 0.78,
      status:          'QUALIFIED',
      fired_at:        '2026-03-20T14:22:00Z',
    },
    {
      signal_id:       'SIG-0440',
      market_id:       'MKT-0387',
      market_name:     'SOL / BTC ratio holds',
      outcome:         'NO',
      composite_score: 0.55,
      status:          'FILTERED',
      fired_at:        '2026-03-20T14:18:00Z',
    },
    {
      signal_id:       'SIG-0439',
      market_id:       'MKT-0389',
      market_name:     'Fed rate cut in May',
      outcome:         'NO',
      composite_score: 0.62,
      status:          'QUALIFIED',
      fired_at:        '2026-03-20T14:10:00Z',
    },
    {
      signal_id:       'SIG-0438',
      market_id:       'MKT-0201',
      market_name:     'DOGE above $0.30 by April',
      outcome:         'YES',
      composite_score: 0.43,
      status:          'FILTERED',
      fired_at:        '2026-03-20T13:55:00Z',
    },
  ],
  systemStatus: {
    is_paused:             false,
    paper_trading:         true,
    last_block_processed:  68234891,
    daily_pnl_usdc:        47.32,
  },
  systemState: {
    market_regime:       'TRENDING',
    signal_density:      4.7,
    avg_confidence_pct:  71,
    risk_level:          'LOW',
  },
  positions: [
    {
      market_id:           'MKT-0441',
      market_name:         'BTC $120k before July',
      outcome:             'YES',
      entry_price:         0.52,
      current_price:       0.61,
      unrealized_pnl_pct:  17.3,
      unrealized_pnl_usdc: 25.95,
      stance:              'HOLD',
    },
    {
      market_id:           'MKT-0389',
      market_name:         'Fed rate cut in May',
      outcome:             'NO',
      entry_price:         0.38,
      current_price:       0.35,
      unrealized_pnl_pct:  -7.9,
      unrealized_pnl_usdc: -6.32,
      stance:              'HOLD',
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

// ── API → UI data adapter ────────────────────────────────────────────────────
// Maps raw API responses onto the shape the component tree expects.
// Real values take precedence; MOCK values fill in fields with no API equivalent.
//
// API responses:
//   status   → GET /api/v1/status
//   signals  → GET /api/v1/signals   (last 50, newest first)
//   pending  → GET /api/v1/signals?status=PENDING
//   positions→ GET /api/v1/positions
//   pnl      → GET /api/v1/pnl
//
// Data flow:
//   Promise.allSettled([status, signals, pending, positions, pnl])
//       │
//   ┌───┴─────────────────────────────────────────────┐
//   │ fulfilled → merge into liveData                 │
//   │ rejected  → keep prior value for that section   │
//   └─────────────────────────────────────────────────┘
//       │
//   setLiveData(adapted) → re-render

function adaptData(prev, { status, signals, pending, positions, pnl }) {
  const next = { ...prev }

  // systemStatus — from GET /api/v1/status
  if (status) {
    next.systemStatus = {
      is_paused:            status.is_paused,
      paper_trading:        status.paper_trading,
      last_block_processed: status.last_block_processed,
      daily_pnl_usdc:       status.daily_pnl_usdc,
    }
    // topBar: derive LIVE/PAUSED from is_paused; keep mock for latency/markets/telegram
    next.topBar = {
      ...prev.topBar,
      status: status.is_paused ? 'PAUSED' : 'LIVE',
    }
  }

  // signalFeed — from GET /api/v1/signals
  if (signals && Array.isArray(signals.signals)) {
    next.signalFeed = signals.signals.map(s => ({
      signal_id:       s.signal_id,
      market_id:       s.market_id,
      market_name:     s.market_id,   // market_name not yet in API; use market_id
      outcome:         s.outcome,
      composite_score: s.composite_score,
      status:          s.status,
      fired_at:        s.fired_at,
    }))
  }

  // approvalQueue — from GET /api/v1/signals?status=PENDING
  if (pending && Array.isArray(pending.signals)) {
    next.approvalQueue = pending.signals.map(s => {
      const minsAgo = Math.round((Date.now() - new Date(s.fired_at).getTime()) / 60_000)
      const timeAgo = minsAgo < 60 ? `${minsAgo}m` : `${Math.round(minsAgo / 60)}h`
      return {
        market_id:           s.market_id,
        market_name:         s.market_id,
        outcome:             s.outcome,
        composite_score:     s.composite_score,
        suggested_size_usdc: s.recommended_size_usdc,
        trap_warning:        s.trap_warning,
        urgency:             s.composite_score >= 0.65 ? 'high' : 'normal',
        status:              s.trap_warning ? 'TRAP' : 'TRACKING',
        time_ago:            timeAgo,
        signal_id:           s.signal_id,   // retained for approve/reject calls
      }
    })

    // primarySignal — first PENDING item with full context
    if (pending.signals.length > 0) {
      const s = pending.signals[0]
      next.primarySignal = {
        market_id:           s.market_id,
        market_name:         s.market_id,
        outcome:             s.outcome,
        composite_score:     s.composite_score,
        confidence_pct:      Math.round(s.composite_score * 100),
        edge_pct:            parseFloat(((s.composite_score - 0.5) * 100).toFixed(1)),
        suggested_size_usdc: s.recommended_size_usdc,
        fired_at:            s.fired_at,
        lead_lag_hrs:        s.scores_json?.lead_lag != null
                               ? parseFloat((s.scores_json.lead_lag * 10).toFixed(1))
                               : 0,
        consensus:           s.whale_count >= 3 ? 'STRONG' : s.whale_count >= 2 ? 'MODERATE' : 'WEAK',
        trap_risk:           s.trap_warning ? 'HIGH' : s.saturation_score > 0.6 ? 'MED' : 'LOW',
        whale_align:         s.composite_score >= 0.7 ? 'HIGH' : 'MODERATE',
        whale_count:         s.whale_count,
        trap_warning:        s.trap_warning,
        signal_id:           s.signal_id,
      }
    } else {
      next.primarySignal = null
    }
  }

  // positions — from GET /api/v1/positions
  if (positions && Array.isArray(positions.positions)) {
    next.positions = positions.positions.map(p => ({
      market_id:           p.market_id,
      market_name:         p.market_id,
      outcome:             p.outcome,
      entry_price:         p.entry_price,
      current_price:       p.current_price,
      unrealized_pnl_pct:  p.unrealized_pnl_pct,
      unrealized_pnl_usdc: p.unrealized_pnl_usdc,
      stance:              'HOLD',          // v1: always HOLD (auto-exit not implemented)
      position_id:         p.position_id,  // retained for exit calls
    }))
  }

  // pnlHistory — equity curve endpoint not yet implemented; keep mock seed
  // pnl summary from GET /api/v1/pnl is available but not rendered in pnlHistory array yet

  return next
}

// ── SVG P&L chart for HUD panel (original, unchanged) ────────────────────────

function PnLChart({ data: chartData }) {
  const W = 280
  const H = 80
  const PAD = 4

  if (!chartData || chartData.length === 0) {
    const midY = (H / 2).toFixed(1)
    return (
      <div className="pnl-chart-wrap">
        <svg viewBox={`0 0 ${W} ${H}`} className="pnl-chart" preserveAspectRatio="none">
          <line
            x1={PAD} y1={midY} x2={W - PAD} y2={midY}
            stroke="rgba(0, 212, 255, 0.18)" strokeWidth="1.5"
            strokeDasharray="5 5" strokeLinecap="round"
          />
        </svg>
        <div className="pnl-no-trades">No trades yet</div>
      </div>
    )
  }

  const min = Math.min(...chartData)
  const max = Math.max(...chartData)
  const range = max - min || 1
  const pts = chartData.map((v, i) => ({
    x: PAD + (i / (chartData.length - 1)) * (W - PAD * 2),
    y: PAD + (1 - (v - min) / range) * (H - PAD * 2),
  }))
  const linePath = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(' ')
  const fillPath = linePath + ` L ${pts[pts.length - 1].x.toFixed(1)} ${H} L ${pts[0].x.toFixed(1)} ${H} Z`
  const finalPnl = chartData[chartData.length - 1]
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
      <path d={linePath} fill="none" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

// ── Dashboard P&L chart — glow, zero-line, drawdown shading ─────────────────

function DashPnLChart({ data: chartData }) {
  const W   = 1000
  const H   = 80
  const PAD = 6

  if (!chartData || chartData.length === 0) {
    return (
      <div className="dash-pnl-wrap">
        <svg viewBox={`0 0 ${W} ${H}`} className="dash-pnl-svg" preserveAspectRatio="none">
          <line x1={PAD} y1={H / 2} x2={W - PAD} y2={H / 2}
            stroke="rgba(0,212,255,0.15)" strokeWidth="1" strokeDasharray="8 6" />
        </svg>
        <div className="dash-pnl-empty">NO TRADES YET</div>
      </div>
    )
  }

  const min   = Math.min(...chartData)
  const max   = Math.max(...chartData)
  const range = max - min || 1
  const toX   = (i) => PAD + (i / (chartData.length - 1)) * (W - PAD * 2)
  const toY   = (v) => PAD + (1 - (v - min) / range) * (H - PAD * 2)

  const pts      = chartData.map((v, i) => ({ x: toX(i), y: toY(v) }))
  const linePath = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')
  const areaPath = linePath + ` L${toX(chartData.length - 1).toFixed(1)},${H} L${PAD},${H} Z`

  const zeroY       = min < 0 && max > 0 ? toY(0) : null
  const lastVal     = chartData[chartData.length - 1]
  const prevVal     = chartData.length > 1 ? chartData[chartData.length - 2] : 0
  const todayPnl    = lastVal - prevVal
  const totalPnl    = lastVal
  const wins        = chartData.filter((v, i) => i > 0 && v > chartData[i - 1]).length
  const winRate     = Math.round((wins / (chartData.length - 1)) * 100)

  return (
    <div className="dash-pnl-wrap">
      <div className="dash-pnl-header">
        <span className="db-panel-label">P&L HISTORY</span>
        <div className="dash-pnl-stats">
          <span className={`dash-pnl-stat ${todayPnl >= 0 ? 'pos' : 'neg'}`}>
            TODAY {todayPnl >= 0 ? '+' : ''}${todayPnl.toFixed(2)}
          </span>
          <span className={`dash-pnl-stat ${totalPnl >= 0 ? 'pos' : 'neg'}`}>
            TOTAL {totalPnl >= 0 ? '+' : ''}${totalPnl.toFixed(2)}
          </span>
          <span className="dash-pnl-stat neu">WIN RATE {winRate}%</span>
        </div>
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} className="dash-pnl-svg" preserveAspectRatio="none">
        <defs>
          <linearGradient id="dpnl-grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#00d4ff" stopOpacity="0.1" />
            <stop offset="100%" stopColor="#00d4ff" stopOpacity="0" />
          </linearGradient>
          {zeroY !== null && (
            <>
              <clipPath id="dpnl-clip-above">
                <rect x="0" y="0" width={W} height={zeroY} />
              </clipPath>
              <clipPath id="dpnl-clip-below">
                <rect x="0" y={zeroY} width={W} height={H - zeroY} />
              </clipPath>
            </>
          )}
          <filter id="dpnl-glow">
            <feDropShadow dx="0" dy="0" stdDeviation="3" floodColor="#00d4ff" floodOpacity="0.8" />
          </filter>
        </defs>

        {/* Zero reference line */}
        {zeroY !== null && (
          <line x1={PAD} y1={zeroY} x2={W - PAD} y2={zeroY}
            stroke="rgba(255,255,255,0.08)" strokeWidth="0.5" />
        )}

        {/* Area fill — cyan above zero */}
        {zeroY !== null ? (
          <path d={areaPath} fill="url(#dpnl-grad)" clipPath="url(#dpnl-clip-above)" />
        ) : (
          <path d={areaPath} fill="url(#dpnl-grad)" />
        )}

        {/* Drawdown fill — red below zero */}
        {zeroY !== null && (
          <path d={areaPath} fill="rgba(255,68,68,0.06)" clipPath="url(#dpnl-clip-below)" />
        )}

        {/* Line with glow */}
        <path d={linePath} fill="none" stroke="#00d4ff" strokeWidth="1.5"
          strokeLinecap="round" strokeLinejoin="round" filter="url(#dpnl-glow)" />
      </svg>
    </div>
  )
}

// ── Status tag helper ────────────────────────────────────────────────────────

const TAG_COLORS = {
  QUALIFIED: '#00d4ff',
  FILTERED:  '#4a6070',
  TRACKING:  '#00d4ff',
  LOCKED:    '#00ff88',
  TRAP:      '#ff4444',
  HOLD:      '#00d4ff',
  EXIT:      '#ff4444',
  SCALE:     '#00ff88',
}

function StatusTag({ label }) {
  const color = TAG_COLORS[label] ?? '#4a6070'
  return (
    <span className="db-status-tag" style={{ '--tag-color': color }}>
      {label}
    </span>
  )
}

// ── Root ─────────────────────────────────────────────────────────────────────

export default function App() {
  const panelRefs        = useRef([null, null, null, null, null])
  const canvasWrapperRef = useRef(null)
  const dashboardRef     = useRef(null)

  // ── Live data state — seeded from MOCK so panels are never empty on first render
  const [liveData, setLiveData] = useState(MOCK)

  // ── API fetch + 10s poll ──────────────────────────────────────────────────
  const fetchAll = useCallback(async () => {
    const [statusRes, signalsRes, pendingRes, positionsRes, pnlRes] =
      await Promise.allSettled([
        fetch(`${API}/status`).then(r => r.ok ? r.json() : null),
        fetch(`${API}/signals`).then(r => r.ok ? r.json() : null),
        fetch(`${API}/signals?status=PENDING`).then(r => r.ok ? r.json() : null),
        fetch(`${API}/positions`).then(r => r.ok ? r.json() : null),
        fetch(`${API}/pnl`).then(r => r.ok ? r.json() : null),
      ])

    const get = res => res.status === 'fulfilled' ? res.value : null

    setLiveData(prev => adaptData(prev, {
      status:    get(statusRes),
      signals:   get(signalsRes),
      pending:   get(pendingRes),
      positions: get(positionsRes),
      pnl:       get(pnlRes),
    }))
  }, [])

  useEffect(() => {
    fetchAll()
    const id = setInterval(fetchAll, 10_000)
    return () => clearInterval(id)
  }, [fetchAll])

  // ── Approve / Reject handlers ─────────────────────────────────────────────
  const handleApprove = useCallback(async (signalId) => {
    if (!signalId) return
    try {
      const res = await fetch(`${API}/signals/${signalId}/approve`, { method: 'POST' })
      if (res.ok) {
        // Optimistic: remove from approval queue and clear primary signal
        setLiveData(prev => ({
          ...prev,
          approvalQueue: prev.approvalQueue.filter(p => p.signal_id !== signalId),
          primarySignal: prev.primarySignal?.signal_id === signalId ? null : prev.primarySignal,
        }))
      } else {
        const err = await res.json().catch(() => ({}))
        console.error('Approve failed:', res.status, err.detail ?? err)
      }
    } catch (e) {
      console.error('Approve request error:', e)
    }
  }, [])

  const handleReject = useCallback(async (signalId) => {
    if (!signalId) return
    try {
      const res = await fetch(`${API}/signals/${signalId}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason: 'rejected_via_dashboard' }),
      })
      if (res.ok) {
        setLiveData(prev => ({
          ...prev,
          approvalQueue: prev.approvalQueue.filter(p => p.signal_id !== signalId),
          primarySignal: prev.primarySignal?.signal_id === signalId ? null : prev.primarySignal,
        }))
      } else {
        const err = await res.json().catch(() => ({}))
        console.error('Reject failed:', res.status, err.detail ?? err)
      }
    } catch (e) {
      console.error('Reject request error:', e)
    }
  }, [])

  const {
    topBar, primarySignal, approvalQueue, signalFeed,
    systemStatus, systemState, positions, pnlHistory,
  } = liveData

  return (
    <div className="app">
      {/* ── Canvas wrapper — faded out by cutscene GSAP tween ── */}
      <div className="canvas-wrapper" ref={canvasWrapperRef}>

      {/* ── Full-screen R3F canvas ── */}
      <Canvas
        gl={{ antialias: true }}
        camera={{ fov: 45, near: 0.1, far: 200, position: [0, 0, 40] }}
      >
        <ScrollControls pages={5} damping={0.25}>
          <Scene panelRefs={panelRefs} canvasWrapperRef={canvasWrapperRef} dashboardRef={dashboardRef} />
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
          {approvalQueue.length === 0 ? (
            <div className="empty-state">No pending proposals</div>
          ) : (
            approvalQueue.map((p) => (
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
            ))
          )}
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
          {signalFeed.length === 0 ? (
            <div className="empty-state">
              <span className="pulse-dot" />
              Waiting for signals...
            </div>
          ) : (
            signalFeed.map((s) => (
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
            ))
          )}
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
              {systemStatus ? (
                <span className={`status-val ${systemStatus.is_paused ? 'warn' : 'pos'}`}>
                  {systemStatus.is_paused ? 'PAUSED' : 'LIVE'}
                </span>
              ) : (
                <span className="status-dash">—</span>
              )}
            </div>
            <div className="status-item">
              <span className="metric-label">Mode</span>
              {systemStatus ? (
                <span className="mode-badge">
                  {systemStatus.paper_trading ? 'PAPER' : 'LIVE'}
                </span>
              ) : (
                <span className="mode-badge">PAPER</span>
              )}
            </div>
            <div className="status-item">
              <span className="metric-label">Last Block</span>
              {systemStatus ? (
                <span className="metric-value">
                  {systemStatus.last_block_processed.toLocaleString()}
                </span>
              ) : (
                <span className="status-dash">—</span>
              )}
            </div>
            <div className="status-item">
              <span className="metric-label">Daily P&L</span>
              {systemStatus ? (
                <span
                  className={`metric-value ${systemStatus.daily_pnl_usdc >= 0 ? 'pos' : 'neg'}`}
                >
                  {systemStatus.daily_pnl_usdc >= 0 ? '+' : ''}$
                  {systemStatus.daily_pnl_usdc.toFixed(2)}
                </span>
              ) : (
                <span className="status-dash">—</span>
              )}
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
          {positions.length === 0 ? (
            <div className="empty-state">No open positions</div>
          ) : (
            positions.map((p) => (
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
            ))
          )}
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
            {pnlHistory.length > 0 ? (
              <span
                className={`metric-value lg ${pnlHistory[pnlHistory.length - 1] >= 0 ? 'pos' : 'neg'}`}
              >
                {pnlHistory[pnlHistory.length - 1] >= 0 ? '+' : ''}$
                {pnlHistory[pnlHistory.length - 1].toFixed(2)}
              </span>
            ) : (
              <span className="metric-value lg" style={{ color: 'var(--text-dim)' }}>
                $0.00
              </span>
            )}
          </div>
          <PnLChart data={pnlHistory} />
        </div>
      </div>

      </div>{/* end .canvas-wrapper */}

      {/* ── Traditional dashboard — hidden until cutscene completes ── */}
      {/* meg-logo img is spawned dynamically by spawnAndFlyLogo in Scene.jsx */}
      <div className="traditional-dashboard" ref={dashboardRef}>

        {/* ── PAPER TRADING persistent banner — PRD §14 ── */}
        {/* Visible whenever paper_trading=true in system status.
            Defaults to shown (systemStatus may be null before first fetch). */}
        {(systemStatus === null || systemStatus.paper_trading) && (
          <div className="paper-trading-banner">
            ● PAPER TRADING — no real capital at risk
          </div>
        )}

        <div className="db-grid">

          {/* ── TOP BAR ── */}
          <header className="db-topbar">
            <div className="db-topbar-left">
              <img src={megLogoSrc} className="db-topbar-logo" alt="MEG" />
              <span className="db-topbar-wordmark">MEG</span>
            </div>
            <div className="db-topbar-right">
              <div className="db-topbar-stat">
                <span
                  className="db-sys-badge"
                  style={{ '--badge-color': topBar.status === 'LIVE' ? '#00ff88' : '#ffaa00' }}
                >
                  ● {topBar.status}
                </span>
              </div>
              <div className="db-topbar-stat">
                <span className="db-stat-label">LATENCY</span>
                <span className="db-stat-value">{topBar.latency_ms}ms</span>
              </div>
              <div className="db-topbar-stat">
                <span className="db-stat-label">MARKETS</span>
                <span className="db-stat-value">{topBar.markets_active}</span>
              </div>
              <div className="db-topbar-stat">
                <span
                  className="db-tg-badge"
                  style={{ '--badge-color': topBar.telegram === 'CONNECTED' ? '#00d4ff' : '#ff4444' }}
                >
                  ● {topBar.telegram}
                </span>
              </div>
            </div>
          </header>

          {/* ── APPROVAL QUEUE (left) ── */}
          <section className="db-queue db-panel">
            <div className="db-panel-label">DECISION QUEUE</div>
            {approvalQueue.length === 0 ? (
              <div className="db-empty">NO PENDING DECISIONS</div>
            ) : (
              approvalQueue.map((item) => (
                <div key={item.market_id} className="db-queue-item">
                  <div className="db-queue-top">
                    <span className="db-queue-name">{item.market_name}</span>
                    <span
                      className="db-urgency-dot"
                      style={{ '--dot-color': item.urgency === 'high' ? '#ff4444' : '#ffaa00' }}
                    />
                  </div>
                  <div className="db-queue-mid">
                    <span
                      className="db-dir-badge"
                      style={{ '--dir-color': item.outcome === 'YES' ? '#00ff88' : '#ff4444' }}
                    >
                      {item.outcome}
                    </span>
                    <div className="db-score-bar-track">
                      <div
                        className="db-score-bar-fill"
                        style={{ '--bar-w': `${item.composite_score * 100}%` }}
                      />
                    </div>
                  </div>
                  <div className="db-queue-bot">
                    <span className="db-time-ago">{item.time_ago} ago</span>
                    <StatusTag label={item.status} />
                  </div>
                </div>
              ))
            )}
          </section>

          {/* ── PRIMARY SIGNAL HERO (center) ── */}
          <section className="db-hero db-panel">
            {primarySignal ? (
              <>
                <div className="db-panel-label">PRIMARY SIGNAL</div>
                <div className="db-hero-top">
                  <span className="db-hero-market">{primarySignal.market_name}</span>
                  <span
                    className="db-dir-badge db-dir-badge-lg"
                    style={{ '--dir-color': primarySignal.outcome === 'YES' ? '#00ff88' : '#ff4444' }}
                  >
                    {primarySignal.outcome}
                  </span>
                </div>

                <div className="db-hero-scores">
                  <div className="db-hero-score-item">
                    <span className="db-hero-big">{primarySignal.confidence_pct}</span>
                    <span className="db-hero-score-label">CONFIDENCE</span>
                  </div>
                  <div className="db-hero-score-item db-hero-score-green">
                    <span className="db-hero-big">{primarySignal.edge_pct.toFixed(1)}</span>
                    <span className="db-hero-score-label">EDGE %</span>
                  </div>
                  <div className="db-hero-score-item db-hero-score-white">
                    <span className="db-hero-big">${primarySignal.suggested_size_usdc}</span>
                    <span className="db-hero-score-label">SIZE USDC</span>
                  </div>
                  <div className="db-hero-score-item">
                    <span className="db-hero-time">
                      {new Date(primarySignal.fired_at).toLocaleTimeString()}
                    </span>
                    <span className="db-hero-score-label">FIRED AT</span>
                  </div>
                </div>

                <div className="db-hero-divider" />

                <div className="db-panel-label db-panel-label-sm">WHY MEG LIKES THIS</div>
                <div className="db-hero-reasons">
                  <div className="db-reason-row">
                    <span className="db-reason-label">LEAD-LAG</span>
                    <span className="db-reason-val" style={{ '--rv-color': '#00d4ff' }}>
                      +{primarySignal.lead_lag_hrs} hrs
                    </span>
                  </div>
                  <div className="db-reason-row">
                    <span className="db-reason-label">CONSENSUS</span>
                    <span
                      className="db-reason-val"
                      style={{ '--rv-color': primarySignal.consensus === 'STRONG' ? '#00ff88' : '#ffaa00' }}
                    >
                      {primarySignal.consensus}
                    </span>
                  </div>
                  <div className="db-reason-row">
                    <span className="db-reason-label">TRAP RISK</span>
                    <span
                      className="db-reason-val"
                      style={{ '--rv-color': primarySignal.trap_risk === 'LOW' ? '#00ff88' : primarySignal.trap_risk === 'MED' ? '#ffaa00' : '#ff4444' }}
                    >
                      {primarySignal.trap_risk}
                    </span>
                  </div>
                  <div className="db-reason-row">
                    <span className="db-reason-label">WHALE ALIGN</span>
                    <span className="db-reason-val" style={{ '--rv-color': '#00d4ff' }}>
                      {primarySignal.whale_align} ({primarySignal.whale_count})
                    </span>
                  </div>
                </div>

                <div className="db-hero-divider" />

                <div className="db-hero-actions">
                  <button
                    className="db-btn db-btn-approve"
                    onClick={() => handleApprove(primarySignal.signal_id)}
                  >APPROVE</button>
                  <button
                    className="db-btn db-btn-reject"
                    onClick={() => handleReject(primarySignal.signal_id)}
                  >REJECT</button>
                </div>
              </>
            ) : (
              <div className="db-empty">NO ACTIVE SIGNAL</div>
            )}
          </section>

          {/* ── SIGNAL FEED (right) ── */}
          <section className="db-feed db-panel">
            <div className="db-panel-label">SIGNAL FEED</div>
            {signalFeed.length === 0 ? (
              <div className="db-empty">
                <span className="db-pulse-dot" />
                WAITING FOR SIGNALS
              </div>
            ) : (
              signalFeed.map((s, idx) => (
                <div key={s.signal_id} className="db-feed-item">
                  <span className="db-feed-rank">{String(idx + 1).padStart(2, '0')}</span>
                  <div className="db-feed-body">
                    <div className="db-feed-top">
                      <span className="db-feed-name">{s.market_name}</span>
                      <span
                        className="db-dir-badge"
                        style={{ '--dir-color': s.outcome === 'YES' ? '#00ff88' : '#ff4444' }}
                      >
                        {s.outcome}
                      </span>
                    </div>
                    <div className="db-score-bar-track">
                      <div
                        className="db-score-bar-fill"
                        style={{ '--bar-w': `${s.composite_score * 100}%` }}
                      />
                    </div>
                    <div className="db-feed-bot">
                      <StatusTag label={s.status} />
                      <span className="db-feed-score">{(s.composite_score * 100).toFixed(0)}</span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </section>

          {/* ── OPEN POSITIONS (bottom left, spans 2 cols) ── */}
          <section className="db-positions db-panel">
            <div className="db-panel-label">OPEN POSITIONS</div>
            {positions.length === 0 ? (
              <div className="db-empty">NO OPEN POSITIONS</div>
            ) : (
              <div className="db-pos-rows">
                {positions.map((p) => (
                  <div key={`${p.market_id}-${p.outcome}`} className="db-pos-row">
                    <div className="db-pos-left">
                      <span className="db-pos-name">{p.market_name}</span>
                      <span className="db-pos-entry">
                        entry {p.entry_price.toFixed(2)} → {p.current_price.toFixed(2)}
                      </span>
                    </div>
                    <div className="db-pos-right">
                      <span className={`db-pos-pnl ${p.unrealized_pnl_usdc >= 0 ? 'pos' : 'neg'}`}>
                        {p.unrealized_pnl_usdc >= 0 ? '+' : ''}${p.unrealized_pnl_usdc.toFixed(2)}
                        <span className="db-pos-pct">
                          ({p.unrealized_pnl_pct >= 0 ? '+' : ''}{p.unrealized_pnl_pct.toFixed(1)}%)
                        </span>
                      </span>
                      <StatusTag label={p.stance} />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>

          {/* ── SYSTEM STATE (bottom right) ── */}
          <section className="db-system db-panel">
            <div className="db-panel-label">SYSTEM STATE</div>
            <div className="db-sys-grid">
              <div className="db-sys-item">
                <span className="db-stat-label">MARKET REGIME</span>
                <span
                  className="db-sys-val"
                  style={{
                    '--sv-color':
                      systemState.market_regime === 'TRENDING' ? '#00ff88' :
                      systemState.market_regime === 'CHOPPY'   ? '#ffaa00' : '#ff4444',
                  }}
                >
                  {systemState.market_regime}
                </span>
              </div>
              <div className="db-sys-item">
                <span className="db-stat-label">SIGNAL DENSITY</span>
                <span className="db-sys-val" style={{ '--sv-color': '#00d4ff' }}>
                  {systemState.signal_density}/hr
                </span>
              </div>
              <div className="db-sys-item">
                <span className="db-stat-label">AVG CONFIDENCE</span>
                <span className="db-sys-val" style={{ '--sv-color': '#ffffff' }}>
                  {systemState.avg_confidence_pct}%
                </span>
              </div>
              <div className="db-sys-item">
                <span className="db-stat-label">RISK LEVEL</span>
                <span
                  className="db-sys-val"
                  style={{
                    '--sv-color':
                      systemState.risk_level === 'LOW'  ? '#00ff88' :
                      systemState.risk_level === 'MED'  ? '#ffaa00' : '#ff4444',
                  }}
                >
                  {systemState.risk_level}
                </span>
              </div>
            </div>
            <div
              className="db-mode-badge"
              style={{
                '--mode-color': systemStatus?.paper_trading ? '#ffaa00' : '#00ff88',
              }}
            >
              ● {systemStatus?.paper_trading ? 'PAPER TRADING' : 'LIVE TRADING'}
            </div>
          </section>

          {/* ── P&L HISTORY (full width) ── */}
          <section className="db-pnl db-panel">
            <DashPnLChart data={pnlHistory} />
          </section>

        </div>
      </div>

    </div>
  )
}
