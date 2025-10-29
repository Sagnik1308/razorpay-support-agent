const API_BASE = "http://127.0.0.1:8000";
const chatEl = document.getElementById("chat");
const inputEl = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const escalateBtn = document.getElementById("escalateBtn");

const sheetPanel = document.getElementById("sheetPanel");
const nameInput = document.getElementById("nameInput");
const emailInput = document.getElementById("emailInput");
const issueInput = document.getElementById("issueInput");
const cancelEscalation = document.getElementById("cancelEscalation");
const submitEscalation = document.getElementById("submitEscalation");
const sheetResult = document.getElementById("sheetResult");
const statusEl = document.getElementById("status");

// Simple session id
const sessionId = "sess_" + Math.random().toString(36).slice(2, 10);

// Health check
fetch(`${API_BASE}/health`).then(r => r.ok ? "ok" : "down").then(s => {
  statusEl.textContent = `backend: ${s}`;
}).catch(() => statusEl.textContent = "backend: down");

function appendMessage(text, who = "bot") {
  const wrap = document.createElement("div");
  wrap.className = `msg ${who}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = text.replace(/\n/g, "<br/>");
  wrap.appendChild(bubble);
  chatEl.appendChild(wrap);
  chatEl.scrollTop = chatEl.scrollHeight;
}

async function sendMessage() {
  const msg = inputEl.value.trim();
  if (!msg) return;
  inputEl.value = "";
  appendMessage(msg, "user");

  sendBtn.disabled = true;
  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message: msg })
    });
    if (!res.ok) {
      appendMessage("Sorry, I couldn't reach the server. Please try again.", "bot");
      return;
    }
    const data = await res.json();
    appendMessage(data.answer || "I couldn't find that. Would you like to talk to a human?", "bot");

    // show sources (optional)
    if (data.sources && data.sources.length) {
      const meta = document.createElement("div");
      meta.className = "meta";
      meta.innerHTML = "Sources: " + data.sources.map(s => `<a href="${s.url}" target="_blank">${new URL(s.url).hostname}</a>`).join(" · ");
      chatEl.lastElementChild.appendChild(meta);
    }

    // enable escalation suggestion
    if (data.escalatable) {
      escalateBtn.disabled = false;
    }
  } catch (e) {
    appendMessage("Network error. Please try again.", "bot");
  } finally {
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener("click", sendMessage);
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

// Escalation panel controls
escalateBtn.addEventListener("click", () => {
  sheetPanel.classList.remove("hidden");
  nameInput.focus();
  // Pre-fill user's last message as issue if empty
  if (!issueInput.value) {
    const bubbles = [...document.querySelectorAll(".msg.user .bubble")];
    const last = bubbles.at(-1);
    if (last) issueInput.value = last.textContent.trim();
  }
});

cancelEscalation.addEventListener("click", () => {
  sheetPanel.classList.add("hidden");
  sheetResult.textContent = "";
});

submitEscalation.addEventListener("click", async () => {
  const name = nameInput.value.trim();
  const email = emailInput.value.trim();
  const issue = issueInput.value.trim();
  if (!name || !email || !issue) {
    sheetResult.style.color = "#fecaca";
    sheetResult.textContent = "Please fill all fields.";
    return;
  }
  submitEscalation.disabled = true;
  try {
    const res = await fetch(`${API_BASE}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, question: issue, session_id: sessionId })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      sheetResult.style.color = "#a7f3d0";
      sheetResult.textContent = "Logged! Our human agent will reach out soon.";
      appendMessage(`Thanks ${name}! I’ve sent your details to our support team at ${email}.`, "bot");
      setTimeout(() => sheetPanel.classList.add("hidden"), 900);
      nameInput.value = emailInput.value = issueInput.value = "";
    } else {
      sheetResult.style.color = "#fecaca";
      sheetResult.textContent = data.detail || "Failed to log. Please try again.";
    }
  } catch {
    sheetResult.style.color = "#fecaca";
    sheetResult.textContent = "Network error. Please try again.";
  } finally {
    submitEscalation.disabled = false;
  }
});
