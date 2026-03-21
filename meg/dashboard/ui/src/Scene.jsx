import { useRef, useEffect, useMemo, Suspense } from 'react'
import * as THREE from 'three'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF, useAnimations, useScroll } from '@react-three/drei'

const GLB = '/megalodon/source/high_quality_shark_animation.glb'

// 6 waypoints → 5 scroll segments, each 20% wide.
// Waypoint index maps directly to scroll fraction: index / (length-1).
//   0 = scroll 0%   far back, approaching the mouth
//   1 = scroll 20%  deep inside jaw (end of bite section)
//   2 = scroll 40%  eye
//   3 = scroll 60%  head / brain
//   4 = scroll 80%  dorsal fin
//   5 = scroll 100% tail
// Recalibrate after reading bbox from console ([MEG] Shark bbox).
const WAYPOINTS = [
  { pos: new THREE.Vector3(0,     0,   40), look: new THREE.Vector3(0,    0,  0) }, // 0%  far
  { pos: new THREE.Vector3(0,  -1.5,    1), look: new THREE.Vector3(0, -0.5,  0) }, // 20% jaw
  { pos: new THREE.Vector3(20,    2,   10), look: new THREE.Vector3(0,    1,  0) }, // 40% eye
  { pos: new THREE.Vector3(0,    15,   20), look: new THREE.Vector3(0,    0,  0) }, // 60% head
  { pos: new THREE.Vector3(-15,  18,   -5), look: new THREE.Vector3(0,    2, -3) }, // 80% dorsal
  { pos: new THREE.Vector3(0,     2,  -28), look: new THREE.Vector3(0,    0,  0) }, // 100% tail
]

// Case-insensitive keyword search across all clip names.
function findClip(actions, keys, keywords) {
  for (const kw of keywords) {
    const match = keys.find(k => k.toLowerCase().includes(kw))
    if (match) {
      console.log(`[MEG] Clip resolved: keyword "${kw}" → "${match}"`)
      return actions[match]
    }
  }
  return null
}

// ── Particles ─────────────────────────────────────────────────────────────────

function Particles() {
  const ref = useRef()
  const COUNT = 200

  const [positions, velocities] = useMemo(() => {
    const pos = new Float32Array(COUNT * 3)
    const vel = new Float32Array(COUNT)
    for (let i = 0; i < COUNT; i++) {
      pos[i * 3 + 0] = (Math.random() - 0.5) * 20
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10
      pos[i * 3 + 2] = (Math.random() - 0.5) * 15
      vel[i] = 0.003 + Math.random() * 0.004
    }
    return [pos, vel]
  }, [])

  useFrame(() => {
    if (!ref.current) return
    const arr = ref.current.geometry.attributes.position.array
    for (let i = 0; i < COUNT; i++) {
      arr[i * 3 + 1] += velocities[i]
      if (arr[i * 3 + 1] > 6) arr[i * 3 + 1] = -6
    }
    ref.current.geometry.attributes.position.needsUpdate = true
  })

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={COUNT}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial color="#00d4ff" size={0.02} sizeAttenuation transparent opacity={0.8} />
    </points>
  )
}

// ── Shark — model + fully scroll-driven animations ────────────────────────────

function Shark() {
  const sharkRef = useRef()
  const { scene, animations } = useGLTF(GLB)
  const { actions, mixer } = useAnimations(animations, sharkRef)
  const scroll = useScroll()

  // Action refs — set once in useEffect, read every frame
  const biteRef   = useRef(null)
  const swimRef   = useRef(null)
  const circleRef = useRef(null)
  const biteDur   = useRef(3.5) // overwritten when GLB loads
  const animState = useRef('none')
  const warnedRef = useRef(false)

  // ── Debug: scene load + ref check ──
  useEffect(() => {
    // Check 1: confirm GLB scene loaded
    console.log('[MEG] GLB scene object:', scene)
    console.log('[MEG] Scene type:', scene?.type, '| visible:', scene?.visible,
                '| children:', scene?.children?.length)
    if (!scene) { console.error('[MEG] scene is null — GLB failed to load'); return }

    // Check 3: scale is set by <primitive scale={1.5}> — log it after commit
    // (sharkRef is populated after the JSX commits, so read it in a nested rAF)
    requestAnimationFrame(() => {
      if (sharkRef.current) {
        console.log('[MEG] sharkRef.current:', sharkRef.current)
        console.log('[MEG] sharkRef scale:', sharkRef.current.scale)
        console.log('[MEG] sharkRef visible:', sharkRef.current.visible)
        console.log('[MEG] sharkRef position:', sharkRef.current.position)
      } else {
        console.error('[MEG] sharkRef.current is null after commit!')
      }
    })

    // Force-ensure nothing in the GLB tree is hidden
    scene.visible = true
    scene.traverse(child => {
      if (!child.visible) {
        console.warn('[MEG] Invisible child found and fixed:', child.name, child.type)
        child.visible = true
      }
    })

    const box = new THREE.Box3().setFromObject(scene)
    const size = new THREE.Vector3()
    const center = new THREE.Vector3()
    box.getSize(size)
    box.getCenter(center)
    console.log('[MEG] Shark bbox size:', size, '| center:', center)
    console.log('[MEG] Shark bbox min:', box.min, '| max:', box.max)
  }, [scene])

  // ── Resolve clips on load ──
  useEffect(() => {
    if (!actions || !mixer) return
    const keys = Object.keys(actions)
    // Check 1: log every clip name from the GLB
    console.log('[MEG] All GLB clip names:', keys)
    if (keys.length === 0) return

    const bite   = findClip(actions, keys, ['bite', 'attack', 'snap', 'jaw', 'chomp', 'open'])
    // fallback to first clip (index 0), not second, so there's always a swim
    const swim   = findClip(actions, keys, ['swim', 'idle', 'move', 'float', 'cruise'])
               ?? actions[keys[0]]
    const circle = findClip(actions, keys, ['circle', 'turn', 'patrol', 'loop', 'rotate'])

    console.log('[MEG] Resolved — bite:', bite?.getClip().name ?? 'none',
                '| swim:', swim?.getClip().name ?? 'none',
                '| circle:', circle?.getClip().name ?? 'none')

    biteRef.current   = bite
    swimRef.current   = swim
    circleRef.current = circle
    if (bite) biteDur.current = bite.getClip().duration

    // FIX: always start with swim so the mesh renders in a valid animated pose.
    // useFrame switches to bite-driven control when scroll < 0.2.
    // Previously starting bite paused at t=0 could put the mesh in a degenerate
    // bind-pose state before the mixer had fully attached to the scene ref.
    swim?.reset().play()
    animState.current = 'swim'
    console.log('[MEG] Initial animation: swim — mesh should be visible now')
  }, [actions, mixer]) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Per-frame: scroll drives bite time; crossfade at 20%; swim↔circle ──
  useFrame(() => {
    const o    = scroll.offset
    const bite = biteRef.current
    const swim = swimRef.current
    const circ = circleRef.current

    // Check 2: log sharkRef null state (once, not every frame)
    if (!sharkRef.current) {
      if (!warnedRef.current) {
        console.warn('[MEG] useFrame: sharkRef.current is null')
        warnedRef.current = true
      }
      return
    }

    if (o < 0.2) {
      // ── Bite section (0–20%): scroll manually drives bite.time ──
      if (animState.current !== 'bite' && bite) {
        // Entering bite section (from swim on re-scroll or initial load at o≈0)
        console.log('[MEG] Entering bite section — switching to manual time control')
        swim?.isRunning() && swim.fadeOut(0.3)
        circ?.isRunning() && circ.fadeOut(0.3)
        // Play bite but immediately pause so mixer doesn't auto-advance time
        bite.reset().play()
        bite.paused = true
        animState.current = 'bite'
      }
      // Drive time: scroll 0→0.2 maps bite 0→full duration
      if (bite && animState.current === 'bite') {
        bite.time = Math.min((o / 0.2) * biteDur.current, biteDur.current)
      }
      return
    }

    // ── Post-bite sections (20–100%) ──

    // First frame after crossing 20%: leave bite → crossfade to swim or circle
    if (animState.current === 'bite') {
      const inEye  = o < 0.4
      const target = inEye && circ ? circ : swim
      if (bite) bite.paused = false // unpause so crossFadeTo works cleanly
      target.reset().play()
      bite?.crossFadeTo(target, 0.5, true)
      console.log(`[MEG] Exiting bite section → "${target.getClip().name}"`)
      animState.current = inEye && circ ? 'circle' : 'swim'
    }

    // Eye section (20–40%): circle; all other sections: swim
    const desired = o >= 0.2 && o < 0.4 && circ ? 'circle' : 'swim'
    if (desired === animState.current) return

    const fromAction = animState.current === 'circle' ? circ : swim
    const toAction   = desired === 'circle' ? circ : swim
    if (!fromAction || !toAction || toAction.isRunning()) return

    console.log(`[MEG] Crossfade "${animState.current}" → "${desired}" (offset ${o.toFixed(3)})`)
    toAction.reset().play()
    fromAction.crossFadeTo(toAction, 0.5, true)
    animState.current = desired
  })

  return <primitive ref={sharkRef} object={scene} scale={1.5} />
}

// ── Camera — always scroll-driven through all 6 waypoints ────────────────────

function CameraController() {
  const { camera } = useThree()
  const scroll = useScroll()
  const lookTarget  = useRef(new THREE.Vector3(0, 0, 0))
  const desiredPos  = useRef(new THREE.Vector3())
  const desiredLook = useRef(new THREE.Vector3())

  useFrame(() => {
    const o = scroll.offset
    const t = o * (WAYPOINTS.length - 1)           // 0 → 5
    const i = Math.min(Math.floor(t), WAYPOINTS.length - 2)
    const f = t - i

    desiredPos.current.lerpVectors(WAYPOINTS[i].pos,  WAYPOINTS[i + 1].pos,  f)
    desiredLook.current.lerpVectors(WAYPOINTS[i].look, WAYPOINTS[i + 1].look, f)

    camera.position.lerp(desiredPos.current, 0.06)
    lookTarget.current.lerp(desiredLook.current, 0.06)
    camera.lookAt(lookTarget.current)
  })

  return null
}

// ── Panel opacity — direct DOM, no React re-renders ───────────────────────────

function PanelController({ panelRefs }) {
  const scroll = useScroll()
  const HALF = 0.11

  useFrame(() => {
    const o = scroll.offset
    for (let i = 0; i < 5; i++) {
      const el = panelRefs.current[i]
      if (!el) continue
      const center = 0.1 + i * 0.2
      const dist   = Math.abs(o - center)
      el.style.opacity = Math.max(0, 1 - dist / HALF)
    }
  })

  return null
}

// ── Scene root ────────────────────────────────────────────────────────────────

export default function Scene({ panelRefs }) {
  return (
    <>
      <fogExp2 attach="fog" args={['#020818', 0.004]} />
      <ambientLight color="#0a2a4a" intensity={0.4} />
      <directionalLight position={[-3, 4, 2]} color="#ffffff" intensity={1.2} />

      <Particles />

      <Suspense fallback={null}>
        <Shark />
      </Suspense>

      <CameraController />
      <PanelController panelRefs={panelRefs} />
    </>
  )
}
