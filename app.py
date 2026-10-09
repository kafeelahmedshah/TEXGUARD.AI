import io
import math
import statistics
from datetime import datetime

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

st.set_page_config(
    page_title="TexGuard AI",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subtitle {
        color: #64748b;
        font-size: 17px;
        margin-top: 0;
    }
    .metric-card {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        background: rgba(248,250,252,.75);
    }
    .defect-box {
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #ef4444;
        background: #fff7f7;
        margin-bottom: 10px;
    }
    .success-box {
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #16a34a;
        background: #f0fdf4;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Demo defect-analysis engine
# NOTE: This is an MVP/prototype.
# A trained CNN/YOLO model can later
# replace this function.
# -----------------------------
DEFECTS = [
    {
        "name": "Stain / Color Irregularity",
        "cause": "Possible dyeing contamination, uneven dye application, or foreign material.",
        "action": "Check dye bath cleanliness, dosing, circulation, and fabric preparation.",
    },
    {
        "name": "Uneven Texture",
        "cause": "Possible variation in yarn density, tension, or fabric formation.",
        "action": "Inspect yarn uniformity, machine settings, tension, and fabric construction.",
    },
    {
        "name": "Possible Hole / Open Area",
        "cause": "Possible broken yarn, mechanical damage, or excessive tension.",
        "action": "Inspect needles/loom parts, yarn strength, tension, and machine condition.",
    },
    {
        "name": "Surface Irregularity",
        "cause": "Possible slub, lint accumulation, finishing variation, or yarn fault.",
        "action": "Inspect yarn quality, cleaning, drafting, and finishing parameters.",
    },
]

def analyze_image(image: Image.Image):
    """Heuristic image analysis for a hackathon MVP.
    It is NOT a trained fabric-defect classifier.
    """
    img = image.convert("RGB")
    small = img.copy()
    small.thumbnail((700, 700))

    arr = np.asarray(small).astype(np.float32)
    gray = (
        0.299 * arr[:, :, 0]
        + 0.587 * arr[:, :, 1]
        + 0.114 * arr[:, :, 2]
    )

    mean = float(gray.mean())
    std = float(gray.std())
    h, w = gray.shape

    # Local variation: compare pixels with a shifted copy.
    dx = np.abs(gray[:, 1:] - gray[:, :-1]).mean() if w > 1 else 0
    dy = np.abs(gray[1:, :] - gray[:-1, :]).mean() if h > 1 else 0
    texture_score = float((dx + dy) / 2)

    # Simple darkness/brightness irregularity.
    dark_ratio = float((gray < max(35, mean * 0.55)).mean())
    bright_ratio = float((gray > min(245, mean * 1.45)).mean())

    # Normalize indicators to 0-100.
    texture_indicator = min(100.0, texture_score * 3.0)
    contrast_indicator = min(100.0, std * 1.8)
    irregularity = min(
        100.0,
        0.45 * texture_indicator
        + 0.35 * contrast_indicator
        + 0.20 * min(100, (dark_ratio + bright_ratio) * 250),
    )

    # Deterministic prototype decision.
    if irregularity < 25:
        quality = "A — Excellent"
        severity = "Low"
        confidence = 82
        detected = []
    elif irregularity < 45:
        quality = "B — Acceptable"
        severity = "Medium"
        confidence = 76
        detected = [DEFECTS[1]]
    elif irregularity < 65:
        quality = "C — Needs Inspection"
        severity = "High"
        confidence = 71
        detected = [DEFECTS[3], DEFECTS[1]]
    else:
        quality = "D — Reject / Recheck"
        severity = "Critical"
        confidence = 68
        detected = [DEFECTS[0], DEFECTS[2]]

    # Add a visual inspection marker based on strongest local variation.
    normalized = np.abs(gray - gray.mean())
    y, x = np.unravel_index(np.argmax(normalized), normalized.shape)

    display_img = small.copy()
    draw = ImageDraw.Draw(display_img)

    box_w = max(50, int(w * 0.18))
    box_h = max(50, int(h * 0.18))
    left = max(0, x - box_w // 2)
    top = max(0, y - box_h // 2)
    right = min(w - 1, left + box_w)
    bottom = min(h - 1, top + box_h)

    if detected:
        draw.rectangle([left, top, right, bottom], outline="red", width=4)
        draw.text((left + 5, max(2, top - 20)), "Possible defect area", fill="red")

    # Estimated waste risk is a presentation/demo metric.
    waste_risk = min(95, max(2, round(irregularity * 0.85)))

    result = {
        "quality": quality,
        "severity": severity,
        "confidence": confidence,
        "irregularity": round(irregularity, 1),
        "texture_score": round(texture_score, 2),
        "waste_risk": waste_risk,
        "detected": detected,
        "mean": round(mean, 1),
        "std": round(std, 1),
        "marked_image": display_img,
    }
    return result


def make_report(filename, result, notes):
    lines = [
        "TEXGUARD AI — FABRIC QUALITY INSPECTION REPORT",
        "=" * 52,
        f"Inspection date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"File: {filename}",
        "",
        f"Quality grade: {result['quality']}",
        f"Severity: {result['severity']}",
        f"Prototype confidence: {result['confidence']}%",
        f"Surface irregularity score: {result['irregularity']}/100",
        f"Estimated waste risk: {result['waste_risk']}%",
        "",
        "Detected / suspected issues:",
    ]

    if result["detected"]:
        for item in result["detected"]:
            lines.append(f"- {item['name']}")
            lines.append(f"  Possible cause: {item['cause']}")
            lines.append(f"  Recommended action: {item['action']}")
    else:
        lines.append("- No major irregularity detected by the prototype.")

    if notes.strip():
        lines.extend(["", "Operator notes:", notes.strip()])

    lines.extend([
        "",
        "IMPORTANT:",
        "This hackathon MVP uses image-statistics heuristics. It is not a certified",
        "industrial inspection system. A trained computer-vision model should be",
        "connected before production use."
    ])
    return "\n".join(lines)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("🧵 TexGuard AI")
    st.caption("AI-assisted textile quality inspection — Hackathon MVP")

    st.divider()
    st.subheader("Inspection Settings")
    fabric_type = st.selectbox(
        "Fabric type",
        ["Woven", "Knitted", "Denim", "Cotton", "Polyester", "Blended", "Other"]
    )
    batch_id = st.text_input("Batch ID", value="BATCH-001")
    operator = st.text_input("Inspector / Operator", value="Student QC")

    st.divider()
    st.info(
        "Prototype mode: the current detector uses image statistics. "
        "For a final hackathon demo, connect a trained YOLO/CNN model."
    )

# -----------------------------
# Header
# -----------------------------
st.markdown('<p class="main-title">🧵 TexGuard AI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">AI-powered fabric quality inspection, defect analysis and QC reporting</p>',
    unsafe_allow_html=True
)

# Project owner / student identity — shown at the top of the app
st.markdown("""
<div style="
    padding: 18px 22px;
    margin: 18px 0 24px 0;
    border-radius: 14px;
    border: 1px solid #bfdbfe;
    background: linear-gradient(120deg, #eff6ff, #f8fafc);
">
    <div style="font-size: 13px; font-weight: 700; letter-spacing: 1px; color: #1d4ed8;">
        PROJECT DEVELOPER
    </div>
    <div style="font-size: 25px; font-weight: 800; color: #0f172a; margin-top: 5px;">
        Syed Kafeel Ahmed Shah
    </div>
    <div style="font-size: 16px; color: #334155; margin-top: 5px;">
        <b>Roll Number:</b> 25TE006
        &nbsp; | &nbsp;
        <b>Department:</b> Textile Engineering
    </div>
    <div style="font-size: 14px; color: #475569; margin-top: 4px;">
        Mehran University of Engineering &amp; Technology (MUET)
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍 Inspection", "📊 Dashboard", "🤖 Textile AI Guide"])

with tab1:
    st.subheader("Upload Fabric Image")
    uploaded = st.file_uploader(
        "Upload a clear fabric/fabric-surface image",
        type=["jpg", "jpeg", "png", "webp"],
        help="For best results, use a well-lit close-up image with the fabric filling most of the frame."
    )

    if uploaded:
        image = Image.open(uploaded)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Original fabric image", use_container_width=True)

        result = analyze_image(image)

        with col2:
            st.image(
                result["marked_image"],
                caption="AI-assisted inspection area",
                use_container_width=True
            )

        st.divider()

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Quality Grade", result["quality"].split(" — ")[0])
        with m2:
            st.metric("Severity", result["severity"])
        with m3:
            st.metric("Confidence", f"{result['confidence']}%")
        with m4:
            st.metric("Waste Risk", f"{result['waste_risk']}%")

        st.subheader("🔎 Inspection Result")

        if result["detected"]:
            for item in result["detected"]:
                st.markdown(
                    f"""
                    <div class="defect-box">
                    <b>{item['name']}</b><br>
                    <b>Possible cause:</b> {item['cause']}<br>
                    <b>Recommended action:</b> {item['action']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div class="success-box"><b>No major irregularity detected.</b><br>'
                'The prototype considers this sample relatively uniform. '
                'A trained production model should be used for final QC.</div>',
                unsafe_allow_html=True
            )

        st.subheader("📈 Technical Indicators")
        c1, c2, c3 = st.columns(3)
        c1.metric("Surface irregularity", f"{result['irregularity']}/100")
        c2.metric("Texture variation", f"{result['texture_score']}")
        c3.metric("Brightness variation", f"{result['std']}")

        st.subheader("📝 QC Notes")
        notes = st.text_area(
            "Add operator observations",
            placeholder="Example: Defect observed near selvedge. Recheck machine tension.",
            height=100,
        )

        report = make_report(uploaded.name, result, notes)
        st.download_button(
            "📄 Download QC Report",
            data=report,
            file_name=f"TexGuard_Report_{batch_id}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.caption(
            f"Fabric: {fabric_type} | Batch: {batch_id} | Operator: {operator}"
        )

    else:
        st.info("Upload a fabric image to start the inspection.")

with tab2:
    st.subheader("📊 Demo Quality Dashboard")
    st.caption("Illustrative dashboard for the hackathon prototype.")

    # Demo data intentionally kept local so the app works without a database.
    demo_batches = [
        ("BATCH-001", 1200, 18, 1.5),
        ("BATCH-002", 980, 31, 3.2),
        ("BATCH-003", 1500, 12, 0.8),
        ("BATCH-004", 1100, 45, 4.1),
    ]

    total = sum(x[1] for x in demo_batches)
    defects = sum(x[2] for x in demo_batches)
    avg_waste = statistics.mean(x[3] for x in demo_batches)

    a, b, c, d = st.columns(4)
    a.metric("Fabric inspected", f"{total:,} m")
    b.metric("Defect events", defects)
    c.metric("Defect rate", f"{defects / len(demo_batches):.1f} / batch")
    d.metric("Avg. waste risk", f"{avg_waste:.1f}%")

    st.subheader("Batch Performance")
    st.table({
        "Batch": [x[0] for x in demo_batches],
        "Inspected (m)": [x[1] for x in demo_batches],
        "Defects": [x[2] for x in demo_batches],
        "Waste Risk %": [x[3] for x in demo_batches],
    })

    st.subheader("🏭 Recommended Hackathon Expansion")
    st.markdown("""
    - Connect a trained **YOLO/CNN fabric-defect model**.
    - Store inspections in **SQLite/PostgreSQL**.
    - Add live camera inspection.
    - Add machine sensor data such as tension, speed and temperature.
    - Predict defect root cause from production parameters.
    - Add PDF/Excel QC reports.
    - Add a factory-level analytics dashboard.
    """)

with tab3:
    st.subheader("🤖 Textile AI Guide")
    st.write("Use these built-in examples during your hackathon presentation.")

    questions = {
        "Why do yarn breaks increase?":
            "Common causes include excessive tension, weak yarn, poor winding, drafting problems, damaged machine parts, or unsuitable machine settings.",
        "How can fabric defects be reduced?":
            "Use better raw-material control, yarn testing, correct machine settings, preventive maintenance, operator training, and continuous inspection.",
        "Why is defect detection important?":
            "Early detection reduces rework, waste, customer complaints, production loss, and the cost of poor quality.",
        "How does AI help textile QC?":
            "Computer vision can inspect fabric images consistently, flag suspicious areas, classify defects, and support faster quality decisions.",
    }

    selected = st.selectbox("Select a question", list(questions.keys()))
    st.success(questions[selected])

    st.divider()
    st.subheader("💡 30-second Project Pitch")
    st.write(
        "TexGuard AI is an AI-assisted textile quality platform that analyzes fabric "
        "images, identifies suspicious defect areas, assigns a quality grade, suggests "
        "possible root causes, estimates waste risk, and generates a QC report. "
        "It combines textile engineering knowledge with computer vision and Industry 4.0."
    )

st.divider()
st.caption("TexGuard AI • Developed by Syed Kafeel Ahmed Shah • 25TE006 • Textile Engineering")
