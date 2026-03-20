import { useRef, useEffect, useMemo, Suspense } from 'react'
import * as THREE from 'three'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF, useAnimations, useScroll } from '@react-three/drei'

const GLB = '/megalodon/source/high_quality_shark_animation.glb'

// Camera waypoints — one per scroll section.
// Section order: Mouth → Eye → Head/Brain → Dorsal Fin → Tail
const WAYPOINTS = [
  { pos: new THREE.Vector3(0, -0.2, 2.5),   look: new THREE.Vector3(0, -0.3, 0) },   // 1 Mouth
  { pos: new THREE.Vector3(2.5, 0.5, 0.5),  look: new THREE.Vector3(1.0, 0.5, 0) },  // 2 Eye
  { pos: new THREE.Vector3(0.5, 2.2, 1.5),  look: new THREE.Vector3(0, 0.4, 0) },    // 3 Head
  { pos: new THREE.Vector3(-1.2, 2.5, -0.5),look: new THREE.Vector3(0, 0.6, -1) },   // 4 Dorsal
  { pos: new THREE.Vector3(0, 0.5, -4.0),   look: new THREE.Vector3(0, 0, -2) },     // 5 Tail
]

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
      <pointsMaterial
        color="#00d4ff"
        size={0.02}
        sizeAttenuation
        transparent
        opacity={0.8}
      />
    </points>
  )
}

// ── Shark — model + animations ────────────────────────────────────────────────

function Shark() {
  const sharkRef = useRef()
  const { scene, animations } = useGLTF(GLB)
  const { actions, mixer } = useAnimations(animations, sharkRef)
  const scroll = useScroll()
  const animState = useRef('none') // 'none' | 'bite' | 'swim' | 'circle'

  // ── Initial: play "bite" once, then crossfade to "swim" ──
  useEffect(() => {
    if (!actions || !mixer) return
    const keys = Object.keys(actions)
    if (keys.length === 0) return

    const swim = actions['swim'] ?? actions[keys[0]]
    const bite = actions['bite']

    if (bite) {
      bite.setLoop(THREE.LoopOnce, 1)
      bite.clampWhenFinished = true
      bite.reset().play()
      animState.current = 'bite'

      const onFinished = () => {
        if (animState.current !== 'bite') return
        swim.reset().play()
        bite.fadeOut(0.5)
        animState.current = 'swim'
        mixer.removeEventListener('finished', onFinished)
      }
      mixer.addEventListener('finished', onFinished)
      return () => mixer.removeEventListener('finished', onFinished)
    } else {
      swim?.reset().play()
      animState.current = 'swim'
    }
  }, [actions, mixer])

  // ── Scroll-driven: swim ↔ circle (eye section = 20-40%) ──
  useFrame(() => {
    if (!actions || animState.current === 'bite') return
    const o = scroll.offset
    const desired = o >= 0.18 && o < 0.42 ? 'circle' : 'swim'
    if (desired === animState.current) return

    const from = actions[animState.current]
    const to = actions[desired]
    if (!from || !to) return
    if (to.isRunning()) return

    to.reset().play()
    from.crossFadeTo(to, 0.5, true)
    animState.current = desired
  })

  return <primitive ref={sharkRef} object={scene} scale={1.5} />
}

// ── Camera — lerps through WAYPOINTS driven by scroll ────────────────────────

function CameraController() {
  const { camera } = useThree()
  const scroll = useScroll()
  const lookTarget = useRef(new THREE.Vector3(0, -0.3, 0))

  useFrame(() => {
    const o = scroll.offset
    const t = o * (WAYPOINTS.length - 1)
    const i = Math.min(Math.floor(t), WAYPOINTS.length - 2)
    const f = t - i

    const desiredPos = new THREE.Vector3().lerpVectors(
      WAYPOINTS[i].pos,
      WAYPOINTS[i + 1].pos,
      f
    )
    const desiredLook = new THREE.Vector3().lerpVectors(
      WAYPOINTS[i].look,
      WAYPOINTS[i + 1].look,
      f
    )

    camera.position.lerp(desiredPos, 0.06)
    lookTarget.current.lerp(desiredLook, 0.06)
    camera.lookAt(lookTarget.current)
  })

  return null
}

// ── Panel opacity — direct DOM manipulation, no React re-renders ──────────────

function PanelController({ panelRefs }) {
  const scroll = useScroll()
  // Section centers: 0.1, 0.3, 0.5, 0.7, 0.9
  // Panel is fully visible at center, fades over ±0.11 on each side
  const HALF = 0.11

  useFrame(() => {
    const o = scroll.offset
    for (let i = 0; i < 5; i++) {
      const el = panelRefs.current[i]
      if (!el) continue
      const center = 0.1 + i * 0.2
      const dist = Math.abs(o - center)
      const opacity = Math.max(0, 1 - dist / HALF)
      el.style.opacity = opacity
    }
  })

  return null
}

// ── Scene root ────────────────────────────────────────────────────────────────

export default function Scene({ panelRefs }) {
  return (
    <>
      {/* Deep ocean fog */}
      <fogExp2 attach="fog" args={['#020818', 0.02]} />

      {/* Lighting — spec: DirectionalLight upper-left + AmbientLight ocean tint */}
      <ambientLight color="#0a2a4a" intensity={0.4} />
      <directionalLight position={[-3, 4, 2]} color="#ffffff" intensity={1.2} />

      {/* Bioluminescent particles */}
      <Particles />

      {/* Megalodon */}
      <Suspense fallback={null}>
        <Shark />
      </Suspense>

      {/* Controllers — no geometry, just drive camera + panel opacity */}
      <CameraController />
      <PanelController panelRefs={panelRefs} />
    </>
  )
}
