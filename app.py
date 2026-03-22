import streamlit as st
import re
import html as html_lib

st.set_page_config(
    page_title="學習病歷產生器",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary: #1a5276;
    --primary-light: #2980b9;
    --accent: #e74c3c;
    --bg-card: #f7f9fb;
    --text-main: #2c3e50;
    --border: #d5dde5;
}

.stApp { font-family: 'Noto Sans TC', sans-serif; }
h1, h2, h3 { font-family: 'Noto Sans TC', sans-serif !important; font-weight: 700 !important; }

/* Header banner */
.header-banner {
    background: linear-gradient(135deg, #1a5276 0%, #2980b9 60%, #3498db 100%);
    padding: 2rem 2.5rem; border-radius: 12px; margin-bottom: 1.5rem;
    color: white; position: relative; overflow: hidden;
}
.header-banner::before {
    content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 70%, rgba(255,255,255,0.06) 0%, transparent 60%);
}
.header-banner h1 { margin: 0; font-size: 1.8rem; color: white !important; position: relative; z-index: 1; }
.header-banner p { margin: 0.4rem 0 0 0; opacity: 0.85; font-size: 0.95rem; position: relative; z-index: 1; }

/* Section labels */
.section-label {
    background: var(--primary); color: white; display: inline-block;
    padding: 0.3rem 1rem; border-radius: 6px; font-weight: 500;
    font-size: 0.9rem; margin-bottom: 0.5rem; letter-spacing: 0.5px;
}
.section-label-green {
    background: #1e8449; color: white; display: inline-block;
    padding: 0.3rem 1rem; border-radius: 6px; font-weight: 500;
    font-size: 0.9rem; margin-bottom: 0.5rem; letter-spacing: 0.5px;
}
.section-label-purple {
    background: #6c3483; color: white; display: inline-block;
    padding: 0.3rem 1rem; border-radius: 6px; font-weight: 500;
    font-size: 0.9rem; margin-bottom: 0.5rem; letter-spacing: 0.5px;
}

/* Output card */
.output-card {
    background: #fdfdfe; border: 1px solid var(--border); border-left: 4px solid var(--primary-light);
    border-radius: 8px; padding: 1.5rem; margin: 0.5rem 0;
    font-size: 0.88rem; line-height: 1.75; white-space: pre-wrap;
    font-family: 'JetBrains Mono', 'Noto Sans TC', monospace;
    max-height: 600px; overflow-y: auto;
}
.output-card .red { color: #c0392b; font-weight: 600; }

/* Learning card */
.learning-card {
    background: linear-gradient(135deg, #fef9f0 0%, #fdf2e9 100%);
    border: 1px solid #f0d9b5; border-left: 4px solid #e67e22;
    border-radius: 10px; padding: 1.5rem; margin: 0.5rem 0;
    font-size: 0.9rem; line-height: 1.85;
    font-family: 'Noto Sans TC', sans-serif;
    max-height: 600px; overflow-y: auto;
}
.learning-card h4 {
    color: #b7560f; margin: 1.2rem 0 0.5rem 0; font-size: 1.05rem;
    border-bottom: 2px solid #f0d9b5; padding-bottom: 0.3rem;
}
.learning-card h4:first-child { margin-top: 0; }
.learning-card ul { margin: 0.3rem 0 0.8rem 1.2rem; padding: 0; }
.learning-card li { margin-bottom: 0.35rem; }

/* Chat area */
.chat-container {
    background: #f8f9fa; border: 1px solid var(--border);
    border-radius: 10px; padding: 1rem; margin: 0.5rem 0;
    max-height: 380px; overflow-y: auto;
}
.chat-msg-user {
    background: #2980b9; color: white; border-radius: 12px 12px 4px 12px;
    padding: 0.6rem 1rem; margin: 0.5rem 0; max-width: 85%;
    margin-left: auto; font-size: 0.85rem; text-align: right;
}
.chat-msg-ai {
    background: white; color: #2c3e50; border: 1px solid #e0e0e0;
    border-radius: 12px 12px 12px 4px;
    padding: 0.6rem 1rem; margin: 0.5rem 0; max-width: 85%;
    font-size: 0.85rem; line-height: 1.65; white-space: pre-wrap;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #1a5276, #2980b9) !important;
    color: white !important; border: none !important; border-radius: 8px !important;
    padding: 0.6rem 2rem !important; font-weight: 600 !important;
    font-size: 1rem !important; transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(26,82,118,0.3) !important;
}

/* Text area */
div[data-testid="stTextArea"] textarea {
    font-family: 'JetBrains Mono', 'Noto Sans TC', monospace !important;
    font-size: 0.85rem !important; border-radius: 8px !important;
    border: 1.5px solid var(--border) !important; line-height: 1.7 !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--primary-light) !important;
    box-shadow: 0 0 0 2px rgba(41,128,185,0.15) !important;
}

.tips-box {
    background: #eef6fc; border: 1px solid #bdd7ee; border-radius: 8px;
    padding: 1rem 1.2rem; font-size: 0.85rem; color: #1a5276; line-height: 1.6;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
.stTabs [data-baseweb="tab"] { border-radius: 8px 8px 0 0; font-weight: 600; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ══════════════════════════════════════════════════════════════

SYSTEM_PROMPT = r"""You are an experienced clinical physician and medical educator.

CRITICAL LANGUAGE RULE:
The ENTIRE medical note content MUST be written in ENGLISH. Even if the user input is in Chinese, you MUST write all clinical content (Chief Complaint, Present Illness, Past History, Personal History, Impression, Plan, etc.) in English.
The ONLY Chinese allowed is the section headers themselves (e.g. "主訴 (Chief Complaint)").
Do NOT write any clinical narrative, findings, or plans in Chinese. All body text must be in English.
This is non-negotiable.

Your task is to convert raw patient encounter information into a structured medical note suitable for clinical documentation training.

The input may be a standardized patient script, outpatient note, emergency note, or incomplete clinical information.

If information is incomplete, you should infer and expand the history using reasonable general medical knowledge of the suspected disease, while keeping the content realistic and clinically consistent.

Do NOT fabricate extreme or unlikely findings.

The format must closely follow the structure of a real hospital admission note, including the following sections:

Chief Complaint  
Present Illness  
Past History  
Personal History  
Review of System  
Physical Examination  
Impression  
Plan

The output must follow the same style and structure used in real hospital notes.

--------------------------------------------------

INPUT
The user will provide:
- Outpatient note / ER note / standardized patient script
- Possibly incomplete clinical information

If the information is incomplete:
- Expand the history based on reasonable general medical knowledge of the suspected disease.
- Do NOT invent rare findings.
- Keep the case clinically realistic.

--------------------------------------------------

OUTPUT FORMAT

主訴 (Chief Complaint)
- One concise sentence including symptom and duration.

現在病症 (Present Illness)
Use narrative paragraph style similar to hospital documentation.
Avoid bullet points.
Write a complete clinical narrative including:

• Patient basic information (age, sex, ADL status if available)  
• Relevant underlying diseases  
• Symptom onset and duration  
• Symptom characteristics (refer to LQQOPERA, keep it focused, avoid redundancy)
• Associated symptoms  
• Pertinent negatives  
• Reason for ER visit or clinic visit  

If ER course or investigations are mentioned:
Summarize important findings. Vital signs must use the following concise inline format ONLY:
T:XX.X P:XX R:XX SBP:XXX DBP:XX E:X V:X M:X SPO2:XX%
Do NOT expand vital signs into narrative sentences. Keep them as a single compact line.

Important abnormal laboratory findings.
Imaging findings (CXR / ECG / CT / KUB etc.)

ER medications and interventions: write concisely, omit dosages — just name the drug/procedure briefly (e.g. "Empirical Ceftriaxone was given", "Normal saline hydration was initiated").

Conclude with: Under the impression of ....(tentative diagnosis), he/she was admitted to our ward for further management.

--------------------------------------------------

過去病史 (Past History)

List:
• Chronic diseases  
• Operation history  
• Previous admission history

--------------------------------------------------

個人病史 (Personal History)

Include:

Allergy  
Alcohol  
Smoking  
Betelnut  

If information is missing:
Assume reasonable defaults such as "denied".

--------------------------------------------------

系統整理 (Review of System)

CRITICAL FORMATTING RULE FOR HIGHLIGHTING:
For any ROS item that you CHANGE from the default template value (i.e. changed from "no" to "yes", or from "normal" to something abnormal), you MUST wrap ONLY the changed value with double asterisks.
Example: if fever changes from no to yes, write: fever:( **yes**)
Items that remain at their default template value must NOT have asterisks.

CRITICAL FORMATTING RULE FOR COPY-PASTE:
The ROS MUST be output as a numbered list exactly matching the template below.
Each numbered item must start on its own line with the number prefix (e.g. "1. General：").
Sub-items under HEENT (a. Head, b. Eyes, etc.) must each start on their own indented line.
This ensures the numbering is preserved when copying.

Keep the full structure of the template. Modify only relevant symptoms.
Keep the entire template structure unchanged. Only modify the content inside parentheses. Do NOT delete template lines.
請記得根據男女性別去調整

##Template: 

1. General：
    weakness:( no), fatigue:( no), anorexia:( no), fever:( no), insomnia:( no)
2. Integument (skin, hair and nails)：
    changes in color:( no), pruritus:( no), rash:( no), hair loss:( no)
3. HEENT：
    a. Head - headache:( no), dizziness:( no), vertigo:( no)
    b. Eyes - visual acuity:( normal), color vision:( normal), corrective lenses:( no), photophobia:( no), diplopia:( no), pain:( no)
    c. Ears - pain:( no), discharge:( no), hearing loss:( no), tinnitus:( no)
    d. Nose - epistaxis:( no), discharge:( no), stuffiness:( no), sense of smell:( normal)
    e. Throat - status of teeth:( normal), gums:( normal), dentures:( no), taste:( normal), soreness:( no), hoarseness:( no), lump:( no)
4. Respiratory：cough:( no), sputum:( no), hemoptysis:( no), wheezing:( no), dyspnea:( no)
5. CV：edema:( no), chest distress:( no), chest pain:( no), palpitation:( no), intermittent claudication:( no), cold limbs:( no), cyanosis:( no)
6. GI：dysphagia:( no), nausea:( no), vomiting:( no), abdominal distress/pain:( no), change in bowel habit:( no), hematemesis:( no), melena:( no), bloody stool:( no)
7. GU：urinary frequency:( no), hesitancy:( no), urgency:( no), dribbling:( no), incontinence:( no), dysuria:( no), hematuria:( no), nocturia:( no), polyuria:( no)
8. Metabolic and endocrine：growth:( fair), development:( normal), weight change:( no), heat/cold intolerance:( no), nervousness:( no), sweating:( no), polydipsia:( no)
9. Hematotologic: anemia:( no), easy bruising or bleeding:( no), lymphadenopathy:( no), transfusions:( no)
10. Neuropsychiatry：dizziness:( no), syncope:( no), seizure:( no), speech disturbance:( no), loss of sensation:( no), paresthesia:( no), ataxia:( no), weakness or paralysis:( no), tremor:( no), anxiety:( no), depression:( no), irritability:( no)
11. Musculoskeletal：joint pain:( no), stiffness:( no), limitation of motion:( no), muscular weakness:( no), muscle wasting:( no)

--------------------------------------------------

理學檢查 (Physical Examination)

CRITICAL FORMATTING RULE FOR HIGHLIGHTING:
For any PE finding that you CHANGE from the default template value, you MUST wrap ONLY the changed text with double asterisks like **changed finding here**.
Items left at their default template value should NOT have asterisks.

CRITICAL FORMATTING RULE FOR COPY-PASTE:
Do NOT insert blank lines between PE sections or between lines within a section.
Every line of the PE should follow immediately after the previous line with no empty lines in between.
The output should be compact — section headers (GENERAL APPEARANCE, CONSCIOUSNESS, etc.) go on their own line, and their content follows on the next line(s), with NO extra blank lines anywhere.

Maintain the same structure. Modify abnormal findings based on the disease.
Keep normal findings unchanged. Do NOT remove sections. Modify only the specific abnormal findings.
Ensure PE findings are consistent with the clinical presentation.

## Template:

GENERAL APPEARANCE:
    chronic ill looking
CONSCIOUSNESS:
    Clear, E 4 V 5 M 6
HEENT:
    Sclerae: NOT icteric
    Conjunctivae: not arrow pale
    Oral cavity : Intact oral mucosa
NECK:
    Supple
    No jugular vein engorgement
CHEST:
    Breath pattern: smooth, Bilateral symmetric expansion
    No USE OF accessory muscles
    Breathing sound: bilateral clear AND symmetric breathing sound
    Wheezing: No wheezing
    Crackles: No basal crackles
HEART:
    Regular heart beat without audible murmur
    No audible S3; No audible S4
ABDOMEN:
    flat and soft, normoactive bowel sound
    No tenderness; No rebounding pain
    No muscle guarding
    No Murphy's sign
BACK:
    No knocking pain over bilateral flank area
EXTREMITIES:
    No joint deformity
    Freely movable
    No pitting edema
    Peripheral pulse: symmetric
SKIN:
    No petechiae OR ecchymosis
    No abnormal skin rash
    Skin intact
    No wound

--------------------------------------------------

臨床臆斷 (Impression)

Provide: 
List problems in clinical priority order.
Include important abnormal laboratory findings as diagnoses if clinically relevant.

1. Primary diagnosis, followed by rule-out secondary/differential diagnoses on the same line.
2. Antibiotics and critical medications: list on a SEPARATE line, grouped together. Include start date. Do NOT include dosage. Format example:
   Antibiotics: Ceftriaxone (D1: 2025/01/15), Metronidazole (D1: 2025/01/15)
3. Underlying diseases with past history information.

Use numbered format.

--------------------------------------------------

處理計畫 (Plan)

The plan MUST contain at least 3 items and no more than 6 items total. Only include clinically important items.

Divide into three sections:

Diagnostic
• Only the most important labs, imaging, or evaluations for this case.

Therapeutic
• Key medications (no dosages), fluid management if relevant, core interventions only.

Measurable goal
• 1–2 specific clinical targets with timeframe (include days).

Do NOT list exhaustive or routine orders. Keep it focused and realistic.
The total number of items across all three sections must be at least 3.

--------------------------------------------------

IMPORTANT RULES

1. The final output should read like a real hospital admission note.

2. Maintain internal consistency between:
Present illness
ROS
Physical examination
Impression
Plan

3. If the provided information is limited:
Expand the clinical story using common presentations of the disease.

4. ALL clinical content MUST be in English. The user input may be in Chinese — translate and write everything in English. Only section headers (主訴, 現在病症, etc.) may contain Chinese. Every sentence of the note body — Present Illness, ROS values, PE findings, Impression, Plan — must be in English. No exceptions.

5. Do NOT output explanations. Only output the final medical note. Do not include commentary, reasoning explanation, or teaching notes.

6. Avoid overly polished or AI-sounding phrasing. Write like a real clinician documenting a case — direct, efficient, no filler words. Prefer short declarative sentences. Avoid phrases like "comprehensive evaluation", "meticulous", "notably", "it is important to note". Just write the note.

7. MANDATORY: wrap ALL changed ROS values and PE findings with **double asterisks**. Unchanged default values must NOT have asterisks. This is critical for the red-highlight display system."""


LEARNING_ZONE_PROMPT = """You are a senior attending physician teaching a medical student.

Based on the following generated medical note, provide a concise clinical learning summary in Traditional Chinese (繁體中文). Use medical English terms where appropriate (e.g. disease names, drug names, lab items).

Format your response EXACTLY using these markdown headers. The output will be rendered as markdown:

#### 📌 主要診斷與臨床推理
Briefly explain why this is the most likely diagnosis based on the presentation (2-3 sentences max).

#### 🔍 鑑別診斷

Present a markdown table comparing the differential diagnoses. Use this exact format:

| 鑑別診斷 | 支持點 | 不支持點 |
|---------|--------|---------|
| Disease A | supporting features | against features |
| Disease B | supporting features | against features |
| Disease C | supporting features | against features |

Include 3-5 differential diagnoses. Keep each cell to one short sentence.

#### 💊 治療原則與藥物建議
List 3-5 key treatment items as bullet points. For each:
- State the drug NAME, DOSE, ROUTE, and FREQUENCY (e.g. Ceftriaxone 2g IV Q24H).
- Briefly state the clinical rationale.
- Reference the relevant guideline or standard of care if applicable (e.g. IDSA guideline, AHA guideline, Surviving Sepsis Campaign, UpToDate recommendation, etc.).

After the list, add a short paragraph titled **⚠️ Guideline 符合度檢查** that reviews whether the current treatment plan in the medical note aligns with the latest guideline recommendations. If there are discrepancies or areas for improvement, point them out specifically. If it is largely compliant, state so briefly.

#### 🔬 建議進一步檢查
List 3-5 recommended next-step labs/imaging/evaluations as bullet points. For each, briefly state the clinical rationale.

#### ⚡ 學習重點摘要
List 3-5 high-yield take-home points — the kind of pearls for exams and clinical practice.

If there is an especially useful comparison or classification that benefits from a table (e.g. comparing similar diseases, classifying severity, staging criteria, antibiotic spectrum comparison), include an additional markdown table in this section. Label it clearly. Only add a table if it genuinely aids learning — do not force one.

Rules:
- Be concise and direct. No filler.
- Use 繁體中文 for explanations, English for medical terms.
- Drug dosages must follow standard adult dosing from current guidelines.
- Do not repeat the medical note content verbatim.
- Avoid AI-sounding phrases. Write like a real attending at bedside.
- Use bullet points (- ) for list items.
- Use proper markdown table syntax with | and header separators."""


CHAT_SYSTEM_PROMPT = """You are a senior attending physician answering questions from a medical student about a specific patient case.

You have access to the complete medical note below. Answer questions based on the information in the note. If the answer is not in the note, say so clearly and offer your clinical reasoning based on the likely diagnosis.

Be concise, direct, and use clinical language. Answer in the same language the student uses (繁體中文 or English).
Do not repeat the entire note. Just answer the specific question.
Avoid AI-sounding filler phrases.

===== MEDICAL NOTE =====
{note}
==========================="""


# ══════════════════════════════════════════════════════════════
# HELPER: highlight **text** → red HTML spans
# ══════════════════════════════════════════════════════════════

def highlight_changes(text: str) -> str:
    """Convert **text** markers to red-highlighted HTML spans."""
    escaped = html_lib.escape(text)
    highlighted = re.sub(
        r'\*\*(.+?)\*\*',
        r'<span class="red">\1</span>',
        escaped,
    )
    return highlighted


# ══════════════════════════════════════════════════════════════
# HELPER: call Anthropic API
# ══════════════════════════════════════════════════════════════

def call_claude(api_key: str, system: str, user_msg: str, max_tokens: int = 4096) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    )
    return message.content[0].text


def call_claude_multi(api_key: str, system: str, messages: list, max_tokens: int = 1024) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    return response.content[0].text


# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div class="header-banner">
    <h1>🏥 學習病歷產生器</h1>
    <p>貼入病患資訊（門診紀錄 / 急診紀錄 / 標準化病人腳本），自動產生結構化學習病歷 · 學習重點 · AI 問答</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar: API key ────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ 設定")
    api_key = st.text_input("Anthropic API Key", type="password", help="輸入你的 Anthropic API Key")
    st.markdown("---")
    st.markdown("""
<div style="font-size:0.8rem; color:#7f8c8d; line-height:1.6;">
<b>使用說明</b><br>
1. 在左側輸入 API Key<br>
2. 在主頁貼入病患資料<br>
3. 按下「產生學習病歷」<br>
4. 查看病歷、學習重點、與 AI 對話
</div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
<div style="font-size:0.78rem; color:#95a5a6; line-height:1.5;">
<b>功能說明</b><br>
📝 <b>學習病歷</b>：ROS/PE 更動處以<span style="color:#c0392b;">紅字</span>標示<br>
📚 <b>學習重點</b>：診斷推理、鑑別診斷、治療原則<br>
💬 <b>AI 問答</b>：根據病歷內容直接提問
</div>
    """, unsafe_allow_html=True)

# ── Initialize session state ────────────────────────────────
if "result" not in st.session_state:
    st.session_state["result"] = ""
if "learning" not in st.session_state:
    st.session_state["learning"] = ""
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "patient_data_saved" not in st.session_state:
    st.session_state["patient_data_saved"] = ""

# ══════════════════════════════════════════════════════════════
# LAYOUT: Input (left) | Output tabs (right)
# ══════════════════════════════════════════════════════════════

col_input, col_output = st.columns([2, 3], gap="large")

# ── LEFT: Input ─────────────────────────────────────────────
with col_input:
    st.markdown('<div class="section-label">📋 貼入病患資料</div>', unsafe_allow_html=True)

    patient_data = st.text_area(
        "病患資料",
        height=400,
        placeholder="在此貼入門診紀錄 / 急診紀錄 / 標準化病人腳本...\n\n範例：\n65歲男性，主訴右上腹痛3天，過去病史有高血壓、糖尿病。\n急診抽血顯示WBC 15000, CRP 12.5, GOT 85, GPT 92...",
        label_visibility="collapsed",
    )

    st.markdown("""
<div class="tips-box">
💡 <b>輸入提示</b>：可接受門診紀錄、急診紀錄、SP 腳本，或簡短的臨床摘要。<br>
資訊不完整時，AI 會根據疾病的常見表現合理補充。<br>
🔴 ROS 與 PE 中有更動的項目會以<span style="color:#c0392b;font-weight:700;">紅色字體</span>標示。
</div>
    """, unsafe_allow_html=True)

    generate_btn = st.button("🩺 產生學習病歷", use_container_width=True)

    # Handle generation
    if generate_btn:
        if not api_key:
            st.error("請先在左側欄輸入 Anthropic API Key。")
        elif not patient_data.strip():
            st.error("請在左側貼入病患資料。")
        else:
            # Reset previous results
            st.session_state["result"] = ""
            st.session_state["learning"] = ""
            st.session_state["chat_history"] = []
            st.session_state["patient_data_saved"] = patient_data.strip()

            with st.spinner("正在生成學習病歷，請稍候⋯"):
                try:
                    result = call_claude(api_key, SYSTEM_PROMPT, patient_data.strip())
                    st.session_state["result"] = result
                except Exception as e:
                    st.error(f"病歷生成錯誤：{str(e)}")

            # Auto-generate learning zone
            if st.session_state["result"]:
                with st.spinner("正在生成學習重點⋯"):
                    try:
                        learning = call_claude(
                            api_key, LEARNING_ZONE_PROMPT,
                            st.session_state["result"], max_tokens=3072,
                        )
                        st.session_state["learning"] = learning
                    except Exception:
                        st.session_state["learning"] = "（學習重點生成失敗，請重試）"
                st.rerun()

# ── RIGHT: Output tabs ──────────────────────────────────────
with col_output:
    if st.session_state["result"]:
        tab_note, tab_learn, tab_chat = st.tabs([
            "📝 學習病歷",
            "📚 學習重點",
            "💬 AI 問答",
        ])

        # ── Tab 1: Medical Note ─────────────────────────────
        with tab_note:
            result = st.session_state["result"]

            st.download_button(
                label="📥 下載病歷 (.txt)",
                data=result,
                file_name="learning_medical_note.txt",
                mime="text/plain",
                use_container_width=True,
            )

            # Highlight **changed** items in red
            highlighted_html = highlight_changes(result)
            st.markdown(
                f'<div class="output-card">{highlighted_html}</div>',
                unsafe_allow_html=True,
            )

            st.markdown("""
<div style="font-size:0.78rem; color:#95a5a6; margin-top:0.5rem;">
    🔴 <span style="color:#c0392b; font-weight:600;">紅色字體</span> = ROS / PE 中與預設模板不同的項目（AI 根據病歷更動）
</div>
            """, unsafe_allow_html=True)

        # ── Tab 2: Learning Zone ────────────────────────────
        with tab_learn:
            st.markdown('<div class="section-label-green">📚 臨床學習重點</div>', unsafe_allow_html=True)

            if st.session_state["learning"]:
                st.markdown(st.session_state["learning"])
            else:
                st.info("學習重點將在病歷生成後自動產生。")

        # ── Tab 3: AI Chat ──────────────────────────────────
        with tab_chat:
            st.markdown('<div class="section-label-purple">💬 病歷 AI 問答</div>', unsafe_allow_html=True)
            st.caption("根據生成的病歷內容提問，例如：「病患有無發燒？」「為什麼選擇這個抗生素？」「還需要做什麼檢查？」")

            # Display chat history
            if st.session_state["chat_history"]:
                chat_html_parts = []
                for msg in st.session_state["chat_history"]:
                    escaped_content = html_lib.escape(msg["content"])
                    if msg["role"] == "user":
                        chat_html_parts.append(f'<div class="chat-msg-user">{escaped_content}</div>')
                    else:
                        chat_html_parts.append(f'<div class="chat-msg-ai">{escaped_content}</div>')
                st.markdown(
                    f'<div class="chat-container">{"".join(chat_html_parts)}</div>',
                    unsafe_allow_html=True,
                )

            # Chat input
            chat_input = st.text_input(
                "提問",
                placeholder="輸入你的問題⋯",
                key="chat_input_field",
                label_visibility="collapsed",
            )

            col_send, col_clear = st.columns([3, 1])
            with col_send:
                send_btn = st.button("送出提問", use_container_width=True, key="send_chat_btn")
            with col_clear:
                clear_btn = st.button("清除對話", use_container_width=True, key="clear_chat_btn")

            if clear_btn:
                st.session_state["chat_history"] = []
                st.rerun()

            if send_btn and chat_input.strip():
                if not api_key:
                    st.error("請先輸入 API Key。")
                else:
                    st.session_state["chat_history"].append(
                        {"role": "user", "content": chat_input.strip()}
                    )

                    # Build conversation messages
                    system = CHAT_SYSTEM_PROMPT.format(note=st.session_state["result"])
                    api_messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state["chat_history"]
                    ]

                    with st.spinner("AI 回覆中⋯"):
                        try:
                            answer = call_claude_multi(api_key, system, api_messages)
                            st.session_state["chat_history"].append(
                                {"role": "assistant", "content": answer}
                            )
                        except Exception as e:
                            st.session_state["chat_history"].append(
                                {"role": "assistant", "content": f"錯誤：{str(e)}"}
                            )
                    st.rerun()

    else:
        # Empty state
        st.markdown("""
<div style="
    border: 2px dashed #d5dde5; border-radius: 12px;
    padding: 4rem 2rem; text-align: center; color: #95a5a6; margin-top: 0.5rem;
">
    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📄</div>
    <div style="font-size: 1rem;">產生的學習病歷將顯示在此處</div>
    <div style="font-size: 0.85rem; margin-top: 0.3rem;">請先在左側貼入資料並按下按鈕</div>
    <div style="font-size: 0.8rem; margin-top: 1rem; color: #bdc3c7;">
        生成後可切換：📝 病歷 ｜ 📚 學習重點 ｜ 💬 AI 問答
    </div>
</div>
        """, unsafe_allow_html=True)
