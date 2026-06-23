import streamlit as st
import google.generativeai as genai
import time
import datetime

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="KHAN SIR BADNAPUR AI Office Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# API CONFIG
# ============================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ============================================
# SESSION STATE INIT
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0
if "msg_date" not in st.session_state:
    st.session_state.msg_date = str(datetime.date.today())
if "history" not in st.session_state:
    st.session_state.history = []

# नया दिन तो reset
if st.session_state.msg_date != str(datetime.date.today()):
    st.session_state.msg_count = 0
    st.session_state.msg_date = str(datetime.date.today())

# ============================================
# DAILY LIMIT
# ============================================
DAILY_LIMIT = 50

# ============================================
# CUSTOM CSS — पूरा जादू 🎨
# ============================================
st.markdown("""
<style>
/* === मुख्य बैकग्राउंड === */
.stApp {
    background: #0a0a0c;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

/* === एनिमेटेड टाइटल === */
.main-title {
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(90deg, #f59e0b, #ef4444, #f59e0b, #10b981, #f59e0b);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
    text-align: center;
    letter-spacing: -1px;
    line-height: 1.2;
    margin-bottom: 0;
}

@keyframes shine {
    to { background-position: 300% center; }
}

/* === सबटाइटल === */
.subtitle {
    text-align: center;
    color: #72717a;
    font-size: 1rem;
    margin-top: 6px;
    margin-bottom: 30px;
}

/* === कार्ड === */
.card {
    background: rgba(22, 22, 26, 0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 16px;
    padding: 22px;
    margin: 8px 0;
    transition: all 0.3s ease;
    cursor: pointer;
}

.card:hover {
    border-color: rgba(245, 158, 11, 0.5);
    box-shadow: 0 0 30px rgba(245, 158, 11, 0.08);
    transform: translateY(-3px);
}

.card-active {
    border-color: #f59e0b !important;
    box-shadow: 0 0 25px rgba(245, 158, 11, 0.15) !important;
    background: rgba(245, 158, 11, 0.05) !important;
}

/* === टास्क आइकन === */
.task-icon {
    font-size: 2.2rem;
    margin-bottom: 8px;
    display: block;
}

.task-name {
    color: #e8e6e3;
    font-weight: 700;
    font-size: 1rem;
    margin: 0 0 4px 0;
}

.task-desc {
    color: #72717a;
    font-size: 0.8rem;
    margin: 0;
    line-height: 1.4;
}

/* === इनपुट बॉक्स === */
.stTextArea > div > div > textarea {
    border-radius: 14px !important;
    border: 2px solid #2a2a32 !important;
    background: #16161a !important;
    color: #e8e6e3 !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    transition: all 0.3s ease;
    min-height: 140px !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 20px rgba(245, 158, 11, 0.15) !important;
    outline: none !important;
}

.stTextArea > div > div > textarea::placeholder {
    color: #555 !important;
}

/* === सिलेक्टबॉक्स === */
.stSelectbox > div > div {
    background: #16161a !important;
    border: 2px solid #2a2a32 !important;
    border-radius: 12px !important;
    color: #e8e6e3 !important;
    padding: 10px 14px !important;
}

.stSelectbox > div > div:focus-within {
    border-color: #f59e0b !important;
    box-shadow: 0 0 20px rgba(245, 158, 11, 0.15) !important;
}

/* === जेनरेट बटन === */
.gen-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    width: 100%;
    padding: 16px;
    border-radius: 14px;
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: white;
    font-weight: 800;
    font-size: 1.1rem;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
}

.gen-btn:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 35px rgba(245, 158, 11, 0.3);
}

.gen-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
}

/* === आउटपुट बॉक्स === */
.output-box {
    background: rgba(22, 22, 26, 0.9);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
    animation: fadeSlideUp 0.5s ease;
    position: relative;
}

.output-box::before {
    content: "AI OUTPUT";
    position: absolute;
    top: -10px;
    left: 20px;
    background: #10b981;
    color: #0a0a0c;
    font-size: 0.7rem;
    font-weight: 800;
    padding: 2px 12px;
    border-radius: 20px;
    letter-spacing: 1px;
}

.output-text {
    color: #e8e6e3;
    font-size: 0.95rem;
    line-height: 1.8;
    white-space: pre-wrap;
}

/* === कॉपी बटन === */
.copy-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 10px;
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 14px;
}

.copy-btn:hover {
    background: rgba(245, 158, 11, 0.25);
    transform: scale(1.03);
}

/* === लोडिंग स्पिनर === */
.thinking-box {
    text-align: center;
    padding: 40px 20px;
    animation: pulse 1.5s ease-in-out infinite;
}

.thinking-dots {
    display: inline-flex;
    gap: 6px;
    margin-bottom: 12px;
}

.thinking-dots span {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #f59e0b;
    animation: bounce 1.4s ease-in-out infinite;
}

.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40% { transform: scale(1); opacity: 1; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* === साइडबार === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111115 0%, #0d0d10 100%) !important;
    border-right: 1px solid #2a2a32 !important;
}

[data-testid="stSidebar"] .stMarkdown h2 {
    color: #f59e0b !important;
}

.sidebar-card {
    background: rgba(22, 22, 26, 0.8);
    border: 1px solid #2a2a32;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
}

.sidebar-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
}

.sidebar-stat-label {
    color: #72717a;
    font-size: 0.85rem;
}

.sidebar-stat-value {
    color: #f59e0b;
    font-weight: 700;
    font-size: 0.9rem;
}

/* === प्रोग्रेस बार === */
.progress-bar-bg {
    width: 100%;
    height: 6px;
    background: #2a2a32;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 8px;
}

.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #f59e0b, #ef4444);
    border-radius: 10px;
    transition: width 0.5s ease;
}

/* === हिस्ट्री कार्ड === */
.history-item {
    background: rgba(22, 22, 26, 0.6);
    border: 1px solid #2a2a32;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 6px;
    font-size: 0.8rem;
    color: #72717a;
    transition: all 0.2s ease;
    cursor: pointer;
}

.history-item:hover {
    border-color: #f59e0b;
    color: #e8e6e3;
}

/* === अलर्ट/एरर === */
.limit-alert {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    animation: fadeSlideUp 0.4s ease;
}

/* === स्क्रॉलबार === */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #f59e0b; border-radius: 10px; }

/* === डिफॉल्ट छुपाओ === */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }

/* === हिस्ट्री सेक्शन === */
.section-title {
    color: #72717a;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 20px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# TASKS CONFIG
# ============================================
TASKS = {
    "Letter Drafting": {
        "icon": "✉️",
        "desc": "Official Marathi letters with Subject & Reference",
        "color": "#f59e0b"
    },
    "GR Analysis": {
        "icon": "📊",
        "desc": "Government Resolution analysis & summary",
        "color": "#3b82f6"
    },
    "Note Sheet": {
        "icon": "📋",
        "desc": "Government format Note Sheet preparation",
        "color": "#10b981"
    },
    "WhatsApp Message": {
        "icon": "📱",
        "desc": "Concise official WhatsApp messages",
        "color": "#ef4444"
    }
}

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:

    # लोगो
    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px 0;">
        <div style="font-size:2.5rem;">🏛️</div>
        <h2 style="color:#f59e0b;margin:4px 0 0 0;font-size:1.1rem;">KHAN SIR</h2>
        <p style="color:#72717a;font-size:0.75rem;margin:0;">BADNAPUR OFFICE AI</p>
    </div>
    """, unsafe_allow_html=True)

    # उपयोग स्टैट्स
    used = st.session_state.msg_count
    percent = min((used / DAILY_LIMIT) * 100, 100)

    bar_color = "#10b981" if percent < 60 else "#f59e0b" if percent < 85 else "#ef4444"

    st.markdown(f"""
    <div class="sidebar-card">
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">आज का उपयोग</span>
            <span class="sidebar-stat-value">{used} / {DAILY_LIMIT}</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{percent}%;background:linear-gradient(90deg,{bar_color},{bar_color}88);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Model सेलेक्ट
    st.markdown('<p class="section-title">Model</p>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"],
        label_visibility="collapsed"
    )

    # भाषा मोड
    st.markdown('<p class="section-title">भाषा</p>', unsafe_allow_html=True)
    lang_mode = st.radio(
        "",
        ["मराठी (Default)", "English", "हिंग्लिश"],
        label_visibility="collapsed"
    )

    # चैट मिटाओ
    st.markdown("---")
    if st.button("🗑️ सब हटाओ", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

    # हिस्ट्री
    if st.session_state.history:
        st.markdown('<p class="section-title">हाल के काम</p>', unsafe_allow_html=True)
        for i, h in enumerate(reversed(st.session_state.history[-8:])):
            icon = TASKS.get(h["task"], {}).get("icon", "📄")
            st.markdown(f"""
            <div class="history-item">
                {icon} <strong>{h['task']}</strong><br>
                <span style="font-size:0.75rem;color:#555;">{h['text'][:50]}...</span>
            </div>
            """, unsafe_allow_html=True)

    # फुटर
    st.markdown("""
    <div style="text-align:center;padding:20px 0 5px 0;color:#444;font-size:0.7rem;">
        Made with ❤️ for Khan Sir<br>
        Badnapur Office
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN AREA
# ============================================

# टाइटल
st.markdown('<p class="main-title">KHAN SIR BADNAPUR</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI Office Assistant — सरकारी कामकाज अब स्मार्ट तरीके से</p>', unsafe_allow_html=True)

# ============================================
# LIMIT CHECK
# ============================================
if st.session_state.msg_count >= DAILY_LIMIT:
    st.markdown(f"""
    <div class="limit-alert">
        <div style="font-size:3rem;margin-bottom:10px;">⏰</div>
        <h3 style="color:#ef4444;margin:0 0 6px 0;">आज की लिमिट पूरी हो गई</h3>
        <p style="color:#72717a;margin:0;">आपने आज {DAILY_LIMIT} बार इस्तेमाल किया।<br>कल फिर से आओ! 🙏</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================
# TASK SELECTION — कार्ड स्टाइल
# ============================================
st.markdown('<p class="section-title">काम चुनो</p>', unsafe_allow_html=True)

cols = st.columns(4)
selected_task = st.session_state.get("selected_task", "Letter Drafting")

for i, (task_name, task_info) in enumerate(TASKS.items()):
    with cols[i]:
        is_active = selected_task == task_name
        active_class = "card-active" if is_active else ""
        st.markdown(f"""
        <div class="card {active_class}" onclick="document.getElementById('task_{i}').click()">
            <span class="task-icon">{task_info['icon']}</span>
            <p class="task-name">{task_name}</p>
            <p class="task-desc">{task_info['desc']}</p>
        </div>
        <button id="task_{i}" style="display:none;" onclick="
            const payload = {{task: '{task_name}'}};
            window.parent.postMessage({{type: 'streamlit:setComponentValue', value: payload}}, '*');
        "></button>
        """, unsafe_allow_html=True)

# Hidden selectbox for task (real data binding)
task_options = list(TASKS.keys())
task_index = task_options.index(selected_task) if selected_task in task_options else 0

# यह selectbox छुपा हुआ है — कार्ड click से चलेगा
task = st.selectbox(
    "Task",
    task_options,
    index=task_index,
    label_visibility="collapsed",
    key="task_select"
)

# Simple approach — visible selectbox with custom label
st.markdown("---")
st.markdown(f'<p style="color:#72717a;font-size:0.85rem;font-weight:600;">📌 टास्क: <span style="color:#f59e0b;">{task}</span></p>', unsafe_allow_html=True)

# ============================================
# TEXT INPUT
# ============================================
placeholders = {
    "Letter Drafting": "यहाँ letter की details लिखो...\n\nजैसे: कार्यालय प्रमुख को, विषय, किस बारे में लिखना है, कोई reference number...",
    "GR Analysis": "यहाँ GR का विवरण या text डालो...\n\nजैसे: GR number, विभाग, तारीख, मुख्य बिंदु जो analyze करने हैं...",
    "Note Sheet": "यहाँ Note Sheet की details लिखो...\n\nजैसे: विषय, प्रस्ताव, वित्तीय ब्यौरा, अनुमोदन के लिए किसे भेजना है...",
    "WhatsApp Message": "यहाँ message की details लिखो...\n\nजैसे: किसे भेजना है, क्या सूचना देनी है, कोई deadline..."
}

text = st.text_area(
    "Details लिखो",
    height=160,
    placeholder=placeholders.get(task, "यहाँ details लिखो..."),
    key="input_text"
)

# ============================================
# GENERATE BUTTON
# ============================================
st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

btn_html = f"""
<button class="gen-btn" id="genBtn" onclick="
    document.getElementById('streamlit_gen_btn').click();
">
    🚀 Generate {task}
</button>
<button id="streamlit_gen_btn" style="display:none;"></button>
"""
st.markdown(btn_html, unsafe_allow_html=True)
generate_clicked = st.button("Generate", key="gen_button", label_visibility="collapsed")

# ============================================
# GENERATE LOGIC
# ============================================
if generate_clicked and text.strip():

    # भाषा सेट करो
    lang_map = {
        "मराठी (Default)": "official Marathi language",
        "English": "English language",
        "हिंग्लिश": "Hinglish (Marathi written in English script)"
    }
    lang_instruction = lang_map.get(lang_mode, "official Marathi language")

    # Prompt बनाओ
    prompt = f"""
    You are an expert Government Office Assistant working for Khan Sir at Badnapur Office.

    Task Type: {task}

    Language: Use {lang_instruction}.

    Rules:
    - Generate complete, ready-to-use output.
    - For Letter Drafting: Include Subject line, Reference number (if applicable), proper salutation, main body, and closing.
    - For GR Analysis: Provide summary, key points, implications, and action required.
    - For Note Sheet: Use proper government format with proposal, background, financial details, and recommendation.
    - For WhatsApp Message: Keep it concise, official, and clear with proper formatting.
    - Use proper government terminology and format.
    - Do NOT add any extra explanation outside the output format.

    User Request:
    {text}
    """

    # लोडिंग दिखाओ
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
    <div class="thinking-box">
        <div class="thinking-dots">
            <span></span><span></span><span></span>
        </div>
        <p style="color:#f59e0b;font-weight:600;margin:0;">AI तैयार कर रहा है...</p>
        <p style="color:#555;font-size:0.8rem;margin:4px 0 0 0;">कृपया थोड़ा रुको</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        # Model बनाओ
        model = genai.GenerativeModel(model_choice)

        # API call
        response = model.generate_content(prompt)

        # लोडिंग हटाओ
        loading_placeholder.empty()

        # काउंट बढ़ाओ
        st.session_state.msg_count += 1

        # हिस्ट्री में जोड़ो
        st.session_state.history.append({
            "task": task,
            "text": text.strip()[:100],
            "time": datetime.datetime.now().strftime("%H:%M")
        })

        # आउटपुट दिखाओ
        output_text = response.text

        # Escape HTML for safe display
        safe_output = output_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        st.markdown(f"""
        <div class="output-box">
            <div class="output-text">{safe_output}</div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;">
                <button class="copy-btn" onclick="
                    navigator.clipboard.writeText(decodeURIComponent('{urllib.parse.quote(output_text)}'));
                    this.innerHTML='✅ Copied!';
                    setTimeout(() => this.innerHTML='📋 Copy Text', 2000);
                ">📋 Copy Text</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Session messages में भी रखो
        st.session_state.messages.append({
            "task": task,
            "input": text,
            "output": output_text
        })

    except Exception as e:
        loading_placeholder.empty()
        st.markdown(f"""
        <div class="limit-alert" style="border-color:rgba(239,68,68,0.3);">
            <div style="font-size:2.5rem;margin-bottom:10px;">⚠️</div>
            <h3 style="color:#ef4444;margin:0 0 6px 0;">Error आया</h3>
            <p style="color:#72717a;margin:0;font-size:0.9rem;">{str(e)}</p>
        </div>
        """, unsafe_allow_html=True)

elif generate_clicked and not text.strip():
    st.markdown("""
    <div style="text-align:center;padding:15px;color:#f59e0b;font-weight:600;animation:fadeSlideUp 0.3s ease;">
        ⚠️ पहले details लिखो फिर Generate दबाओ!
    </div>
    """, unsafe_allow_html=True)

# ============================================
# पुराने रिजल्ट्स दिखाओ
# ============================================
if st.session_state.messages:
    st.markdown("---")
    st.markdown('<p class="section-title">पिछले रिजल्ट्स</p>', unsafe_allow_html=True)

    for i, msg in enumerate(reversed(st.session_state.messages[-5:])):
        icon = TASKS.get(msg["task"], {}).get("icon", "📄")
        safe_prev = msg["output"][:300].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(f"""
        <div class="card" style="cursor:pointer;" onclick="
            navigator.clipboard.writeText(decodeURIComponent('{urllib.parse.quote(msg[\"output\"])}'));
        ">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <span style="font-size:1.4rem;">{icon}</span>
                <strong style="color:#f59e0b;font-size:0.9rem;">{msg['task']}</strong>
                <span style="color:#444;font-size:0.75rem;margin-left:auto;">click to copy</span>
            </div>
            <p style="color:#72717a;font-size:0.82rem;margin:0;line-height:1.5;">
                {safe_prev}...
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div style="text-align:center;padding:40px 0 10px 0;border-top:1px solid #1a1a1e;margin-top:30px;">
    <p style="color:#444;font-size:0.8rem;margin:0;">
        🏛️ KHAN SIR BADNAPUR — AI Office Assistant
    </p>
    <p style="color:#333;font-size:0.7rem;margin:4px 0 0 0;">
        Powered by Gemini AI | Made with ❤️
    </p>
</div>
""", unsafe_allow_html=True)
