import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";

const ATTRACTIONS = [
  { id: "trampolines", name: "Main Arena Trampolines", angle: 0 },
  { id: "ninja", name: "Ninja Warrior Course", angle: 45 },
  { id: "foampit", name: "Foam Pit", angle: 90 },
  { id: "dodgeball", name: "Dodgeball Court", angle: 135 },
  { id: "toddler", name: "Toddler Zone", angle: 180 },
  { id: "climbing", name: "Climbing Wall", angle: 225 },
  { id: "battlebeam", name: "Battle Beam", angle: 270 },
  { id: "arcade", name: "Arcade", angle: 315 },
];

const RADIUS = 9;
const COLORS = { low: 0x22c55e, mid: 0xf59e0b, high: 0xef4444 };
const COLORS_HEX = { low: "#22c55e", mid: "#f59e0b", high: "#ef4444" };

function statusOf(wait) {
  if (wait < 15) return "low";
  if (wait < 30) return "mid";
  return "high";
}

function makeTextSprite(text) {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 64;
  const ctx = canvas.getContext("2d");
  ctx.font = "bold 26px 'Work Sans', sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.lineWidth = 5;
  ctx.strokeStyle = "rgba(22,33,58,0.85)";
  ctx.strokeText(text, canvas.width / 2, canvas.height / 2);
  ctx.fillStyle = "#ffffff";
  ctx.fillText(text, canvas.width / 2, canvas.height / 2);
  const texture = new THREE.CanvasTexture(canvas);
  const material = new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false });
  const sprite = new THREE.Sprite(material);
  sprite.scale.set(3.2, 0.8, 1);
  return sprite;
}

function makeGrassTexture() {
  const size = 512;
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "#7fc96b";
  ctx.fillRect(0, 0, size, size);
  const shades = ["#8bd17a", "#74bd63", "#93d982"];
  for (let i = 0; i < 900; i++) {
    ctx.fillStyle = shades[i % shades.length];
    const x = Math.random() * size;
    const y = Math.random() * size;
    const r = 2 + Math.random() * 5;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }
  return new THREE.CanvasTexture(canvas);
}

function makeTree(x, z) {
  const group = new THREE.Group();
  const trunk = new THREE.Mesh(
    new THREE.CylinderGeometry(0.14, 0.18, 1, 8),
    new THREE.MeshStandardMaterial({ color: 0x8a5a3b, roughness: 0.9 })
  );
  trunk.position.y = 0.5;
  trunk.castShadow = true;
  group.add(trunk);

  const leafColors = [0x4fae5e, 0x59c26a, 0x3f9a4f];
  const leaf = new THREE.Mesh(
    new THREE.ConeGeometry(0.75, 1.6, 8),
    new THREE.MeshStandardMaterial({ color: leafColors[Math.floor(Math.random() * leafColors.length)], roughness: 0.8 })
  );
  leaf.position.y = 1.6;
  leaf.castShadow = true;
  group.add(leaf);

  group.position.set(x, 0, z);
  group.scale.setScalar(0.8 + Math.random() * 0.6);
  return group;
}

// ---------- scene setup ----------
const canvasEl = document.getElementById("scene-canvas");
const renderer = new THREE.WebGLRenderer({ canvas: canvasEl, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0xbfe6ff, 22, 42);

const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 12, 18);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1, 0);
controls.enableDamping = true;
controls.minDistance = 8;
controls.maxDistance = 32;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.6;
controls.update();
controls.addEventListener("start", () => {
  controls.autoRotate = false;
});

const hemi = new THREE.HemisphereLight(0xbde3ff, 0x8bd17a, 0.9);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff3d6, 1.4);
sun.position.set(10, 18, 8);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
scene.add(sun);

const ground = new THREE.Mesh(
  new THREE.CircleGeometry(17, 64),
  new THREE.MeshStandardMaterial({ map: makeGrassTexture(), roughness: 0.95 })
);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

const path = new THREE.Mesh(
  new THREE.RingGeometry(RADIUS - 0.7, RADIUS + 0.7, 64),
  new THREE.MeshStandardMaterial({ color: 0xf0d9a8, roughness: 1 })
);
path.rotation.x = -Math.PI / 2;
path.position.y = 0.01;
path.receiveShadow = true;
scene.add(path);

// scattered decorative trees, kept clear of the ring and its attractions
for (let i = 0; i < 16; i++) {
  const angle = Math.random() * Math.PI * 2;
  const r = 12.5 + Math.random() * 3.5;
  scene.add(makeTree(Math.cos(angle) * r, Math.sin(angle) * r));
}

// ---------- attractions ----------
const state = {};
const meshes = [];

for (const a of ATTRACTIONS) {
  const rad = (a.angle * Math.PI) / 180;
  const x = Math.cos(rad) * RADIUS;
  const z = Math.sin(rad) * RADIUS;

  const wait = Math.floor(Math.random() * 40) + 3;
  state[a.id] = { ...a, x, z, wait, targetWait: wait, height: 0, targetHeight: 0 };

  const base = new THREE.Mesh(
    new THREE.CylinderGeometry(1.1, 1.2, 0.4, 20),
    new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 })
  );
  base.position.set(x, 0.2, z);
  base.castShadow = true;
  base.receiveShadow = true;
  scene.add(base);

  const towerColor = COLORS[statusOf(wait)];
  const tower = new THREE.Mesh(
    new RoundedBoxGeometry(1.5, 1, 1.5, 3, 0.15),
    new THREE.MeshStandardMaterial({
      color: towerColor,
      emissive: towerColor,
      emissiveIntensity: 0.45,
      roughness: 0.4,
    })
  );
  tower.position.set(x, 0.9, z);
  tower.castShadow = true;
  tower.userData.id = a.id;
  tower.userData.baseScale = 1;
  scene.add(tower);
  meshes.push(tower);

  const roof = new THREE.Mesh(
    new THREE.ConeGeometry(1.15, 0.7, 6),
    new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.5 })
  );
  roof.castShadow = true;
  scene.add(roof);

  const label = makeTextSprite(a.name);
  label.position.set(x, 2, z);
  scene.add(label);

  state[a.id].towerMesh = tower;
  state[a.id].labelMesh = label;
  state[a.id].roofMesh = roof;
}

// ---------- postprocessing (bloom) ----------
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  0.55, // strength
  0.5, // radius
  0.25 // threshold
);
composer.addPass(bloomPass);

// ---------- UI wiring ----------
const listEl = document.getElementById("attraction-list");
const capacityEl = document.getElementById("stat-capacity");
const detailPanel = document.getElementById("detail-panel");
const detailName = document.getElementById("detail-name");
const detailWait = document.getElementById("detail-wait");
const detailCapacity = document.getElementById("detail-capacity");
const detailStatus = document.getElementById("detail-status");
document.getElementById("detail-close").addEventListener("click", () => {
  detailPanel.classList.remove("visible");
  activeId = null;
  renderList();
});

let activeId = null;
let hoveredId = null;

function capacityFor(wait) {
  return Math.min(100, Math.round(wait * 2.2));
}

function renderList() {
  listEl.innerHTML = "";
  for (const a of ATTRACTIONS) {
    const s = state[a.id];
    const status = statusOf(s.wait);
    const row = document.createElement("div");
    row.className = "attraction-row" + (activeId === a.id ? " active" : "");
    row.innerHTML = `
      <span class="status-dot" style="background:${COLORS_HEX[status]};"></span>
      <div class="attraction-info">
        <div class="attraction-name">${a.name}</div>
        <div class="attraction-wait">${s.wait} min wait</div>
        <div class="wait-bar-track"><div class="wait-bar-fill" style="width:${capacityFor(s.wait)}%; background:${COLORS_HEX[status]};"></div></div>
      </div>
    `;
    row.addEventListener("click", () => selectAttraction(a.id));
    row.addEventListener("mouseenter", () => (hoveredId = a.id));
    row.addEventListener("mouseleave", () => (hoveredId = null));
    listEl.appendChild(row);
  }
}

function selectAttraction(id) {
  activeId = id;
  const s = state[id];
  const status = statusOf(s.wait);
  detailName.textContent = s.name;
  detailWait.textContent = `Wait: ${s.wait} min`;
  detailCapacity.textContent = `Capacity: ${capacityFor(s.wait)}%`;
  detailStatus.textContent = status === "low" ? "Short wait" : status === "mid" ? "Moderate" : "Long wait";
  detailStatus.style.background = COLORS_HEX[status];
  detailPanel.classList.add("visible");
  renderList();
}

function updateCapacityStat() {
  const avg = Math.round(
    ATTRACTIONS.reduce((sum, a) => sum + capacityFor(state[a.id].wait), 0) / ATTRACTIONS.length
  );
  capacityEl.textContent = `${avg}%`;
}

// ---------- click / hover raycast ----------
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

function updatePointer(event) {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
}

renderer.domElement.addEventListener("click", (event) => {
  updatePointer(event);
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(meshes);
  if (hits.length > 0) {
    selectAttraction(hits[0].object.userData.id);
  }
});

renderer.domElement.addEventListener("mousemove", (event) => {
  updatePointer(event);
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(meshes);
  hoveredId = hits.length > 0 ? hits[0].object.userData.id : null;
  renderer.domElement.style.cursor = hoveredId ? "pointer" : "grab";
});

// ---------- live simulation ----------
function tickSimulation() {
  for (const a of ATTRACTIONS) {
    const s = state[a.id];
    const drift = Math.floor(Math.random() * 13) - 6;
    s.targetWait = Math.max(2, Math.min(55, s.wait + drift));
  }
}
setInterval(() => {
  tickSimulation();
  for (const a of ATTRACTIONS) {
    const s = state[a.id];
    s.wait = s.targetWait;
  }
  renderList();
  updateCapacityStat();
  if (activeId) selectAttraction(activeId);
}, 3200);

renderList();
updateCapacityStat();

// ---------- render loop ----------
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();

  for (const a of ATTRACTIONS) {
    const s = state[a.id];
    s.targetHeight = 0.6 + s.targetWait / 8;
    s.height += (s.targetHeight - s.height) * 0.08;
    s.towerMesh.scale.y = s.height;
    s.towerMesh.position.y = 0.4 + (s.height * 1) / 2 + Math.sin(t * 1.5 + s.x) * 0.03;
    s.roofMesh.position.set(s.x, 0.4 + s.height + 0.35, s.z);
    s.labelMesh.position.y = 0.4 + s.height + 1.1;

    const targetColor = new THREE.Color(COLORS[statusOf(s.targetWait)]);
    s.towerMesh.material.color.lerp(targetColor, 0.05);
    s.towerMesh.material.emissive.lerp(targetColor, 0.05);

    const isHot = a.id === hoveredId || a.id === activeId;
    const targetScaleXZ = isHot ? 1.12 : 1;
    s.towerMesh.scale.x += (targetScaleXZ - s.towerMesh.scale.x) * 0.15;
    s.towerMesh.scale.z += (targetScaleXZ - s.towerMesh.scale.z) * 0.15;
  }

  controls.update();
  composer.render();
}
animate();

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  composer.setSize(window.innerWidth, window.innerHeight);
});
