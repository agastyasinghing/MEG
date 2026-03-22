import { useRef, useEffect, useMemo, Suspense } from 'react'
import * as THREE from 'three'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF, useAnimations, useScroll } from '@react-three/drei'
import underwaterSceneGLSL from './shaders/underwater_scene.glsl?raw'
import causticsGLSL        from './shaders/caustics.glsl?raw'
import {
  EffectComposer,
  HueSaturation,
  BrightnessContrast,
  wrapEffect,
} from '@react-three/postprocessing'
import { Effect } from 'postprocessing'
import gsap from 'gsap'
import megLogoSrc from './assets/meglogo.png'

const GLB = '/megalodon/source/high_quality_shark_animation.glb'

// 6 waypoints → 5 scroll segments, each 20% wide.
const WAYPOINTS = [
  { pos: new THREE.Vector3(0,     0,   40), look: new THREE.Vector3(0,    0,  0) }, // 0%  far
  { pos: new THREE.Vector3(0,  -1.5,    1), look: new THREE.Vector3(0, -0.5,  0) }, // 20% jaw
  { pos: new THREE.Vector3(20,    2,   10), look: new THREE.Vector3(0,    1,  0) }, // 40% eye
  { pos: new THREE.Vector3(0,    15,   20), look: new THREE.Vector3(0,    0,  0) }, // 60% head
  { pos: new THREE.Vector3(-15,  18,   -5), look: new THREE.Vector3(0,    2, -3) }, // 80% dorsal
  { pos: new THREE.Vector3(0,     2,  -28), look: new THREE.Vector3(0,    0,  0) }, // 100% tail
]

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

// ── JS port of getWaveHeight / getwaves from water_atmosphere.glsl ────────────

function wavedxJS(px, py, dx, dy, time, freq) {
  const x = (dx * px + dy * py) * freq + time
  return Math.exp(Math.sin(x) - 1.0)
}

function getWaveHeightJS(px, pz, uTime) {
  const wx = px * 0.1
  const wz = pz * 0.1
  let iter = 0, phase = 6.0, speed = 2.0
  let weight = 1.0, w = 0.0, ws = 0.0
  for (let i = 0; i < 5; i++) {
    const dx = Math.sin(iter), dy = Math.cos(iter)
    w += wavedxJS(wx, wz, dx, dy, speed * uTime, phase) * weight
    ws += weight
    iter += 12.0
    weight *= 0.75
    phase  *= 1.18
    speed  *= 1.08
  }
  return w / ws
}

// ── 1. SCENE SETUP — null background so the fullscreen quad shows through ─────

function SceneSetup() {
  const { scene } = useThree()
  useEffect(() => { scene.background = null }, [scene])
  return null
}

// ── UNDERWATER BACKGROUND — fullscreen raymarched environment quad ─────────────
// gl_Position = vec4(pos.xy, 1, 1) places this at NDC depth 1.0 (far plane),
// so it renders behind every 3D object without touching the depth buffer.
// The shader (underwater_scene.glsl) provides: rocky cave floor below,
// water surface ripples visible above, camera drifting through the scene.

const UNDERWATER_VERT = /* glsl */`
void main() {
  gl_Position = vec4(position.xy, 1.0, 1.0);
}`

// Inject getCaustic() into the rock shading pass of underwaterScene() via JS
// string replace — targets the single occurrence of `col = mix(rock, col, tn)`
// at the end of the t<FAR branch. causticsGLSL is embedded before
// underwaterSceneGLSL so getCaustic() is in scope when underwaterScene() runs.
const underwaterWithCaustics = underwaterSceneGLSL
  // 1. Bake caustics into rock shading (getCaustic in scope from causticsGLSL above)
  .replace(
    'col = mix(rock, col, tn);',
    `// Caustic light patterns baked into the rock — light filtering through the surface
   vec3 causticLight = getCaustic(hp.xz * 0.05, uTime);
   rock += causticLight * 0.35 * (1.0 - tn);
   col = mix(rock, col, tn);`
  )
  // 2. Nonlinear depth darkening — injected at end of else block while t is in scope
  .replace(
    '        float f = (-dir.y - 0.3 + sin(time * 0.05) * 0.2) * 0.3185;\n        f = clamp(f, 0.0, 1.0);\n        col = mix(col, rock, f);\n    }',
    `        float f = (-dir.y - 0.3 + sin(time * 0.05) * 0.2) * 0.3185;
        f = clamp(f, 0.0, 1.0);
        col = mix(col, rock, f);
        // Nonlinear depth darkening: far rock collapses faster than near
        float depthFade = 1.0 - exp(-max(t - 5.0, 0.0) * 0.15);
        col = mix(col, vec3(0.0, 0.01, 0.02), depthFade * depthFade);
    }`
  )
  // 3. Layered fog gradient — before final grade so contrast boost amplifies it
  .replace(
    '    // Final infrared grade: push contrast, desaturate',
    `    // Layered fog gradient: surface glow above, abyss black below
    col = mix(col, vec3(0.25, 0.28, 0.32), smoothstep(0.5, 0.9, dir.y));
    col = mix(col, vec3(0.0), smoothstep(-0.5, -1.0, dir.y));

    // Final infrared grade: push contrast, desaturate`
  )

const UNDERWATER_FRAG = /* glsl */`
uniform vec2  uResolution;
uniform float uTime;

${causticsGLSL}
${underwaterWithCaustics}

void main() {
  vec3 color = underwaterScene(gl_FragCoord.xy, uResolution, uTime);
  gl_FragColor = vec4(color, 1.0);
}`

function UnderwaterBackground() {
  const mat = useMemo(() => new THREE.ShaderMaterial({
    uniforms: {
      uTime:       { value: 0 },
      uResolution: { value: new THREE.Vector2(1, 1) },
    },
    vertexShader:   UNDERWATER_VERT,
    fragmentShader: UNDERWATER_FRAG,
    depthWrite: false,
    depthTest:  false,
  }), [])

  useFrame(({ clock, size }) => {
    mat.uniforms.uTime.value = clock.elapsedTime
    mat.uniforms.uResolution.value.set(size.width, size.height)
  })

  return (
    <mesh renderOrder={-999} frustumCulled={false}>
      <planeGeometry args={[2, 2]} />
      <primitive object={mat} attach="material" />
    </mesh>
  )
}

// Caustic plane removed — getCaustic() is now baked into the underwaterScene()
// rock shading pass via underwaterWithCaustics string injection above.

// ── 5. SURFACE PLANE — water surface at Y=8 ───────────────────────────────────
// MeshStandardMaterial + onBeforeCompile for getwaves() vertex displacement.
// Renamed functions (wavedx_s / getwaves_s) to avoid namespace collisions.

const SURFACE_WAVE_GLSL = /* glsl */`
  uniform float uTime;

  float wavedx_s(vec2 pos, vec2 dir, float time, float freq) {
    float x = dot(dir, pos) * freq + time;
    return exp(sin(x) - 1.0);
  }

  float getwaves_s(vec2 pos, float t) {
    float iter = 0.0; float phase = 6.0; float speed = 2.0;
    float weight = 1.0; float w = 0.0; float ws = 0.0;
    for (int i = 0; i < 5; i++) {
      vec2 p = vec2(sin(iter), cos(iter));
      float res = wavedx_s(pos, p, speed * t, phase);
      w  += res * weight;
      ws += weight;
      iter  += 12.0;
      weight *= 0.75;
      phase  *= 1.18;
      speed  *= 1.08;
    }
    return w / ws;
  }
`

function SurfacePlane() {
  const shaderRef = useRef(null)

  const mat = useMemo(() => {
    const m = new THREE.MeshStandardMaterial({
      color:       new THREE.Color('#c8dde8'),  // cold pale blue-gray
      transparent: true,
      opacity:     0.08,                        // barely visible — just a hint
      side:        THREE.DoubleSide,
    })
    m.onBeforeCompile = (shader) => {
      shader.uniforms.uTime = { value: 0 }
      shaderRef.current = shader
      // Prepend wave functions before the vertex main
      shader.vertexShader = SURFACE_WAVE_GLSL + shader.vertexShader
      // Inject Y displacement after position is set
      shader.vertexShader = shader.vertexShader.replace(
        '#include <begin_vertex>',
        `#include <begin_vertex>
         float waveH = getwaves_s(position.xz * 0.05, uTime) * 0.3;
         transformed.y += waveH;`
      )
    }
    return m
  }, [])

  useFrame(({ clock }) => {
    if (shaderRef.current) shaderRef.current.uniforms.uTime.value = clock.elapsedTime
  })

  return (
    <mesh position={[0, 8, 0]} rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry args={[100, 100, 32, 32]} />
      <primitive object={mat} attach="material" />
    </mesh>
  )
}

// ── 3. PARTICLES — wave-displaced organic movement ────────────────────────────

function Particles() {
  const ref = useRef()
  const COUNT = 200

  const [positions, velocities, phaseOffsets] = useMemo(() => {
    const pos   = new Float32Array(COUNT * 3)
    const vel   = new Float32Array(COUNT)
    const phase = new Float32Array(COUNT)
    for (let i = 0; i < COUNT; i++) {
      pos[i * 3 + 0] = (Math.random() - 0.5) * 20
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10
      pos[i * 3 + 2] = (Math.random() - 0.5) * 15
      vel[i]   = 0.003 + Math.random() * 0.004
      phase[i] = Math.random() * Math.PI * 2
    }
    return [pos, vel, phase]
  }, [])

  useFrame(({ clock }) => {
    if (!ref.current) return
    const t   = clock.elapsedTime
    const arr = ref.current.geometry.attributes.position.array
    for (let i = 0; i < COUNT; i++) {
      const x    = arr[i * 3 + 0]
      const z    = arr[i * 3 + 2]
      const wave = getWaveHeightJS(x, z, t + phaseOffsets[i])
      arr[i * 3 + 1] += velocities[i] + wave * 0.005
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
      <pointsMaterial color="#00d4ff" size={0.02} sizeAttenuation transparent opacity={0.6} />
    </points>
  )
}

// ── 2b. SHARK CAUSTIC INJECTION — getSimpleCaustic() via onBeforeCompile ──────
// Renamed functions (wavedx_c / getwaves_c / getSimpleCaustic_s) to avoid
// collisions with other injected shaders.

const SHARK_CAUSTIC_GLSL = /* glsl */`
  uniform float uCausticTime;

  float wavedx_c(vec2 pos, vec2 dir, float time, float freq) {
    float x = dot(dir, pos) * freq + time;
    return exp(sin(x) - 1.0);
  }

  float getwaves_c(vec2 pos, float t) {
    float iter = 0.0; float phase = 6.0; float speed = 2.0;
    float weight = 1.0; float w = 0.0; float ws = 0.0;
    for (int i = 0; i < 5; i++) {
      vec2 p = vec2(sin(iter), cos(iter));
      float res = wavedx_c(pos, p, speed * t, phase);
      w  += res * weight;
      ws += weight;
      iter  += 12.0;
      weight *= 0.75;
      phase  *= 1.18;
      speed  *= 1.08;
    }
    return w / ws;
  }

  float getSimpleCaustic_s(vec2 uv, float t) {
    vec2 p   = uv * 2.0;
    float w  = getwaves_c(p, t);
    float w2 = getwaves_c(p + vec2(0.5, 0.3), t * 1.1);
    float caustic = abs(w - w2);
    caustic = 1.0 - smoothstep(0.0, 0.3, caustic);
    return caustic * 0.4;
  }
`

// ── Shark ─────────────────────────────────────────────────────────────────────

function Shark({ sharkGroupRef, sharkApiRef }) {
  const { scene, animations } = useGLTF(GLB)
  const { actions, mixer }    = useAnimations(animations, sharkGroupRef)
  const scroll = useScroll()

  const biteRef   = useRef(null)
  const swimRef   = useRef(null)
  const circleRef = useRef(null)
  const biteDur   = useRef(3.5)
  const animState = useRef('none')
  const warnedRef = useRef(false)

  // Shared time uniform object — same reference injected into every patched material
  const causticTime = useMemo(() => ({ value: 0 }), [])

  useFrame(({ clock }) => { causticTime.value = clock.elapsedTime })

  // ── Scene load: visibility fix + caustic injection + bbox log ──
  useEffect(() => {
    console.log('[MEG] GLB scene object:', scene)
    console.log('[MEG] Scene type:', scene?.type, '| visible:', scene?.visible,
                '| children:', scene?.children?.length)
    if (!scene) { console.error('[MEG] scene is null — GLB failed to load'); return }

    requestAnimationFrame(() => {
      if (sharkGroupRef.current) {
        console.log('[MEG] sharkGroupRef scale:',    sharkGroupRef.current.scale)
        console.log('[MEG] sharkGroupRef visible:',  sharkGroupRef.current.visible)
        console.log('[MEG] sharkGroupRef position:', sharkGroupRef.current.position)
      } else {
        console.error('[MEG] sharkGroupRef.current is null after commit!')
      }
    })

    scene.visible = true
    scene.traverse(child => {
      if (!child.visible) {
        console.warn('[MEG] Invisible child found and fixed:', child.name, child.type)
        child.visible = true
      }

      // Inject getSimpleCaustic() additive shimmer on every MeshStandardMaterial.
      // Guarded with try/catch — if injection fails, material falls back unchanged.
      if (child.isMesh && child.material) {
        const mats = Array.isArray(child.material) ? child.material : [child.material]
        mats.forEach(mat => {
          if (!mat.isMeshStandardMaterial || mat.userData._causticPatched) return
          mat.userData._causticPatched = true
          mat.onBeforeCompile = (shader) => {
            try {
              shader.uniforms.uCausticTime = causticTime
              console.log('[MEG] Caustic shader injection on:', mat.name || 'unnamed material')
              // Inject after #include <common> so precision + built-in utils are in scope.
              // Do NOT prepend to the full shader — that puts code before precision statements.
              shader.fragmentShader = shader.fragmentShader.replace(
                '#include <common>',
                `#include <common>\n${SHARK_CAUSTIC_GLSL}`
              )
              // Guard with USE_UV: vUv is only declared when a UV set is active on the mesh.
              // Without this guard, meshes without UV maps produce a compile error → invisible mesh.
              shader.fragmentShader = shader.fragmentShader.replace(
                '#include <emissivemap_fragment>',
                `#include <emissivemap_fragment>
                 #ifdef USE_UV
                   float causticBright = getSimpleCaustic_s(vUv * 2.0, uCausticTime);
                   totalEmissiveRadiance += vec3(causticBright * 0.15);
                 #endif`
              )
            } catch (e) {
              console.error('[MEG] Caustic injection failed — falling back to original material:', e)
            }
          }
          mat.needsUpdate = true
        })
      }
    })

    const box    = new THREE.Box3().setFromObject(scene)
    const size   = new THREE.Vector3()
    const center = new THREE.Vector3()
    box.getSize(size)
    box.getCenter(center)
    console.log('[MEG] Shark bbox size:', size, '| center:', center)
    console.log('[MEG] Shark bbox min:',  box.min, '| max:', box.max)
  }, [scene]) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Resolve clips on load ──
  useEffect(() => {
    if (!actions || !mixer) return
    const keys = Object.keys(actions)
    console.log('[MEG] All GLB clip names:', keys)
    if (keys.length === 0) return

    const bite   = findClip(actions, keys, ['bite', 'attack', 'snap', 'jaw', 'chomp', 'open'])
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

    swim?.reset().play()
    animState.current = 'swim'
    if (sharkApiRef) sharkApiRef.current = { swimAction: swim }
    console.log('[MEG] Initial animation: swim — mesh should be visible now')
  }, [actions, mixer]) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Per-frame: scroll drives bite time; crossfade at 20%; swim↔circle ──
  useFrame(() => {
    const o    = scroll.offset
    const bite = biteRef.current
    const swim = swimRef.current
    const circ = circleRef.current

    if (!sharkGroupRef.current) {
      if (!warnedRef.current) {
        console.warn('[MEG] useFrame: sharkGroupRef.current is null')
        warnedRef.current = true
      }
      return
    }

    if (o < 0.2) {
      if (animState.current !== 'bite' && bite) {
        console.log('[MEG] Entering bite section — switching to manual time control')
        swim?.isRunning() && swim.fadeOut(0.3)
        circ?.isRunning() && circ.fadeOut(0.3)
        bite.reset().play()
        bite.paused = true
        animState.current = 'bite'
      }
      if (bite && animState.current === 'bite') {
        bite.time = Math.min((o / 0.2) * biteDur.current, biteDur.current)
      }
      return
    }

    if (animState.current === 'bite') {
      const inEye  = o < 0.4
      const target = inEye && circ ? circ : swim
      if (bite) bite.paused = false
      target.reset().play()
      bite?.crossFadeTo(target, 0.5, true)
      console.log(`[MEG] Exiting bite section → "${target.getClip().name}"`)
      animState.current = inEye && circ ? 'circle' : 'swim'
    }

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

  return <primitive ref={sharkGroupRef} object={scene} scale={1.5} />
}

// ── Camera — always scroll-driven through all 6 waypoints ────────────────────

function CameraController({ cutsceneActiveRef }) {
  const { camera } = useThree()
  const scroll      = useScroll()
  const lookTarget  = useRef(new THREE.Vector3(0, 0, 0))
  const desiredPos  = useRef(new THREE.Vector3())
  const desiredLook = useRef(new THREE.Vector3())

  useFrame(({ clock }) => {
    if (cutsceneActiveRef.current) return
    const et = clock.elapsedTime
    const o  = scroll.offset
    const wt = o * (WAYPOINTS.length - 1)
    const i  = Math.min(Math.floor(wt), WAYPOINTS.length - 2)
    const frac = wt - i

    desiredPos.current.lerpVectors(WAYPOINTS[i].pos,  WAYPOINTS[i + 1].pos,  frac)
    desiredLook.current.lerpVectors(WAYPOINTS[i].look, WAYPOINTS[i + 1].look, frac)

    // Scroll-driven position — waypoint system unchanged
    camera.position.lerp(desiredPos.current, 0.06)

    // Target drift — look-at oscillates gently around the waypoint target
    lookTarget.current.lerp(desiredLook.current, 0.06)
    lookTarget.current.x += Math.sin(et * 0.15) * 0.04
    lookTarget.current.y += Math.sin(et * 0.22) * 0.02

    // Bob via lookAt offset only — never mutate position or rotation directly
    const bobX = Math.sin(et * 0.25) * 0.12
    const bobY = Math.sin(et * 0.4)  * 0.08
    camera.lookAt(
      lookTarget.current.x + bobX,
      lookTarget.current.y + bobY,
      lookTarget.current.z
    )
  })

  return null
}

// ── Panel opacity — direct DOM, no React re-renders ───────────────────────────

function PanelController({ panelRefs }) {
  const scroll = useScroll()
  const HALF   = 0.11

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

// ── 4. GOD RAYS — post-processing Effect ─────────────────────────────────────
// Adapted from god_rays.glsl for postprocessing Effect API.
// inputBuffer (sampler2D) is auto-injected by the postprocessing library.
// uIntensity tweened 0→1→0 by GSAP on each 20% scroll section boundary.

const GOD_RAYS_FRAG = /* glsl */`
  const int   SAMPLE_COUNT = 24;
  uniform float uTime;
  uniform float uIntensity;

  float hash_gr(vec2 p) {
    return fract(sin(dot(p, vec2(41.0, 289.0))) * 45758.5453);
  }

  vec3 lOff_gr(float t) {
    vec2 u = sin(vec2(1.57, 0.0) - t / 2.0);
    mat2 a = mat2(u.x, u.y, -u.y, u.x);
    vec3 l = normalize(vec3(1.5, 1.0, -0.5));
    l.xz = a * l.xz;
    l.xy = a * l.xy;
    return l;
  }

  void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
    float decay   = 0.97;
    float density = 0.5;
    float weight  = 0.1;
    vec3  l    = lOff_gr(uTime);
    vec2  tuv  = uv - 0.5 - l.xy * 0.45;
    vec2  dTuv = tuv * density / float(SAMPLE_COUNT);

    vec2 uvSample = uv;
    vec4 col = texture(inputBuffer, uvSample) * 0.25;
    uvSample += dTuv * (hash_gr(uvSample + fract(uTime)) * 2.0 - 1.0);

    for (int i = 0; i < SAMPLE_COUNT; i++) {
      uvSample -= dTuv;
      col += texture(inputBuffer, uvSample) * weight;
      weight *= decay;
    }

    col *= (1.0 - dot(tuv, tuv) * 0.75);
    vec4 result = sqrt(smoothstep(vec4(0.0), vec4(1.0), col));

    // Strip blue cast inherited from the scene — convert to luminance then
    float rayLum = dot(result.rgb, vec3(0.299, 0.587, 0.114));
    result.rgb = vec3(rayLum);

    outputColor = mix(inputColor, result, uIntensity);
  }
`

class GodRaysEffectImpl extends Effect {
  constructor() {
    super('GodRaysEffect', GOD_RAYS_FRAG, {
      uniforms: new Map([
        ['uTime',      new THREE.Uniform(0)],
        ['uIntensity', new THREE.Uniform(0.15)], // baseline — never goes fully dark
      ]),
    })
  }
}

const GodRaysPass = wrapEffect(GodRaysEffectImpl)

// Drives god rays uniforms; fires GSAP tween at each 20% scroll boundary.
function GodRaysController({ effectRef }) {
  const scroll      = useScroll()
  const prevSection = useRef(-1)

  useFrame(({ clock }) => {
    const effect = effectRef.current
    if (!effect) return

    effect.uniforms.get('uTime').value = clock.elapsedTime

    const section = Math.floor(scroll.offset * 5)
    if (section !== prevSection.current) {
      prevSection.current = section
      const uni = effect.uniforms.get('uIntensity')
      gsap.killTweensOf(uni)
      // Pulse 0.15 → 0.5 → 0.15 on section boundary — half max, baseline preserved
      gsap.to(uni, { value: 0.5, duration: 0.5, yoyo: true, repeat: 1, ease: 'power2.inOut' })
    }
  })

  return null
}

// ── Logo fly helper — projects shark world pos to screen, spawns img, flies ───
// Called when shark scale drops below 0.05 (nearly invisible).
// The img is appended to body (position: fixed) so it survives canvas hide.

function spawnAndFlyLogo(sharkPos, camera, sw, sh, canvasWrapperRef, dashboardRef) {
  // Project shark world position to normalised device coords → pixels
  const ndc = sharkPos.clone().project(camera)
  const screenX = (ndc.x *  0.5 + 0.5) * sw
  const screenY = (ndc.y * -0.5 + 0.5) * sh

  const img = document.createElement('img')
  img.src = megLogoSrc
  img.className = 'logo-fly'
  img.style.left    = screenX + 'px'
  img.style.top     = screenY + 'px'
  img.style.opacity = '0'
  document.body.appendChild(img)

  // Fade in + fly to fixed top-left corner simultaneously
  gsap.to(img, {
    top:      20,
    left:     20,
    opacity:  1,
    duration: 0.5,
    ease:     'power2.inOut',
    onComplete: () => {
      // Hide 3D canvas once logo has landed
      if (canvasWrapperRef?.current) {
        canvasWrapperRef.current.style.display = 'none'
      }
      // Reveal dashboard behind the now-permanent logo
      if (dashboardRef?.current) {
        dashboardRef.current.style.display = 'block'
        gsap.fromTo(
          dashboardRef.current,
          { opacity: 0 },
          { opacity: 1, duration: 0.5, ease: 'power2.inOut' }
        )
      }
    },
  })
}

// ── Cutscene — fires once when user scrolls past 0.97 with downward velocity ──
// Trigger: offset >= 0.97 AND current - prev > 0 (actively scrolling down).
// hasFiredRef: refresh is the only replay.
// cutsceneActiveRef: disables CameraController so camera freezes.
// Scroll lock: scroll.el overflow set to hidden on fire.

function CutsceneController({ sharkGroupRef, sharkApiRef, cutsceneActiveRef, canvasWrapperRef, dashboardRef }) {
  const scroll      = useScroll()
  const { camera, size } = useThree()
  const hasFiredRef = useRef(false)
  const prevOffset  = useRef(0)

  useFrame(() => {
    const cur  = scroll.offset
    const prev = prevOffset.current
    prevOffset.current = cur

    if (hasFiredRef.current) return

    // Only fire when user is actively scrolling down past the end
    const velocity = cur - prev
    if (cur < 0.97 || velocity <= 0) return

    hasFiredRef.current       = true
    cutsceneActiveRef.current = true

    // Lock scroll immediately — prevent scrolling back during cutscene
    if (scroll.el) {
      scroll.el.style.overflow      = 'hidden'
      scroll.el.style.pointerEvents = 'none'
    }

    // Capture canvas dimensions at fire time (reactive size object)
    const sw = size.width
    const sh = size.height

    // Ensure swim animation is playing
    const swimAction = sharkApiRef.current?.swimAction
    if (swimAction && !swimAction.isRunning()) swimAction.reset().play()

    const tl = gsap.timeline()
    let logoSpawned = false

    if (sharkGroupRef.current) {
      const startX = sharkGroupRef.current.position.x
      const startY = sharkGroupRef.current.position.y
      const startZ = sharkGroupRef.current.position.z

      // No rotation — shark already shows its tail at section 5.
      // Swim straight away: +Z (positive = behind camera), slight left drift,
      // slight rise, shrinks to nothing over 3.5 seconds.
      tl.to(sharkGroupRef.current.position, {
        z: startZ + 150,
        x: startX - 8,
        y: startY + 4,
        duration: 3.5,
        ease: 'power1.in',
      }, 0)

      tl.to(sharkGroupRef.current.scale, {
        x: 0.0,
        y: 0.0,
        z: 0.0,
        duration: 3.5,
        ease: 'power1.in',
        onUpdate() {
          // Spawn logo exactly when shark becomes nearly invisible
          if (!logoSpawned && sharkGroupRef.current && sharkGroupRef.current.scale.x < 0.05) {
            logoSpawned = true
            spawnAndFlyLogo(
              sharkGroupRef.current.position,
              camera, sw, sh,
              canvasWrapperRef, dashboardRef
            )
          }
        },
      }, 0)
    }

    // Canvas fades out as the shark vanishes (starts at 2.8s, 1s fade)
    if (canvasWrapperRef?.current) {
      tl.to(canvasWrapperRef.current, {
        opacity: 0,
        duration: 1,
        ease: 'power2.inOut',
      }, 2.8)
    }
  })

  return null
}

// ── Scene root ────────────────────────────────────────────────────────────────

export default function Scene({ panelRefs, canvasWrapperRef, dashboardRef }) {
  const godRaysRef        = useRef()
  const sharkGroupRef     = useRef()
  const cutsceneActiveRef = useRef(false)
  const sharkApiRef       = useRef({ swimAction: null })

  return (
    <>
      {/* Null scene.background so the fullscreen quad renders through */}
      <SceneSetup />

      {/* Raymarched underwater cave environment — renders at far plane depth */}
      <UnderwaterBackground />

      {/* Fog at 0.025 density: shark reads as dark silhouette against lit background.
          Color matches the deep water base in the shader (#041520). */}
      <fogExp2 attach="fog" args={['#041520', 0.025]} />

      {/* Ambient kept very low so directional light dominates — real shadow contrast */}
      <ambientLight color="#030810" intensity={0.15} />
      {/* Broad cold fill from above — general underwater feel */}
      <directionalLight position={[5, 20, 0]} color="#8ba8c0" intensity={0.6} />
      {/* Primary key light: above-right, strong — bright top edge, near-black belly */}
      <directionalLight position={[3, 12, 5]} color="#c8d8e8" intensity={0.9} />
      {/* Soft bloom at surface level — simulates refraction through Y=8 */}
      <pointLight position={[0, 8, 0]} color="#c8dde8" intensity={0.3} distance={30} />

      {/* Semi-transparent water surface above the shark */}
      <SurfacePlane />

      {/* Wave-displaced particles */}
      <Particles />

      <Suspense fallback={null}>
        <Shark sharkGroupRef={sharkGroupRef} sharkApiRef={sharkApiRef} />
      </Suspense>

      <CameraController cutsceneActiveRef={cutsceneActiveRef} />
      <PanelController panelRefs={panelRefs} />

      {/* God rays controller — reads effectRef, drives GSAP on scroll boundary */}
      <GodRaysController effectRef={godRaysRef} />

      {/* Cutscene — fires once at scroll 0.97 with downward velocity, shark swims to logo */}
      <CutsceneController
        sharkGroupRef={sharkGroupRef}
        sharkApiRef={sharkApiRef}
        cutsceneActiveRef={cutsceneActiveRef}
        canvasWrapperRef={canvasWrapperRef}
        dashboardRef={dashboardRef}
      />

      {/* Post-processing stack: desaturate → contrast → god rays flash */}
      <EffectComposer>
        <HueSaturation saturation={-0.65} />
        <BrightnessContrast contrast={0.15} />
        <GodRaysPass ref={godRaysRef} />
      </EffectComposer>
    </>
  )
}
