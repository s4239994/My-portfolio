import streamlit.components.v1 as components

_ENGINE_JS = r"""
<div id="wrap" style="width:100%; height:HEIGHTpx; border-radius:24px; overflow:hidden; position:relative;">
<canvas id="c" style="width:100%; height:100%; display:block;"></canvas>
</div>
<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const wrap = document.getElementById('wrap');
const TYPE = "TYPE_PLACEHOLDER";
const INTENSITY = INTENSITY_PLACEHOLDER;
const COLOR = "COLOR_PLACEHOLDER";

function resize() {
  canvas.width = wrap.clientWidth;
  canvas.height = wrap.clientHeight;
}
resize();
window.addEventListener('resize', resize);

function hexToRgb(hex) {
  const v = parseInt(hex.slice(1), 16);
  return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
}
const [R, G, B] = hexToRgb(COLOR);

let particles = [];
const COUNT = Math.round(30 + INTENSITY * 90);

function rand(a, b) { return a + Math.random() * (b - a); }

function initParticles() {
  particles = [];
  for (let i = 0; i < COUNT; i++) {
    if (TYPE === 'storm') {
      particles.push({ x: rand(0, canvas.width), y: rand(-canvas.height, canvas.height),
                        len: rand(10, 26), speed: rand(6, 14) * (0.3 + INTENSITY) });
    } else if (TYPE === 'fog') {
      particles.push({ x: rand(0, canvas.width), y: rand(0, canvas.height),
                        r: rand(30, 90), dx: rand(-0.3, 0.3), dy: rand(-0.15, 0.15),
                        phase: rand(0, Math.PI * 2) });
    } else if (TYPE === 'wave') {
      particles.push({ baseY: rand(0, canvas.height), phase: rand(0, Math.PI * 2),
                        speed: rand(0.01, 0.03), amp: rand(6, 22) * (0.3 + INTENSITY),
                        x: rand(0, canvas.width) });
    } else if (TYPE === 'static') {
      particles.push({ x: rand(0, canvas.width), y: rand(0, canvas.height),
                        size: rand(1, 3), life: rand(0, 1) });
    } else if (TYPE === 'calm') {
      particles.push({ x: rand(0, canvas.width), y: rand(0, canvas.height),
                        r: rand(18, 50), dx: rand(-0.15, 0.15), dy: rand(-0.15, 0.15),
                        phase: rand(0, Math.PI * 2) });
    } else if (TYPE === 'stars') {
      particles.push({ x: rand(0, canvas.width), y: rand(0, canvas.height),
                        r: rand(1, 2.6), phase: rand(0, Math.PI * 2), speed: rand(0.02, 0.05) });
    } else {
      particles.push({ x: rand(0, canvas.width), y: rand(-40, canvas.height * 0.3),
                        r: rand(3, 7), vy: rand(0.4, 1.2), settled: false });
    }
  }
}
initParticles();

let flashAlpha = 0;
let t = 0;

function draw() {
  t += 1;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (TYPE === 'stars') {
    ctx.fillStyle = 'rgba(18,18,42,1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  } else {
    const bgAlpha = 0.06 + INTENSITY * 0.10;
    ctx.fillStyle = `rgba(${R},${G},${B},${bgAlpha})`;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  if (TYPE === 'storm') {
    if (Math.random() < 0.004 + INTENSITY * 0.02) flashAlpha = 0.5;
    if (flashAlpha > 0) {
      ctx.fillStyle = `rgba(255,255,255,${flashAlpha})`;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      flashAlpha -= 0.05;
    }
    ctx.strokeStyle = `rgba(${R},${G},${B},${0.25 + INTENSITY * 0.5})`;
    ctx.lineWidth = 1.5;
    for (const p of particles) {
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(p.x - 4, p.y + p.len);
      ctx.stroke();
      p.y += p.speed;
      p.x -= p.speed * 0.25;
      if (p.y > canvas.height) { p.y = -20; p.x = rand(0, canvas.width); }
    }
  } else if (TYPE === 'fog') {
    for (const p of particles) {
      const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
      const a = (0.12 + INTENSITY * 0.22);
      grad.addColorStop(0, `rgba(${R},${G},${B},${a})`);
      grad.addColorStop(1, `rgba(${R},${G},${B},0)`);
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
      p.x += p.dx * (0.3 + INTENSITY);
      p.y += p.dy + Math.sin(t * 0.01 + p.phase) * 0.2;
      if (p.x < -100) p.x = canvas.width + 100;
      if (p.x > canvas.width + 100) p.x = -100;
    }
  } else if (TYPE === 'wave') {
    ctx.strokeStyle = `rgba(${R},${G},${B},${0.35 + INTENSITY * 0.4})`;
    ctx.lineWidth = 2;
    const rows = 5;
    for (let r = 0; r < rows; r++) {
      ctx.beginPath();
      const baseY = canvas.height * ((r + 1) / (rows + 1));
      for (let x = 0; x <= canvas.width; x += 6) {
        const y = baseY + Math.sin(x * 0.02 + t * (0.02 + INTENSITY * 0.03) + r) * (8 + INTENSITY * 18);
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
  } else if (TYPE === 'static') {
    const density = 0.02 + INTENSITY * 0.18;
    for (let i = 0; i < canvas.width * canvas.height * density / 400; i++) {
      const x = rand(0, canvas.width), y = rand(0, canvas.height);
      const shade = Math.random() * 255;
      ctx.fillStyle = `rgba(${shade},${shade},${shade},${0.5 + Math.random() * 0.5})`;
      ctx.fillRect(x, y, 2, 2);
    }
  } else if (TYPE === 'calm') {
    for (const p of particles) {
      const pulse = 0.5 + 0.5 * Math.sin(t * 0.02 + p.phase);
      const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
      const a = (0.10 + INTENSITY * 0.15) * pulse;
      grad.addColorStop(0, `rgba(${R},${G},${B},${a})`);
      grad.addColorStop(1, `rgba(${R},${G},${B},0)`);
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
      p.x += p.dx; p.y += p.dy;
      if (p.x < -60) p.x = canvas.width + 60;
      if (p.x > canvas.width + 60) p.x = -60;
      if (p.y < -60) p.y = canvas.height + 60;
      if (p.y > canvas.height + 60) p.y = -60;
    }
  } else if (TYPE === 'stars') {
    for (const p of particles) {
      const twinkle = 0.3 + 0.7 * Math.abs(Math.sin(t * p.speed + p.phase));
      ctx.fillStyle = `rgba(255,255,255,${twinkle})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
  } else {
    for (const p of particles) {
      ctx.beginPath();
      const a = p.settled ? 0.15 : (0.3 + INTENSITY * 0.4);
      ctx.fillStyle = `rgba(${R},${G},${B},${a})`;
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
      const floorY = canvas.height * (0.55 + (1 - INTENSITY) * 0.3);
      if (INTENSITY > 0.35) {
        p.y += p.vy;
        if (p.y > floorY) { p.y = floorY; p.settled = true; }
      } else {
        p.y -= p.vy * 0.4;
        if (p.y < -20) p.y = canvas.height + 20;
      }
    }
  }

  requestAnimationFrame(draw);
}
draw();
</script>
"""


def render_scene(metaphor_key: str, color: str, intensity: float, height: int = 260):
    intensity = max(0.0, min(1.0, intensity))
    html = (
        _ENGINE_JS.replace("HEIGHT", str(height))
        .replace("TYPE_PLACEHOLDER", metaphor_key)
        .replace("INTENSITY_PLACEHOLDER", str(round(intensity, 3)))
        .replace("COLOR_PLACEHOLDER", color)
    )
    components.html(html, height=height + 10, scrolling=False)
