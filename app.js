/**
 * SAARTHI (सारथी) - AI-Powered Hyper-Personalized Banking for Bharat
 * Frontend Application Logic & Speech Synthesis Engine
 */

// Application State
let currentCustomer = null;
let currentLanguage = 'hi';
let voiceAudioEnabled = true;
let activeTenure = 12;
let lastBotSpokenText = "";
let recognitionInstance = null;
let isRecording = false;

// Language code mappings for Web Speech API
const LANG_SPEECH_MAP = {
  'en': 'en-IN',
  'hi': 'hi-IN',
  'gu': 'gu-IN',
  'mr': 'mr-IN',
  'ta': 'ta-IN',
  'te': 'te-IN',
  'bn': 'bn-IN'
};

// ==============================================================
// 1. INITIALIZATION & AUTHENTICATION
// ==============================================================

document.addEventListener('DOMContentLoaded', () => {
  // Check if session exists in localStorage
  const savedUser = localStorage.getItem('saarthi_active_user');
  if (savedUser) {
    try {
      currentCustomer = JSON.parse(savedUser);
      currentLanguage = currentCustomer.language || 'hi';
      document.getElementById('globalLangSelect').value = currentLanguage;
      showMainApp();
      loadCustomerData(currentCustomer.id);
    } catch (e) {
      // Fallback to auth screen
      showAuthScreen();
    }
  } else {
    showAuthScreen();
  }
});

function showAuthScreen() {
  document.getElementById('authScreen').classList.remove('hidden');
  document.getElementById('mainApp').classList.add('hidden');
}

function showMainApp() {
  document.getElementById('authScreen').classList.add('hidden');
  document.getElementById('mainApp').classList.remove('hidden');
  switchMainView('customer');
}

function switchAuthTab(tab) {
  const loginBtn = document.getElementById('tabLoginBtn');
  const regBtn = document.getElementById('tabRegisterBtn');
  const loginContent = document.getElementById('loginTabContent');
  const regContent = document.getElementById('registerTabContent');

  if (tab === 'login') {
    loginBtn.className = "flex-1 pb-3 text-sm font-bold text-blue-700 border-b-2 border-blue-600 transition-all";
    regBtn.className = "flex-1 pb-3 text-sm font-bold text-slate-500 hover:text-slate-800 transition-all";
    loginContent.classList.remove('hidden');
    regContent.classList.add('hidden');
  } else {
    regBtn.className = "flex-1 pb-3 text-sm font-bold text-blue-700 border-b-2 border-blue-600 transition-all";
    loginBtn.className = "flex-1 pb-3 text-sm font-bold text-slate-500 hover:text-slate-800 transition-all";
    regContent.classList.remove('hidden');
    loginContent.classList.add('hidden');
  }
}

// Quick demo login for hackathon evaluators
async function quickLoginPersona(personaId) {
  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ loginId: personaId })
    });
    const data = await res.json();
    if (data.success) {
      currentCustomer = data.user;
      currentLanguage = currentCustomer.language || 'hi';
      document.getElementById('globalLangSelect').value = currentLanguage;
      localStorage.setItem('saarthi_active_user', JSON.stringify(currentCustomer));
      showMainApp();
      renderCustomerHub(currentCustomer);
      speakGreeting();
    }
  } catch (err) {
    console.error("Login failed:", err);
    alert("Login failed, please check connection.");
  }
}

async function handleLogin() {
  const input = document.getElementById('loginInput').value.trim();
  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ loginId: input || "ramesh_kirana" })
    });
    const data = await res.json();
    if (data.success) {
      currentCustomer = data.user;
      currentLanguage = currentCustomer.language || 'hi';
      document.getElementById('globalLangSelect').value = currentLanguage;
      localStorage.setItem('saarthi_active_user', JSON.stringify(currentCustomer));
      showMainApp();
      renderCustomerHub(currentCustomer);
      speakGreeting();
    }
  } catch (err) {
    console.error("Login failed:", err);
  }
}

async function handleRegister() {
  const name = document.getElementById('regName').value.trim() || "Mukesh Verma";
  const phone = document.getElementById('regPhone').value.trim() || "+91 98765 11000";
  const location = document.getElementById('regLocation').value.trim() || "Muzaffarpur, Bihar (Tier-3)";
  const role = document.getElementById('regRole').value;
  const aadhaar = document.getElementById('regAadhaar').value.trim() || "492019482103";
  const income = parseInt(document.getElementById('regIncome').value) || 35000;

  try {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name, phone, location, role, aadhaar, monthlyIncome: income, language: currentLanguage
      })
    });
    const data = await res.json();
    if (data.success) {
      alert("✓ Account Created & Verified with Instant Aadhaar e-KYC (DigiLocker)!");
      currentCustomer = data.user;
      localStorage.setItem('saarthi_active_user', JSON.stringify(currentCustomer));
      showMainApp();
      renderCustomerHub(currentCustomer);
      speakGreeting();
    }
  } catch (err) {
    console.error("Registration failed:", err);
  }
}

function handleLogout() {
  localStorage.removeItem('saarthi_active_user');
  currentCustomer = null;
  showAuthScreen();
}


// ==============================================================
// 2. TEXT-TO-SPEECH & SPEECH-TO-TEXT VERNACULAR ENGINE
// ==============================================================

function toggleVoiceAudio() {
  voiceAudioEnabled = !voiceAudioEnabled;
  const statusText = document.getElementById('ttsStatusText');
  const icon = document.getElementById('speakerIcon');
  if (voiceAudioEnabled) {
    statusText.innerText = "Sound: ON";
    icon.innerText = "🔊";
    speakText("सारथी वॉयस ऑडियो चालू है (Voice Audio Enabled)");
  } else {
    statusText.innerText = "Sound: OFF";
    icon.innerText = "🔇";
    window.speechSynthesis.cancel();
  }
}

function speakText(text, lang = currentLanguage) {
  if (!voiceAudioEnabled || !('speechSynthesis' in window) || !text) return;

  window.speechSynthesis.cancel(); // cancel pending speech

  const cleanText = text.replace(/<[^>]*>?/gm, '').replace(/₹/g, ' रुपये ');
  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang = LANG_SPEECH_MAP[lang] || 'hi-IN';
  utterance.rate = 0.95; // Slightly slower for clear Bharat rural understanding
  utterance.pitch = 1.0;

  // Soundbar animation trigger
  const bars = document.querySelectorAll('.sound-bar');
  bars.forEach(b => b.style.animationPlayState = 'running');

  utterance.onend = () => {
    bars.forEach(b => b.style.animationPlayState = 'paused');
  };
  utterance.onerror = () => {
    bars.forEach(b => b.style.animationPlayState = 'paused');
  };

  window.speechSynthesis.speak(utterance);
}

function speakGreeting() {
  if (!currentCustomer) return;
  const greetings = {
    'hi': `नमस्ते ${currentCustomer.name} जी! सारथी बैंकिंग में आपका स्वागत है।`,
    'gu': `નમસ્તે ${currentCustomer.name}ભાઈ! સારથી બેંકિંગમાં આપનું સ્વાગત છે.`,
    'en': `Welcome to Saarthi, ${currentCustomer.name}! How may I assist your financial journey today?`
  };
  const msg = greetings[currentLanguage] || greetings['hi'];
  speakText(msg);
}

function readLastBotMessage() {
  if (lastBotSpokenText) {
    speakText(lastBotSpokenText);
  } else {
    const welcome = document.getElementById('welcomeChatMsg');
    if (welcome) speakText(welcome.innerText);
  }
}

// Speech Recognition (Microphone Voice Input)
function toggleSpeechRecognition() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) {
    alert("Speech recognition is supported in Google Chrome and modern browsers.");
    return;
  }

  const micBtn = document.getElementById('micBtn');
  const micIcon = document.getElementById('micIcon');

  if (isRecording) {
    if (recognitionInstance) recognitionInstance.stop();
    isRecording = false;
    micBtn.classList.remove('bg-red-500', 'text-white');
    micBtn.classList.add('bg-blue-50', 'text-blue-700');
    micIcon.innerText = "🎙️";
    return;
  }

  recognitionInstance = new SpeechRec();
  recognitionInstance.lang = LANG_SPEECH_MAP[currentLanguage] || 'hi-IN';
  recognitionInstance.continuous = false;
  recognitionInstance.interimResults = false;

  micBtn.classList.remove('bg-blue-50', 'text-blue-700');
  micBtn.classList.add('bg-red-500', 'text-white', 'animate-pulse');
  micIcon.innerText = "🔴";
  isRecording = true;

  recognitionInstance.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('chatInput').value = transcript;
    handleSendChat();
  };

  recognitionInstance.onend = () => {
    isRecording = false;
    micBtn.classList.remove('bg-red-500', 'text-white', 'animate-pulse');
    micBtn.classList.add('bg-blue-50', 'text-blue-700');
    micIcon.innerText = "🎙️";
  };

  recognitionInstance.onerror = (e) => {
    console.error("Speech recognition error:", e);
    isRecording = false;
    micBtn.classList.remove('bg-red-500', 'text-white', 'animate-pulse');
    micBtn.classList.add('bg-blue-50', 'text-blue-700');
    micIcon.innerText = "🎙️";
  };

  recognitionInstance.start();
}


// ==============================================================
// 3. CUSTOMER DATA RENDERING & STRESS MONITOR
// ==============================================================

async function loadCustomerData(id) {
  try {
    const res = await fetch(`/api/customer/${id}`);
    const data = await res.json();
    if (data.customer) {
      currentCustomer = data.customer;
      renderCustomerHub(currentCustomer);
    }
  } catch (err) {
    console.error("Failed to load customer data:", err);
  }
}

function renderCustomerHub(c) {
  if (!c) return;

  // Header User Pill
  document.getElementById('headerAvatar').innerText = c.avatar || "👤";
  document.getElementById('headerUserName').innerText = c.name;
  document.getElementById('headerUserRole').innerText = c.role;

  // Hero Card Profile
  document.getElementById('custBalance').innerText = `₹${c.averageBalance.toLocaleString('en-IN')}`;
  document.getElementById('custAvatar').innerText = c.avatar || "👤";
  document.getElementById('custAccount').innerText = c.accountNumber || "••• ••• 4821";
  document.getElementById('custBank').innerText = c.bankName || "Bharat Vikas Gramin Bank";
  document.getElementById('custLocation').innerText = c.location;

  // KYC Information
  if (c.kycInfo) {
    document.getElementById('custKycStatus').innerText = c.kycInfo.status;
    document.getElementById('custAadhaar').innerText = c.kycInfo.aadhaarMasked || "XXXX-XXXX-8912";
    document.getElementById('custAaConsent').innerText = c.kycInfo.accountAggregatorConsent || "Active Consent (Sahamati)";
  }

  // Scores
  document.getElementById('custAltScore').innerText = `${c.altCreditScore} / 900`;
  document.getElementById('custCibilScore').innerText = c.cibilScore > 0 ? c.cibilScore : 'NTC (New-to-Credit)';

  // Stress Status Gauge & Needle
  const needle = document.getElementById('stressNeedle');
  const stressText = document.getElementById('stressValueText');
  const badge = document.getElementById('stressStatusBadge');
  const banner = document.getElementById('empatheticBanner');

  const stressPct = Math.round(c.stressIndex * 100);
  needle.style.left = `${Math.min(95, Math.max(5, stressPct))}%`;

  if (c.stressIndex > 0.65) {
    // Critical Stress
    stressText.innerText = `${c.stressIndex.toFixed(2)} (High Stress - Intervention Required)`;
    stressText.className = "text-red-600 font-black";
    badge.innerText = "⚠️ Cashflow Stress Alert";
    badge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-red-100 text-red-800";
    banner.classList.remove('hidden');
  } else if (c.stressIndex > 0.35) {
    // Moderate
    stressText.innerText = `${c.stressIndex.toFixed(2)} (Moderate / Monitored)`;
    stressText.className = "text-amber-600 font-black";
    badge.innerText = "Monitored Stable";
    badge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-800";
    banner.classList.add('hidden');
  } else {
    // Healthy
    stressText.innerText = `${c.stressIndex.toFixed(2)} (Healthy / Low Risk)`;
    stressText.className = "text-green-700 font-black";
    badge.innerText = "Healthy / Prime";
    badge.className = "text-[10px] font-bold px-2 py-0.5 rounded-full bg-green-100 text-green-800";
    banner.classList.add('hidden');
  }

  // Telemetry updates
  document.getElementById('sigLiquidity').innerText = `${((1 - c.stressIndex) * 14).toFixed(1)} Days`;
  document.getElementById('sigCashflowDrop').innerText = `${Math.round(c.stressIndex * 60)}% Deviation`;
  document.getElementById('sigBounceProb').innerText = `${(c.stressIndex * 95).toFixed(1)}%`;

  // Render Recommendations (Pillar 1)
  renderRecommendations(c.recommendations || []);

  // Render Recent Transactions
  renderTransactions(c.recentTransactions || []);
}

function renderRecommendations(recs) {
  const container = document.getElementById('recommendationsList');
  container.innerHTML = '';

  if (recs.length === 0) {
    container.innerHTML = `<div class="p-6 text-center text-slate-400">No active product recommendations.</div>`;
    return;
  }

  recs.forEach((rec, idx) => {
    const isEmpathetic = rec.category.includes("Empathetic");
    const cardBg = isEmpathetic ? "bg-amber-50/70 border-amber-300" : "bg-white border-slate-200";
    const badgeColor = isEmpathetic ? "bg-amber-200 text-amber-900 border-amber-300" : "bg-blue-100 text-blue-800 border-blue-200";

    const title = (currentLanguage !== 'en' && rec.vernacularTitle) ? rec.vernacularTitle : rec.title;

    const card = document.createElement('div');
    card.className = `p-4 rounded-xl border ${cardBg} touch-card shadow-sm space-y-3`;
    card.innerHTML = `
      <div class="flex items-start justify-between">
        <div>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded border ${badgeColor}">${rec.badge}</span>
          <h4 class="text-sm font-black text-slate-900 mt-1.5">${title}</h4>
          <span class="text-[11px] text-slate-500 font-medium">${rec.category} • Urgency: ${rec.urgency}</span>
        </div>
        <div class="text-right">
          <span class="text-xs font-black text-blue-700">${rec.amount}</span>
          <div class="text-[10px] text-slate-500 font-semibold">${rec.interestRate}</div>
        </div>
      </div>

      <!-- Why Recommended Bullet Summary -->
      <div class="bg-white/80 p-2.5 rounded-lg border border-slate-100 text-xs text-slate-700 space-y-1">
        <div class="flex items-center space-x-1 text-[10px] font-bold text-blue-800 uppercase tracking-wider">
          <span>⚡ Why This Was Recommended For You:</span>
        </div>
        <p class="text-[11px] leading-relaxed text-slate-600">${rec.whyRecommended[0]}</p>
      </div>

      <!-- Key Details & CTA Actions -->
      <div class="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
        <div class="text-[11px] text-slate-500">
          <span class="font-bold text-slate-700">Repayment:</span> ${rec.repaymentType}
        </div>
        <div class="flex space-x-2">
          <button onclick='openExplainModal(${JSON.stringify(rec).replace(/'/g, "&apos;")})' 
                  class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg font-bold text-[11px] transition">
            🔍 Why this?
          </button>
          ${isEmpathetic ? `
            <button onclick="triggerEmpatheticAction('${rec.id}')" class="px-3 py-1 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-bold text-[11px] shadow transition">
              Apply Relief
            </button>
          ` : `
            <button onclick="openLoanModal(50000)" class="px-3 py-1 bg-blue-700 hover:bg-blue-800 text-white rounded-lg font-bold text-[11px] shadow transition">
              Apply in 2 Min →
            </button>
          `}
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

function renderTransactions(txns) {
  const container = document.getElementById('txnsList');
  container.innerHTML = '';
  txns.forEach(t => {
    const isCredit = t.type === 'credit';
    const isWarning = t.type === 'warning';
    const sign = isCredit ? '+' : (isWarning ? '⚠️' : '-');
    const color = isCredit ? 'text-green-600 font-bold' : (isWarning ? 'text-amber-600 font-bold' : 'text-slate-800 font-semibold');

    const item = document.createElement('div');
    item.className = "flex items-center justify-between p-2 bg-white rounded-lg border border-slate-100";
    item.innerHTML = `
      <div>
        <div class="font-medium text-slate-800">${t.desc}</div>
        <div class="text-[10px] text-slate-400">${t.date}</div>
      </div>
      <div class="${color}">${sign} ₹${Math.abs(t.amount).toLocaleString('en-IN')}</div>
    `;
    container.appendChild(item);
  });
}


// ==============================================================
// 4. CONVERSATIONAL BOT (SAARTHI AI) LOGIC
// ==============================================================

async function handleSendChat() {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;

  // Append User Message Bubble
  appendChatMessage(msg, 'user');
  input.value = '';

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personaId: currentCustomer ? currentCustomer.id : 'ramesh_kirana',
        message: msg,
        language: currentLanguage
      })
    });
    const data = await res.json();

    // Append Bot Message Bubble
    appendChatMessage(data.response, 'bot');
    lastBotSpokenText = data.response;

    // Speak aloud if sound enabled
    if (voiceAudioEnabled) {
      speakText(data.response, currentLanguage);
    }
  } catch (err) {
    console.error("Chat error:", err);
    appendChatMessage("माफ़ कीजिए, कनेक्शन में समस्या आई है। कृपया दोबारा पूछें।", 'bot');
  }
}

function sendQuickQuery(text) {
  document.getElementById('chatInput').value = text;
  handleSendChat();
}

function appendChatMessage(text, sender) {
  const container = document.getElementById('chatMessages');
  const bubble = document.createElement('div');

  if (sender === 'user') {
    bubble.className = "flex items-start justify-end space-x-2";
    bubble.innerHTML = `
      <div class="bg-blue-700 text-white p-3 rounded-2xl rounded-tr-none shadow-sm max-w-[85%]">
        <p>${text}</p>
      </div>
      <div class="w-7 h-7 rounded-full bg-slate-300 text-slate-800 flex items-center justify-center text-xs font-bold shrink-0">
        ${currentCustomer ? currentCustomer.avatar : '👤'}
      </div>
    `;
  } else {
    bubble.className = "flex items-start space-x-2 animate-fade-in";
    bubble.innerHTML = `
      <div class="w-7 h-7 rounded-full bg-orange-500 text-white flex items-center justify-center text-xs font-bold shrink-0">सा</div>
      <div class="bg-white p-3 rounded-2xl rounded-tl-none shadow-sm border border-slate-200 max-w-[85%] text-slate-800">
        <p>${text}</p>
        <button onclick="speakText('${text.replace(/'/g, "\\'")}')" class="mt-2 text-[10px] text-blue-600 hover:text-blue-800 font-bold flex items-center space-x-1">
          <span>🔊</span><span>सुनें (Listen)</span>
        </button>
      </div>
    `;
  }

  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}


// ==============================================================
// 5. STRESS SHOCK SIMULATION & EMPATHETIC RELIEF
// ==============================================================

async function simulateCashflowShock() {
  if (!currentCustomer) return;
  try {
    const res = await fetch('/api/simulate-stress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ personaId: currentCustomer.id })
    });
    const data = await res.json();
    if (data.success) {
      currentCustomer = data.customer;
      renderCustomerHub(currentCustomer);
      speakText("सावधान! खाते में 50% से अधिक लेन-देन में गिरावट दर्ज हुई है। सारथी एआई ने लोन के विज्ञापन रोक दिए हैं और आपके लिए किश्त राहत सुरक्षा सक्रिय कर दी है।");
    }
  } catch (err) {
    console.error("Stress simulation error:", err);
  }
}

async function resetCustomerState() {
  if (!currentCustomer) return;
  try {
    const res = await fetch('/api/reset-persona', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ personaId: currentCustomer.id })
    });
    const data = await res.json();
    if (data.success) {
      currentCustomer = data.customer;
      renderCustomerHub(currentCustomer);
      speakText("खाता स्थिति सामान्य रीसेट कर दी गई है।");
    }
  } catch (err) {
    console.error("Reset error:", err);
  }
}

async function triggerEmpatheticAction(actionId) {
  if (!currentCustomer) return;
  try {
    const res = await fetch('/api/trigger-intervention', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ personaId: currentCustomer.id, interventionId: actionId })
    });
    const data = await res.json();
    if (data.success) {
      currentCustomer.stressIndex = data.newStressIndex;
      currentCustomer.stressStatus = data.newStressStatus;
      renderCustomerHub(currentCustomer);

      alert(`✓ ${data.message}\n\n[SMS Sent]: ${data.reliefDetails.smsConfirmation}`);
      speakText("राहत आवेदन स्वीकृत कर लिया गया है। आपका सिबिल स्कोर पूरी तरह सुरक्षित है और पेनल्टी माफ़ कर दी गई है।");
    }
  } catch (err) {
    console.error("Intervention error:", err);
  }
}


// ==============================================================
// 6. 2-MINUTE DIGITAL LOAN APPLICATION & SANCTION LETTER
// ==============================================================

function openLoanModal(initialAmount = 50000) {
  document.getElementById('loanAmountSlider').value = initialAmount;
  updateLoanCalculations();
  document.getElementById('loanModal').classList.remove('hidden');
}

function closeLoanModal() {
  document.getElementById('loanModal').classList.add('hidden');
}

function selectTenure(months) {
  activeTenure = months;
  [6, 12, 24].forEach(m => {
    const btn = document.getElementById(`tenure${m}`);
    if (m === months) {
      btn.className = "p-2 border-2 border-blue-600 bg-blue-50 rounded-lg font-bold text-blue-800";
    } else {
      btn.className = "p-2 border rounded-lg hover:border-blue-500 font-semibold text-slate-700";
    }
  });
  updateLoanCalculations();
}

function updateLoanCalculations() {
  const amount = parseInt(document.getElementById('loanAmountSlider').value);
  document.getElementById('loanAmountDisplay').innerText = `₹${amount.toLocaleString('en-IN')}`;

  const apr = 11.2;
  const monthlyRate = (apr / 100) / 12;
  const emi = Math.round((amount * monthlyRate * Math.pow(1 + monthlyRate, activeTenure)) / (Math.pow(1 + monthlyRate, activeTenure) - 1));
  const dailyBite = Math.round(emi / 30);

  document.getElementById('loanDailyBiteDisplay').innerText = `₹${dailyBite} / day`;
}

async function submitLoanApplication() {
  const consent = document.getElementById('consentCheck').checked;
  if (!consent) {
    alert("Please provide Account Aggregator consent to proceed with paperless underwriting.");
    return;
  }

  const amount = parseInt(document.getElementById('loanAmountSlider').value);
  closeLoanModal();

  try {
    const res = await fetch('/api/apply-loan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personaId: currentCustomer ? currentCustomer.id : 'ramesh_kirana',
        amount,
        tenure: activeTenure
      })
    });
    const data = await res.json();
    if (data.success) {
      renderSanctionLetter(data.sanction);
      speakText(`बधाई हो ${currentCustomer ? currentCustomer.name : ''}! आपका ₹${amount.toLocaleString('en-IN')} का लोन डिजिटल रूप से स्वीकृत हो चुका है।`);
    }
  } catch (err) {
    console.error("Loan application error:", err);
  }
}

function renderSanctionLetter(s) {
  const container = document.getElementById('sanctionLetterContent');
  container.innerHTML = `
    <div class="border-b border-slate-200 pb-3 flex justify-between items-start">
      <div>
        <div class="text-[10px] text-slate-400 uppercase font-mono">Sanction ID: ${s.sanctionId}</div>
        <div class="text-base font-black text-slate-900 mt-0.5">${s.borrowerName}</div>
        <div class="text-[11px] text-slate-500">Account: ${s.maskedAccount} • Issued: ${s.issuedAt}</div>
      </div>
      <span class="px-2.5 py-1 bg-green-100 text-green-800 font-bold rounded-full text-[10px] border border-green-200">
        ● ${s.status}
      </span>
    </div>

    <!-- Loan Financial Matrix -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
      <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100">
        <span class="text-[10px] text-slate-500">Sanctioned Amount</span>
        <div class="text-base font-black text-blue-800">₹${s.sanctionedAmount.toLocaleString('en-IN')}</div>
      </div>
      <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100">
        <span class="text-[10px] text-slate-500">Annual Percentage Rate</span>
        <div class="text-base font-black text-slate-800">${s.interestRate}</div>
      </div>
      <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-100">
        <span class="text-[10px] text-slate-500">Monthly EMI</span>
        <div class="text-base font-black text-slate-800">₹${s.monthlyEmi.toLocaleString('en-IN')}</div>
      </div>
      <div class="p-2.5 bg-green-50 rounded-xl border border-green-100">
        <span class="text-[10px] text-green-700 font-semibold">Micro-Daily Bite</span>
        <div class="text-base font-black text-green-700">₹${s.dailyBite}/day</div>
      </div>
    </div>

    <!-- Regulatory KFS Mandated Items -->
    <div class="space-y-2 bg-slate-50 p-3 rounded-xl border border-slate-200">
      <div class="flex justify-between">
        <span class="text-slate-500">Processing Fees & Upfront Charges:</span>
        <span class="font-bold text-slate-800">${s.processingFee}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-slate-500">Disbursal Route:</span>
        <span class="font-bold text-slate-800">${s.disbursalMode}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-slate-500">Cooling-Off / Look-In Period:</span>
        <span class="font-bold text-green-700">${s.coolingOffPeriod}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-slate-500">Repayment Mode:</span>
        <span class="font-bold text-slate-800">${s.repaymentSchedule}</span>
      </div>
    </div>

    <!-- Underwriting Verification Audit -->
    <div>
      <span class="text-[11px] font-bold text-slate-700 block mb-1">Underwriting Verification Signals:</span>
      <div class="grid grid-cols-2 gap-2 text-[10px]">
        <div class="p-2 bg-white rounded border border-slate-200 flex items-center space-x-1.5">
          <span class="text-green-600 font-bold">✓</span>
          <span>Account Aggregator Consent: ${s.underwritingSignals.accountAggregatorConsent}</span>
        </div>
        <div class="p-2 bg-white rounded border border-slate-200 flex items-center space-x-1.5">
          <span class="text-green-600 font-bold">✓</span>
          <span>UPI Velocity: ${s.underwritingSignals.upiVelocityVerification}</span>
        </div>
        <div class="p-2 bg-white rounded border border-slate-200 flex items-center space-x-1.5">
          <span class="text-green-600 font-bold">✓</span>
          <span>Fraud & SIM Bind Check: ${s.underwritingSignals.fraudCheck}</span>
        </div>
        <div class="p-2 bg-white rounded border border-slate-200 flex items-center space-x-1.5">
          <span class="text-green-600 font-bold">✓</span>
          <span>DPDP Act Token: ${s.underwritingSignals.dpdpComplianceToken}</span>
        </div>
      </div>
    </div>
  `;

  document.getElementById('sanctionModal').classList.remove('hidden');
}

function closeSanctionModal() {
  document.getElementById('sanctionModal').classList.add('hidden');
}

function confirmDisbursal() {
  closeSanctionModal();
  const amount = parseInt(document.getElementById('loanAmountSlider').value);
  if (currentCustomer) {
    currentCustomer.averageBalance += amount;
    renderCustomerHub(currentCustomer);
  }
  alert(`✓ SUCCESS! ₹${amount.toLocaleString('en-IN')} has been disbursed directly into your bank account via NEFT/IMPS.`);
  speakText(`लोन की राशि ₹${amount.toLocaleString('en-IN')} सीधे आपके बैंक खाते में जमा कर दी गई है।`);
}


// ==============================================================
// 7. EXPLAINABLE AI (TreeSHAP ATTRIBUTION CARD)
// ==============================================================

function openExplainModal(rec) {
  const body = document.getElementById('explainModalBody');
  const title = (currentLanguage !== 'en' && rec.vernacularTitle) ? rec.vernacularTitle : rec.title;

  let factorsHtml = '';
  if (rec.shapFactors && rec.shapFactors.length > 0) {
    factorsHtml = rec.shapFactors.map(f => {
      const isPositive = f.impact.startsWith('+');
      const barColor = isPositive ? 'bg-green-600' : 'bg-red-500';
      const pct = Math.abs(parseInt(f.impact)) || 20;

      return `
        <div class="space-y-1">
          <div class="flex justify-between text-[11px] font-semibold">
            <span class="text-slate-800">${f.factor}</span>
            <span class="${isPositive ? 'text-green-700' : 'text-red-600'} font-bold">${f.impact}</span>
          </div>
          <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div class="${barColor} h-full rounded-full" style="width: ${pct}%"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  body.innerHTML = `
    <div>
      <h4 class="font-black text-sm text-slate-900">${title}</h4>
      <span class="text-[11px] text-blue-700 font-bold">Confidence Score: ${rec.confidenceScore}%</span>
    </div>

    <!-- TreeSHAP Attribution Breakdown -->
    <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-2.5">
      <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">TreeSHAP Contributing Factors:</span>
      ${factorsHtml}
    </div>

    <!-- Vernacular plain-language explanation -->
    <div class="p-3 bg-blue-50 rounded-xl border border-blue-100 text-[11px] text-blue-900 space-y-1">
      <div class="font-bold flex items-center space-x-1">
        <span>🗣️</span><span>Plain-Language Reason:</span>
      </div>
      <p class="leading-relaxed">${rec.whyRecommended.join(' ')}</p>
    </div>

    <button onclick="speakText('${rec.whyRecommended[0].replace(/'/g, "\\'")}')" 
            class="w-full py-2 bg-blue-700 hover:bg-blue-800 text-white rounded-lg font-bold text-xs shadow transition flex items-center justify-center space-x-1.5">
      <span>🔊</span><span>Listen Explanation Aloud</span>
    </button>
  `;

  document.getElementById('explainModal').classList.remove('hidden');
}

function closeExplainModal() {
  document.getElementById('explainModal').classList.add('hidden');
}


// ==============================================================
// 8. GLOBAL NAVIGATION & LANGUAGE SWITCHING
// ==============================================================

function switchMainView(view) {
  const views = ['Customer', 'Banker', 'Arch', 'Compliance', 'Pitch'];
  views.forEach(v => {
    const mainEl = document.getElementById(`view${v}`);
    const navEl = document.getElementById(`nav${v}`);
    if (v.toLowerCase() === view.toLowerCase() || (v === 'Arch' && view === 'architecture')) {
      mainEl.classList.remove('hidden');
      if (navEl) {
        navEl.className = "px-3 py-2 rounded-md bg-blue-800 text-white flex items-center space-x-1.5 transition";
      }
    } else {
      mainEl.classList.add('hidden');
      if (navEl) {
        navEl.className = "px-3 py-2 rounded-md hover:bg-blue-800 text-blue-100 flex items-center space-x-1.5 transition";
      }
    }
  });
}

function changeLanguage(lang) {
  currentLanguage = lang;
  if (currentCustomer) {
    currentCustomer.language = lang;
    renderCustomerHub(currentCustomer);
  }
  const langNames = {
    'hi': 'हिंदी चुनी गई है',
    'gu': 'ગુજરાતી ભાષા પસંદ કરવામાં આવી છે',
    'en': 'English language selected',
    'mr': 'मराठी भाषा निवडली आहे',
    'ta': 'தமிழ் மொழி தேர்ந்தெடுக்கப்பட்டது',
    'te': 'తెలుగు భాష ఎంపిక చేయబడింది',
    'bn': 'বাংলা ভাষা নির্বাচিত হয়েছে'
  };
  speakText(langNames[lang] || 'Language changed');
}
