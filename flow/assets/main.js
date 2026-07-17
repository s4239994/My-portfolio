import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

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

// ---------- scene setup ----------
const canvas = document.getElementById("scene-canvas");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 12, 18);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1, 0);
controls.enableDamping = true;
controls.minDistance = 8;
controls.maxDistance = 32;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();

const hemi = new THREE.HemisphereLight(0xbde3ff, 0x8bd17a, 0.9);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xffffff, 1.3);
sun.position.set(10, 18, 8);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
scene.add(sun);

const ground = new THREE.Mesh(
  new THREE.CircleGeometry(16, 48),
  new THREE.MeshStandardMaterial({ color: 0x8bd17a, roughness: 0.9 })
);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

const path = new THREE.Mesh(
  new THREE.RingGeometry(RADIUS - 0.6, RADIUS + 0.6, 64),
  new THREE.MeshStandardMaterial({ color: 0xf0d9a8, roughness: 1 })
);
path.rotation.x = -Math.PI / 2;
path.position.y = 0.01;
scene.add(path);

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
    new THREE.CylinderGeometry(1.1, 1.2, 0.4, 16),
    new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 })
  );
  base.position.set(x, 0.2, z);
  base.castShadow = true;
  base.receiveShadow = true;
  scene.add(base);

  const tower = new THREE.Mesh(
    new THREE.BoxGeometry(1.5, 1, 1.5),
    new THREE.MeshStandardMaterial({ color: COLORS[statusOf(wait)], roughness: 0.5 })
  );
  tower.position.set(x, 0.9, z);
  tower.castShadow = true;
  tower.userData.id = a.id;
  scene.add(tower);
  meshes.push(tower);

  const label = makeTextSprite(a.name);
  label.position.set(x, 2, z);
  scene.add(label);

  state[a.id].towerMesh = tower;
  state[a.id].labelMesh = label;
}

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

// ---------- click / raycast ----------
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
renderer.domElement.addEventListener("click", (event) => {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(meshes);
  if (hits.length > 0) {
    selectAttraction(hits[0].object.userData.id);
  }
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
function animate() {
  requestAnimationFrame(animate);
  for (const a of ATTRACTIONS) {
    const s = state[a.id];
    s.targetHeight = 0.6 + s.targetWait / 8;
    s.height += (s.targetHeight - s.height) * 0.08;
    s.towerMesh.scale.y = s.height;
    s.towerMesh.position.y = 0.4 + (s.height * 1) / 2;
    s.labelMesh.position.y = 0.4 + s.height + 1.1;
    const targetColor = new THREE.Color(COLORS[statusOf(s.targetWait)]);
    s.towerMesh.material.color.lerp(targetColor, 0.05);
  }
  controls.update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
