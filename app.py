import streamlit as st
import pandas as pd
import re
from pathlib import Path

st.set_page_config(
    page_title="CYBER PHANTOM | TallyBridge Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- CREATIVE FRONTEND ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {
  background:
    radial-gradient(circle at 8% 4%, rgba(124,58,237,.22), transparent 27%),
    radial-gradient(circle at 92% 8%, rgba(6,182,212,.18), transparent 25%),
    linear-gradient(135deg,#080d1c 0%,#10172d 52%,#111827 100%);
  color:#f8fafc;
}
.block-container {padding-top:1.5rem; padding-bottom:3rem; max-width:1450px;}
h1,h2,h3 {font-family:'Space Grotesk',sans-serif !important; color:#f8fafc !important;}
p, label, .stMarkdown {color:#dbeafe;}
div[data-testid="stMetric"] {
  background:linear-gradient(135deg,rgba(30,41,59,.95),rgba(49,46,129,.45));
  border:1px solid rgba(129,140,248,.35); padding:18px 20px; border-radius:18px;
  box-shadow:0 10px 28px rgba(0,0,0,.18);
}
div[data-testid="stMetricLabel"] {color:#a5b4fc !important;}
div[data-testid="stMetricValue"] {color:#fff !important; font-family:'Space Grotesk',sans-serif;}
div[data-testid="stFileUploader"] {
  background:rgba(30,41,59,.72); border:1px dashed #818cf8; border-radius:18px; padding:12px;
}
.stButton>button, .stDownloadButton>button {
  background:linear-gradient(90deg,#7c3aed,#2563eb,#0891b2) !important;
  color:white !important; border:0 !important; border-radius:12px !important;
  padding:.65rem 1rem !important; font-weight:700 !important;
  box-shadow:0 6px 18px rgba(37,99,235,.25);
}
.stButton>button:hover, .stDownloadButton>button:hover {filter:brightness(1.15); transform:translateY(-1px);}
div[data-testid="stDataFrame"] {border:1px solid rgba(129,140,248,.28); border-radius:14px; overflow:hidden;}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#111827,#1e1b4b);}
section[data-testid="stSidebar"] * {color:#e0e7ff !important;}
div[data-testid="stAlert"] {border-radius:14px;}
hr {border-color:rgba(148,163,184,.25);}
.hero {
  background:linear-gradient(110deg,rgba(124,58,237,.30),rgba(37,99,235,.20),rgba(8,145,178,.20));
  border:1px solid rgba(165,180,252,.35); border-radius:24px; padding:26px 30px;
  box-shadow:0 16px 40px rgba(0,0,0,.22); margin-bottom:20px;
}
.hero-kicker {letter-spacing:3px;text-transform:uppercase;color:#a5f3fc;font-size:12px;font-weight:800;}
.hero-title {font-family:'Space Grotesk';font-size:clamp(30px,4vw,48px);font-weight:700;color:#fff;line-height:1.05;margin:8px 0;}
.hero-sub {color:#dbeafe;font-size:15px;max-width:800px;}
.pill {display:inline-block;border-radius:999px;padding:6px 11px;margin:4px 6px 0 0;font-size:11px;font-weight:800;letter-spacing:.7px;background:#312e81;color:#c7d2fe;border:1px solid #6366f1;}
.section-tag {color:#67e8f9;font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;}
.info-card {background:rgba(30,41,59,.72);border:1px solid rgba(148,163,184,.22);border-radius:16px;padding:16px 18px;height:100%;}
.info-card h4 {color:#a5b4fc;margin:0 0 7px 0;font-family:'Space Grotesk';}
.info-card p {color:#e2e8f0;margin:0;font-size:14px;}
.alert-banner {padding:14px 18px;border-radius:15px;background:linear-gradient(90deg,rgba(220,38,38,.20),rgba(234,88,12,.13));border:1px solid rgba(248,113,113,.42);color:#fee2e2;}
.good-banner {padding:14px 18px;border-radius:15px;background:linear-gradient(90deg,rgba(5,150,105,.18),rgba(8,145,178,.13));border:1px solid rgba(52,211,153,.4);color:#d1fae5;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="hero-kicker">CYBER PHANTOM · CRIMEATHON TIER 3</div>
  <div class="hero-title">TALLYBRIDGE <span style="color:#67e8f9">SHIELD</span></div>
  <div class="hero-sub">Integration abuse detection console — inspect evidence, correlate requests, and surface vendor payment-change risks.</div>
  <span class="pill">OFFLINE EVIDENCE ANALYSIS</span>
  <span class="pill">EXPLAINABLE RULE ENGINE</span>
  <span class="pill">INVESTIGATOR REVIEW</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🛡️ Control Center")
st.sidebar.caption("CYBER PHANTOM / Defense Operations")
st.sidebar.markdown("---")
st.sidebar.markdown("**Analysis workflow**")
st.sidebar.markdown("① Upload CSV evidence  \n② Inspect column mapping  \n③ Run detection  \n④ Review & export alerts")
st.sidebar.markdown("---")
st.sidebar.info("This tool works only on CSV files supplied by the investigator. It does not connect to, scan, or modify real systems.")

# ---------- ROBUST COLUMN MATCHING ----------
def norm(value):
    return re.sub(r"[^a-z0-9]", "", str(value).lower())

ALIASES = {
    "request": ["request_id","requestid","correlation_id","correlationid","trace_id","transaction_id"],
    "vendor": ["vendor_id","vendorid","supplier_id","supplierid","vendor_code"],
    "action": ["action","event_type","eventtype","operation","activity","event","description","message","endpoint","api_endpoint","request_path","url"],
    "old": ["old_account","old_bank_account","previous_account","old_account_number","from_account","old_value","previous_value"],
    "new": ["new_account","new_bank_account","updated_account","new_account_number","to_account","new_value","current_value"],
    "approval": ["approval_ref","approval_reference","approval_id","approved_by","approval_code","change_ticket"],
    "key": ["api_key","credential","integration_key","key_id","client_id"],
    "ip": ["source_ip","src_ip","ip_address","client_ip","remote_ip"],
    "host": ["host","hostname","source_host","device","machine"],
    "env": ["environment","target_environment","destination","target_system"],
    "time": ["timestamp","time","event_time","datetime","created_at"],
    "evidence": ["evidence_id","evidence","source_id","log_id","record_id"],
}

def find_col(df, key):
    cols = list(df.columns)
    normalized = {norm(c): c for c in cols}
    for alias in ALIASES[key]:
        if norm(alias) in normalized:
            return normalized[norm(alias)]
    # Fuzzy matching for headers such as "vendor_bank_account_old"
    for c in cols:
        nc = norm(c)
        for alias in ALIASES[key]:
            na = norm(alias)
            if len(na) >= 5 and (na in nc or nc in na):
                return c
    # Directional account-header fallback
    if key == "old":
        for c in cols:
            nc = norm(c)
            if ("old" in nc or "previous" in nc or "from" in nc) and ("account" in nc or "bank" in nc or "value" in nc):
                return c
    if key == "new":
        for c in cols:
            nc = norm(c)
            if ("new" in nc or "updated" in nc or "current" in nc or "to" in nc) and ("account" in nc or "bank" in nc or "value" in nc):
                return c
    return None

def val(row, col):
    if not col:
        return ""
    x = row.get(col, "")
    return "" if pd.isna(x) else str(x).strip()

def detect_change(action_text, old_value, new_value, row_text):
    old_new_differ = bool(old_value and new_value and norm(old_value) != norm(new_value))
    action = action_text.lower()
    combined = (action + " " + row_text).lower()
    change_terms = [
        "bank account change", "bank details change", "account changed",
        "account update", "update account", "updated account",
        "change bank", "update bank", "modify bank", "modify account",
        "vendor update", "beneficiary change", "bank_details_updated",
        "vendor_bank_account_update", "update_vendor_bank_account",
        "change_vendor_bank_account", "account number changed"
    ]
    action_suggests_change = any(term in combined for term in change_terms)
    # Also accept clear change verbs near vendor/bank/account terms.
    has_subject = any(t in combined for t in ["vendor", "supplier", "bank", "account", "beneficiary", "payment"])
    has_verb = any(t in combined for t in ["change", "changed", "update", "updated", "modify", "modified", "edit", "edited", "set"])
    return old_new_differ or (has_subject and has_verb) or action_suggests_change

def analyse(frames):
    alerts, diagnostics = [], []
    request_evidence = {}
    for filename, df in frames:
        mapping = {key: find_col(df, key) for key in ALIASES}
        diagnostics.append({
            "File": filename, "Rows": len(df),
            "Action/event column": mapping["action"] or "Not found",
            "Old account column": mapping["old"] or "Not found",
            "New account column": mapping["new"] or "Not found",
            "Approval column": mapping["approval"] or "Not found",
            "Request ID column": mapping["request"] or "Not found",
        })
        for row_index, row in df.iterrows():
            action = val(row, mapping["action"])
            old_value, new_value = val(row, mapping["old"]), val(row, mapping["new"])
            # If action is in an unrecognised header, search the complete row as a fallback.
            row_text = " | ".join(f"{k}: {v}" for k, v in row.items() if str(v).strip())
            if not detect_change(action, old_value, new_value, row_text):
                continue

            approval = val(row, mapping["approval"])
            request_id = val(row, mapping["request"])
            vendor = val(row, mapping["vendor"])
            evidence = val(row, mapping["evidence"]) or filename
            key, ip, host, env = (val(row, mapping[k]) for k in ["key","ip","host","env"])
            timestamp = val(row, mapping["time"])

            reasons = ["Vendor/bank/account change pattern detected"]
            score = 55
            if old_value and new_value and norm(old_value) != norm(new_value):
                reasons.append("Old and new account values differ")
                score += 15
            if not approval:
                reasons.append("No approval reference recorded in this CSV row")
                score += 20
            if key:
                reasons.append(f"Integration credential recorded: {key}")
                score += 5
            if ip or host:
                reasons.append("Source IP/host available for verification")
                score += 5
            score = min(score, 100)
            level = "HIGH" if score >= 75 else "MEDIUM"
            alerts.append({
                "Risk": level, "Score": score, "Alert": "Potential vendor bank-account change",
                "Evidence ID": evidence, "Request ID": request_id or "Not supplied",
                "Vendor ID": vendor or "Not supplied",
                "Old account": old_value or "Not supplied",
                "New account": new_value or "Not supplied",
                "Approval reference": approval or "Blank / not supplied",
                "Credential": key or "Not supplied", "Source IP": ip or "Not supplied",
                "Host": host or "Not supplied", "Environment": env or "Not supplied",
                "Timestamp": timestamp or "Not supplied", "Input file": filename,
                "CSV row": row_index + 2, "Reason": "; ".join(reasons)
            })
            if request_id:
                request_evidence.setdefault(request_id, set()).add(evidence)

    for alert in alerts:
        rid = alert["Request ID"]
        linked = sorted(request_evidence.get(rid, set())) if rid != "Not supplied" else []
        alert["Same-request evidence"] = ", ".join(linked) if linked else "No matching flagged request ID"
    return alerts, diagnostics

def demo_frames():
    e18 = pd.DataFrame([{
        "evidence_id":"E18","timestamp":"2026-09-03 10:14:22","request_id":"req-5f61b0de8",
        "vendor_id":"V-0412","action":"GET vendor bank details and scheduled payments",
        "api_key":"key-tb-07","source_ip":"10.20.4.77","host":"tb-build-02","environment":"production"
    }])
    e19 = pd.DataFrame([{
        "evidence_id":"E19","timestamp":"2026-09-03 10:16:05","request_id":"req-5f61b0de8",
        "vendor_id":"V-0412","action":"UPDATE vendor bank account","old_account":"4417",
        "new_account":"9083","approval_ref":"","api_key":"key-tb-07",
        "source_ip":"10.20.4.77","host":"tb-build-02","environment":"production"
    }])
    return [("E18_demo.csv", e18), ("E19_demo.csv", e19)]

# ---------- INPUT ----------
left, right = st.columns([1.35, 1])
with left:
    st.markdown('<div class="section-tag">01 / Evidence intake</div>', unsafe_allow_html=True)
    uploads = st.file_uploader("Drop your evidence CSV files here", type=["csv"], accept_multiple_files=True)
with right:
    st.markdown('<div class="section-tag">Quick test</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card"><h4>Try the sample incident</h4><p>Loads synthetic E18 and E19 rows that reproduce the vendor account-change scenario for a safe demonstration.</p></div>', unsafe_allow_html=True)
    demo_clicked = st.button("⚡ Load demo incident", use_container_width=True)

if demo_clicked:
    st.session_state["demo_mode"] = True
    st.session_state["last_upload_names"] = []

if uploads:
    st.session_state["demo_mode"] = False
    st.session_state["last_upload_names"] = [f.name for f in uploads]

frames = []
if uploads:
    for file in uploads:
        try:
            df = pd.read_csv(file, dtype=str, keep_default_na=False)
            df.columns = [str(c).strip() for c in df.columns]
            frames.append((file.name, df))
        except Exception as exc:
            st.error(f"Could not read {file.name}: {exc}")
elif st.session_state.get("demo_mode"):
    frames = demo_frames()

if not frames:
    st.markdown("""
    <div class="info-card">
      <h4>👋 Ready for investigation</h4>
      <p>Upload one or more CSV evidence files, or use the demo incident to verify that the alert engine is working.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ---------- ANALYSIS ----------
alerts, diagnostics = analyse(frames)
total_rows = sum(len(df) for _, df in frames)
high_count = sum(1 for a in alerts if a["Risk"] == "HIGH")
st.markdown('<div class="section-tag">02 / Live analysis overview</div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Evidence files", len(frames))
m2.metric("Records inspected", total_rows)
m3.metric("Potential change alerts", len(alerts))
m4.metric("High-risk alerts", high_count)

st.markdown('<div class="section-tag">03 / Detection results</div>', unsafe_allow_html=True)
if alerts:
    st.markdown(f'<div class="alert-banner">🚨 <b>{len(alerts)} potential change alert(s) found.</b> Review the source records before making a conclusion.</div>', unsafe_allow_html=True)
    result = pd.DataFrame(alerts)
    for i, a in enumerate(alerts, 1):
        with st.expander(f"🚩 {a['Risk']} RISK · {a['Alert']} · {a['Evidence ID']} · {a['Vendor ID']}", expanded=(i == 1)):
            c1, c2, c3 = st.columns(3)
            c1.metric("Risk score", f"{a['Score']}/100")
            c2.metric("Vendor", a["Vendor ID"])
            c3.metric("Request ID", a["Request ID"])
            st.write(f"**Account change:** {a['Old account']}  →  **{a['New account']}**")
            st.write(f"**Approval reference:** {a['Approval reference']}")
            st.write(f"**Source:** {a['Source IP']} · {a['Host']} · {a['Environment']}")
            st.write(f"**Evidence correlation:** {a['Same-request evidence']}")
            st.caption(a["Reason"])
    st.dataframe(result, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download investigation alert report", result.to_csv(index=False).encode("utf-8"),
                       "cyber_phantom_alert_report.csv", "text/csv")
else:
    st.markdown('<div class="good-banner">✓ No change indicators matched the current detection rules in these uploaded rows.</div>', unsafe_allow_html=True)
    st.info("A zero-alert result is not proof that the evidence is clean. Check the column mapping below and compare it with the original evidence.")

st.markdown('<div class="section-tag">04 / Input column diagnostics</div>', unsafe_allow_html=True)
st.caption("This table helps identify why an alert might not be detected. If an important column says 'Not found', your CSV may use a different header.")
st.dataframe(pd.DataFrame(diagnostics), use_container_width=True, hide_index=True)

with st.expander("🔎 View uploaded evidence preview"):
    for filename, df in frames:
        st.markdown(f"**{filename}**")
        st.dataframe(df.head(20), use_container_width=True, hide_index=True)

with st.expander("🧭 How this alert is assessed"):
    st.markdown("""
    - A row is flagged when old/new account values differ, or the row text indicates a vendor/bank/account change.
    - A blank approval reference increases the rule score, but does **not** prove that approval never existed.
    - Credential, IP and host fields provide investigation context; they are not automatically treated as malicious.
    - The score is a transparent rule score, not a probability or AI confidence score.
    - Verify findings against the original evidence and authoritative approval/payment records.
    """)

st.divider()
st.caption("CYBER PHANTOM · TallyBridge Shield · Offline CSV prototype · No real-system access or payment blocking")
