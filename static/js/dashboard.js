/* ============================================================
   SmartFarm Dashboard JS — polls /status and updates UI
   ============================================================ */

const POLL_INTERVAL = 2000;  // ms between status checks
let prevPerson = null;

/* ── Clock ─────────────────────────────────────────────── */
function updateClock() {
  const now = new Date();
  document.getElementById('sysClock').textContent =
    now.toLocaleTimeString('en-US', { hour12: false });
  document.getElementById('sysDate').textContent =
    now.toISOString().slice(0, 10);
}
setInterval(updateClock, 1000);
updateClock();

/* ── Toast notification ─────────────────────────────────── */
function showToast(msg, duration = 4000) {
  const toast = document.getElementById('toast');
  document.getElementById('toastMsg').textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), duration);
}

/* ── Image loader helper ─────────────────────────────────── */
function loadImage(imgEl, overlayEl, src) {
  if (!src) return;
  const url = `/${src}?t=${Date.now()}`;   // cache-bust
  imgEl.classList.remove('loaded');
  overlayEl.classList.remove('hidden');

  const tmp = new Image();
  tmp.onload = () => {
    imgEl.src = url;
    imgEl.classList.add('loaded');
    overlayEl.classList.add('hidden');
  };
  tmp.onerror = () => {
    overlayEl.classList.remove('hidden');
  };
  tmp.src = url;
}

/* ── Update entire dashboard from status JSON ─────────────── */
function applyStatus(data) {
  const person = data.person_detected;
  const motion = data.motion_detected;
  const sensor = data.motion_source || 'PIR';

  /* --- Live indicator --- */
  const dot   = document.getElementById('liveDot');
  const label = document.getElementById('liveLabel');
  dot.className   = 'pulse-dot ' + (person ? 'danger' : (motion ? 'live' : ''));
  label.textContent = person ? 'THREAT DETECTED' : (motion ? 'MOTION TRIGGERED' : 'LIVE MONITORING');

  /* --- Alert block --- */
  const block = document.getElementById('alertBlock');
  const icon  = document.getElementById('alertIcon');
  const stTxt = document.getElementById('statusText');

  block.className = 'stat-block ' + (person ? 'danger' : (data.total_frames > 0 ? 'safe' : ''));
  icon.textContent = person ? '▲' : (data.total_frames > 0 ? '●' : '●');
  stTxt.textContent = person ? 'HUMAN DETECTED' : (data.total_frames > 0 ? 'CLEAR' : 'WAITING');

  /* --- Motion block --- */
  const motionBlock = document.getElementById('motionBlock');
  const motionIcon  = document.getElementById('motionIcon');
  const motionText  = document.getElementById('motionText');
  const motionLabel = document.getElementById('motionLabel');

  motionBlock.className = 'stat-block ' + (motion ? 'danger' : '');
  motionIcon.textContent = motion ? '⚠' : '●';
  motionText.textContent = motion ? `${sensor} TRIGGERED` : 'NO MOTION';
  motionLabel.textContent = motion ? data.last_event || 'PIR sensor alert' : 'PIR Sensor Status';

  /* --- Feed cards border --- */
  document.getElementById('feedOriginal').className = 'feed-card' + (person ? ' danger' : '');
  document.getElementById('feedResult').className   = 'feed-card' + (person ? ' danger' : '');

  /* --- Alert banner --- */
  const banner = document.getElementById('alertBanner');
  const msg    = document.getElementById('alertMsg');
  if (person) {
    banner.className = 'alert-banner danger';
    msg.textContent  = '⚠  INTRUSION ALERT — HUMAN PRESENCE CONFIRMED ON PREMISES';
  } else if (motion) {
    banner.className = 'alert-banner danger';
    msg.textContent  = `⚠  ${sensor.toUpperCase()} MOTION — ${data.last_event || 'sensor triggered'}`;
  } else if (data.total_frames > 0) {
    banner.className = 'alert-banner safe';
    msg.textContent  = '✓  ALL CLEAR — NO HUMAN DETECTED IN MONITORED ZONE';
  } else {
    banner.className = 'alert-banner';
    msg.textContent  = 'SYSTEM READY — AWAITING CAMERA FEED FROM ESP32-CAM';
  }

  /* --- Stats --- */
  document.getElementById('totalFrames').textContent    = data.total_frames;
  document.getElementById('detectionCount').textContent = data.detection_count;

  const rate = data.total_frames > 0
    ? Math.round((data.detection_count / data.total_frames) * 100) + '%'
    : '0%';
  document.getElementById('detectionRate').textContent = rate;

  /* --- Last updated --- */
  document.getElementById('lastUpdated').textContent = data.last_updated || '—';

  /* --- Feed images --- */
  const imgOrig = document.getElementById('imgOriginal');
  const ovOrig  = document.getElementById('overlayOrig');
  const imgRes  = document.getElementById('imgResult');
  const ovRes   = document.getElementById('overlayRes');
  const pathOrig = document.getElementById('origPath');
  const pathRes  = document.getElementById('resPath');

  if (data.original) {
    loadImage(imgOrig, ovOrig, data.original);
    pathOrig.textContent = data.original;
  }
  if (data.result) {
    loadImage(imgRes, ovRes, data.result);
    pathRes.textContent = data.result;
  }

  /* --- Toast on new detection --- */
  if (prevPerson === false && person === true) {
    showToast('🚨 Human detected! Telegram alert sent.', 5000);
  } else if (prevPerson === true && person === false) {
    showToast('✅ Area is now clear.', 3000);
  }

  prevPerson = person;
}

/* ── Poll /status endpoint ───────────────────────────────── */
async function fetchStatus() {
  try {
    const resp = await fetch('/status');
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const data = await resp.json();
    applyStatus(data);
  } catch (err) {
    console.warn('[SmartFarm] Status fetch error:', err.message);
    document.getElementById('liveDot').className   = 'pulse-dot';
    document.getElementById('liveLabel').textContent = 'CONNECTION ERROR';
  }
}

/* Kick off */
fetchStatus();
setInterval(fetchStatus, POLL_INTERVAL);
