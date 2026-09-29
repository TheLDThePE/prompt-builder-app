import os
import base64
import logging
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client

logger = logging.getLogger(__name__)
copy_button_component = components.declare_component(
    "prompt_builder_copy_button",
    path=str(Path(__file__).parent / "copy_component"),
)

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="NotebookLM Prompt Builder",
    page_icon="favicon.png",
    layout="wide"
)

# ---------------------------------------------------------
# 1.1 Login Page Style (หน้าแรกก่อนเข้าสู่ระบบ)
# ---------------------------------------------------------
LOGIN_CSS = """
<style>
#MainMenu, header, footer {visibility: hidden !important;}
.stAppDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] {display: none !important;}

.stApp { background: linear-gradient(135deg, #EAF1FB 0%, #FFFFFF 55%, #FDECEE 100%); }
.block-container { max-width: 520px !important; padding-top: 8vh !important; }

/* การ์ด Login */
.st-key-login_card {
    background: #FFFFFF;
    border: 1px solid #E0E7F1 !important;
    border-radius: 16px !important;
    padding: 2rem 2rem 1.5rem 2rem !important;
    box-shadow: 0 10px 30px rgba(18, 48, 90, 0.10);
}
.login-title { font-size: 1.6rem; font-weight: 700; color: #12305A; text-align: center; margin: 0.5rem 0 0.2rem 0; }
.login-sub   { font-size: 0.95rem; color: #5B6B82; text-align: center; margin-bottom: 1.2rem; line-height: 1.6; }
.login-badge { text-align: center; margin-top: 0.9rem; }
.login-badge span { background: #EBF3FE; color: #1E56A0; padding: 3px 12px; border-radius: 12px; font-weight: 600; font-size: 12px; }
.login-foot  { text-align: center; font-size: 11px; color: #7A8799; margin-top: 1rem; }

/* เส้นแบรนด์องค์กร (น้ำเงินยาว + แดงสั้น) */
.brandline { display: flex; height: 3px; margin: 1rem 0 1.2rem 0; }
.brandline span:first-child { flex: 1; background: #1E56A0; }
.brandline span:last-child  { flex: 0 0 18%; background: #D0202E; }

/* ปุ่มล็อกอิน */
.st-key-login_card button {
    background: #1E56A0 !important; color: #FFFFFF !important;
    border: none !important; border-radius: 10px !important;
    padding: 0.6rem 1rem !important; font-weight: 600 !important;
    transition: all .15s ease;
}
.st-key-login_card button:hover { background: #12305A !important; transform: translateY(-1px); }
</style>
"""

# ---------------------------------------------------------
# 1.2 Google Login + Supabase Usage Tracking
# ---------------------------------------------------------
if not st.user.is_logged_in:
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)

    with st.container(border=True, key="login_card"):
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        st.markdown('<div class="brandline"><span></span><span></span></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">NotebookLM Prompt Builder</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="login-sub">เครื่องมือสร้าง Master Prompt สำหรับ Infographic<br>'
            'ตามมาตรฐาน Corporate Identity ของ MinebeaMitsumi</div>',
            unsafe_allow_html=True,
        )
        st.button(
            "เข้าสู่ระบบด้วย Google",
            icon=":material/login:",
            on_click=st.login,
            type="primary",
            use_container_width=True,
        )
        st.markdown('<div class="login-badge"><span>🚀 Trial Version</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-foot">© Developed by Suttichai K.</div>', unsafe_allow_html=True)
    st.stop()

google_sub = st.user.get("sub")
user_email = st.user.get("email")
if not google_sub or not user_email:
    st.error("ไม่พบรหัสผู้ใช้หรืออีเมลจาก Google กรุณาตรวจสอบการตั้งค่า OAuth")
    st.stop()


@st.cache_resource
def get_supabase_client():
    config = st.secrets["supabase"]
    return create_client(config["url"], config["service_role_key"])


try:
    supabase = get_supabase_client()
except Exception:
    logger.exception("Could not initialize the Supabase client")
    st.error(
        "ยังเชื่อมต่อฐานข้อมูลไม่ได้ กรุณาตั้งค่า [supabase] ใน "
        "Streamlit Cloud → Settings → Secrets ให้ครบก่อน"
    )
    st.stop()

# Streamlit reruns the script after interactions. Count once per app session.
if not st.session_state.get("_login_recorded", False):
    try:
        supabase.rpc(
            "record_app_login",
            {"p_google_sub": google_sub, "p_email": user_email},
        ).execute()
        st.session_state["_login_recorded"] = True
    except Exception:
        logger.exception("Could not record an app login")
        st.error("บันทึกข้อมูลการเข้าใช้ไม่สำเร็จ กรุณาลองโหลดหน้าใหม่")
        st.stop()

with st.sidebar:
    st.caption(f"เข้าสู่ระบบ: {user_email}")
    st.button("ออกจากระบบ", on_click=st.logout, use_container_width=True)

# ---------------------------------------------------------
# 2. Custom CSS (ดึงโทนสี MinebeaMitsumi + ล็อก Layout กรอบภาพจาก v3)
# ---------------------------------------------------------
hide_and_custom_style = """
    <style>
    /* ซ่อน UI หลักของ Streamlit */
    #MainMenu, header, footer {visibility: hidden !important;}
    .stAppDeployButton, [data-testid="stStatusWidget"],
    [data-testid="stDecoration"], [data-testid="stToolbar"] {display: none !important;}

    /* การจัดระยะขอบหน้าจอ */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1250px;
    }

    /* โทนสี Title และ Subheader ตาม CI องค์กร */
    h1 { font-size: 1.8rem !important; font-weight: 700 !important; color: #12305A; padding: 0 !important; }
    h3 { font-size: 1.15rem !important; font-weight: 600 !important; color: #12305A; }

    /* เส้นแบรนด์องค์กร (Corporate Accent Line: น้ำเงินยาว + แดงสั้น) */
    .brandline { display: flex; height: 3px; margin: 0.8rem 0 1.5rem 0; }
    .brandline span:first-child { flex: 1; background: #1E56A0; }
    .brandline span:last-child { flex: 0 0 18%; background: #D0202E; }

    /* กรอบพรีวิวภาพคงที่ (Prevent Layout Shift) จาก v3 */
    .pv {
        aspect-ratio: 16 / 9;
        background: #F3F6FB;
        border-radius: 8px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #E0E7F1;
    }
    .pv img { width: 100%; height: 100%; object-fit: contain; display: block; }
    </style>
"""
st.markdown(hide_and_custom_style, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. JavaScript ซ่อน Badge / Watermark มุมขวาล่าง
# ---------------------------------------------------------
js_remove_badges = """
<script>
(function () {
  const SELECTORS = [
    '[class*="viewerBadge"]',
    '[class*="_profileContainer"]',
    '[class*="_profilePreview"]',
    '[data-testid="appCreatorAvatar"]',
    'a[href*="streamlit.io/cloud"]',
    'a[href*="share.streamlit.io"]'
  ];

  function getDocs() {
    const docs = [];
    let w = window;
    for (let i = 0; i < 4; i++) {
      try {
        const p = w.parent;
        docs.push(p.document);
        if (p === w) break;
        w = p;
      } catch (e) { break; }
    }
    return docs;
  }

  function hideFloatingBottomRight(doc) {
    const win = doc.defaultView;
    const vw = win.innerWidth, vh = win.innerHeight;
    doc.querySelectorAll('div, a, button').forEach(el => {
      if (el.querySelector('iframe') || el.tagName === 'IFRAME') return;
      if (win.getComputedStyle(el).position !== 'fixed') return;
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.width < 320 && r.height < 120 &&
          r.right > vw - 320 && r.bottom > vh - 150) {
        el.style.setProperty('display', 'none', 'important');
      }
    });
  }

  function cleanup() {
    getDocs().forEach((doc, idx) => {
      SELECTORS.forEach(sel => doc.querySelectorAll(sel).forEach(el =>
        el.style.setProperty('display', 'none', 'important')));
      if (idx >= 1) hideFloatingBottomRight(doc);
    });
  }

  cleanup();
  setInterval(cleanup, 500);
})();
</script>
"""
components.html(js_remove_badges, height=0, width=0)

# ---------------------------------------------------------
# 4. Modals / Dialogs (อ้างอิงเนื้อหาจาก v1)
# ---------------------------------------------------------
@st.dialog("📘 คู่มือและการใช้งาน NotebookLM Prompt Builder")
def show_help_modal():
    st.markdown("""
    ### 🎯 วัตถุประสงค์
    เครื่องมือช่วยสร้าง **Master Prompt** เพื่อให้พนักงาน MinebeaMitsumi สามารถสร้างภาพ Infographic ผ่าน **NotebookLM** ได้อย่างรวดเร็ว สวยงาม และถูกต้องตามมาตรฐาน **Corporate Identity (CI)** ของบริษัท

    ---
    ### 🚀 ขั้นตอนการใช้งานง่ายๆ (3 Steps)
    1. **ตั้งค่าความต้องการ (Form Inputs):** พิมพ์หัวข้อเรื่องที่ต้องการสรุป เลือกสไตล์ภาพ (Standard / Custom) และปรับแต่งโลโก้ CI
    2. **คัดลอก Master Prompt:** กดปุ่ม **`⚡ คัดลอก Master Prompt`** ทางฝั่งขวา
    3. **นำไปสั่งงานใน NotebookLM:** เปิดโปรแกรม NotebookLM นำ Prompt ที่คัดลอกไป Paste ในช่องสั่งงานเพื่อรับภาพ Infographic ได้ทันที!
    """)

@st.dialog("💡 คำแนะนำการระบุหัวข้อ (Topic Input Guide)")
def show_topic_guide_modal():
    st.markdown("""
    ### 📝 รายละเอียดการระบุหัวข้อ / เนื้อหาหลัก

    * **กรณีพิมพ์ระบุหัวข้อ:**
      AI ใน NotebookLM จะดึงเฉพาะเนื้อหาที่เกี่ยวข้องกับหัวข้อนั้นๆ จากเอกสารมาสรุปและวาดเป็น Infographic เจาะจงเรื่องนั้นเป็นพิเศษ

    * **กรณีเว้นว่างไว้ (`[Insert Topic]`):**
      AI จะอ่านเอกสารทั้งหมดที่คุณอัปโหลดใน NotebookLM แล้วเลือกสรุปภาพรวมทั้งหมดของเนื้อหาให้โดยอัตโนมัติ
    """)

@st.dialog("🔍 ดูภาพตัวอย่างขนาดเต็ม", width="large")
def show_zoom(name, img_path):
    st.markdown(f"### {name}")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("ไม่พบไฟล์ภาพต้นฉบับ")

# ---------------------------------------------------------
# 5. Header Component (ดีไซน์ผสม v1 + v3)
# ---------------------------------------------------------
header_col1, header_col2 = st.columns([0.65, 0.35], vertical_alignment="center")

with header_col1:
    try:
        st.image("logo.png", width=380)
    except Exception:
        pass

with header_col2:
    btn_col1, btn_col2 = st.columns([0.5, 0.5])
    with btn_col1:
        if st.button("วิธีการใช้งาน", icon=":material/help:", use_container_width=True):
            show_help_modal()
    with btn_col2:
        st.markdown(
            """
            <div style="text-align: right;">
                <span style="background-color: #EBF3FE; color: #1E56A0; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 12px;">
                    🚀 Trial Version
                </span>
                <div style="font-size: 11px; color: #666666; margin-top: 3px; font-weight: 500;">
                    © Developed by Suttichai K.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Title & Corporate Accent Line
title_col1, title_col2 = st.columns([0.035, 0.965], gap="small", vertical_alignment="center")
with title_col1:
    try:
        st.image("title_icon.png", width=36)
    except Exception:
        pass
with title_col2:
    st.markdown("<h1 style='margin:0;'>NotebookLM Prompt Builder for Corporate Infographics</h1>", unsafe_allow_html=True)

st.caption("ระบบกำหนดค่าโครงสร้าง Master Prompt และการคุมธีม Corporate Identity (CI) สำหรับ NotebookLM")
st.markdown('<div class="brandline"><span></span><span></span></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. Dictionaries (คงโครงสร้างข้อมูล v1 ไว้ครบ 100%)
# ---------------------------------------------------------
CUSTOM_STYLES = {
    "Corporate Executive (เรียบหรู, มินิมอล, เน้นข้อมูล)": {
        "name_en": "Corporate Executive",
        "desc": "Clean layout, minimalist background, bold data typography, precise structured graphics.",
        "image": "style_1.png"
    },
    "Anime Cinematic (แสง Sunset, ดราม่าติก, แสงเงาจัด)": {
        "name_en": "Anime Cinematic",
        "desc": "Capture a specific moment with high emotion: relieved and proud expressions. Dramatic lighting contrast: golden hour sunset, spotlight vs darkness, glowing holographic details.",
        "image": "style_2.png"
    },
    "Chalkboard Educational (ชอล์กเขียนกระดานดำ, ลุคการเรียนรู้)": {
        "name_en": "Chalkboard Educational",
        "desc": "Chalkboard textures, hand-drawn vector diagrams, white and colored chalk lines, clean organized layouts.",
        "image": "style_3.png"
    },
    "Isometric 3D Tech (ภาพสามมิติ 3D, ลุคล้ำสมัย)": {
        "name_en": "Isometric 3D Tech",
        "desc": "3D isometric layout, smooth gradients, glowing data paths, modern technological UI aesthetic.",
        "image": "style_4.png"
    },
    "Flat Design 2.5D (ภาพเวกเตอร์แบบเรียบ, สีสันชัดเจน)": {
        "name_en": "Flat Design 2.5D",
        "desc": "Clean vector art, subtle depth shadows, bold color accents, modern business infographic style.",
        "image": "style_5.png"
    },
    "Futuristic HUD Dashboard (แดชบอร์ดไซเบอร์, ดาร์กโหมด)": {
        "name_en": "Futuristic HUD Dashboard",
        "desc": "Dark mode interface, cyan and neon blue grid displays, high-tech data visualization charts, sleek futuristic HUD elements.",
        "image": "style_6.png"
    },
    "Minimalist Sketch (งานวาดลายเส้นสเก็ตช์, มินิมอลเรียบง่าย)": {
        "name_en": "Minimalist Sketch",
        "desc": "Hand-drawn ink line art, clean white space, subtle watercolor accent highlights, clear typographic hierarchy.",
        "image": "style_7.png"
    }
}

STANDARD_STYLES = {
    "Kawaii (น่ารัก สไตล์การ์ตูนญี่ปุ่น)": {
        "name_en": "Kawaii",
        "desc": "Cute Japanese character illustrations, soft pastel color palette, friendly approach, playful graphics.",
        "image": "standard_1.png"
    },
    "Clay (งานปั้นดินน้ำมัน 3 มิติ)": {
        "name_en": "Clay",
        "desc": "Tactile claymation aesthetic, smooth 3D clay figures, soft shadow depth, playful corporate graphics.",
        "image": "standard_2.png"
    },
    "SketchNote (ลายเส้นสเก็ตช์เหมือนจดโน้ต)": {
        "name_en": "SketchNote",
        "desc": "Hand-drawn visual notes, sketchy line art icons, informal educational diagrams, storyboard layout.",
        "image": "standard_3.png"
    },
    "Anime (ลายเส้นอนิเมะ)": {
        "name_en": "Anime",
        "desc": "Japanese anime style illustrations, dynamic composition, vibrant visual storytelling.",
        "image": "standard_4.png"
    },
    "Editorial (รายงานบรรณาธิการ สื่อสารองค์กร)": {
        "name_en": "Editorial",
        "desc": "Editorial graphic design style, structured business report layout, clear information hierarchy, high-end publication aesthetics.",
        "image": "standard_5.png"
    },
    "Instructional (ขั้นตอนการทำงาน คู่มือ How-To)": {
        "name_en": "Instructional",
        "desc": "Step-by-step process flow, clear visual guides, modern iconography, structured instruction layout.",
        "image": "standard_6.png"
    },
    "BentoGrid (จัดบล็อกเป็นช่องๆ สไตล์โมเดิร์น)": {
        "name_en": "BentoGrid",
        "desc": "Modern UI bento box grid layout, clean card-based information structure, rounded corners, sleek data boxes.",
        "image": "standard_7.png"
    },
    "Bricks (ตัวต่อบล็อกสามมิติ)": {
        "name_en": "Bricks",
        "desc": "Voxel art, 3D brick building block aesthetics, structured modular graphics.",
        "image": "standard_8.png"
    },
    "Scientific (แผนภูมิวิชาการ ข้อมูลเชิงวิเคราะห์)": {
        "name_en": "Scientific",
        "desc": "Analytical charts, scientific data visualization, precise technical diagrams, clean academic presentation format.",
        "image": "standard_9.png"
    },
    "Professional (ลุคธุรกิจแบบเป็นทางการ)": {
        "name_en": "Professional",
        "desc": "Clean corporate presentation format, highly structured professional data visualization, formal executive layout.",
        "image": "standard_10.png"
    }
}

def preview_path(img):
    """ใช้ภาพย่อความละเอียดต่ำ (previews/*.jpg) เพื่อโหลดเร็ว
    ถ้าไม่มีไฟล์ภาพย่อ (เช่นยังไม่ได้อัปโหลด) จะถอยไปใช้ภาพต้นฉบับแทนอัตโนมัติ"""
    p = f"previews/{img.rsplit('.', 1)[0]}.jpg"
    return p if os.path.exists(p) else img


@st.cache_data(show_spinner=False)
def img_data_uri(path):
    """อ่านไฟล์ภาพแล้วแปลงเป็น base64 ครั้งเดียว แคชไว้ตาม path
    (เดิมสร้างฟังก์ชัน lambda ใหม่ + cache ใหม่ทุกรอบที่สคริปต์รัน ทำให้แคชไม่ช่วยอะไร)"""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    mime = "image/jpeg" if path.endswith(".jpg") else "image/png"
    return f"data:{mime};base64,{data}"

# ---------------------------------------------------------
# 7. Form Inputs & Main Layout
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader(":material/tune: 1. ตั้งค่าความต้องการ (Form Inputs)")

    # 1.1 Topic Input
    with st.container(border=True):
        lbl_col1, lbl_col2 = st.columns([0.72, 0.28], vertical_alignment="center")
        with lbl_col1:
            st.markdown("**📝 หัวข้อ / เนื้อหาหลักที่ต้องการสรุป:**")
        with lbl_col2:
            if st.button("คำแนะนำ", icon=":material/info:", key="btn_topic_info", use_container_width=True):
                show_topic_guide_modal()

        topic = st.text_area(
            label="topic_input",
            label_visibility="collapsed",
            height=90,
            placeholder="เช่น สรุปกลไกการทำลายหลอดเลือดออกเป็น 3 ระยะ หรือ สรุปผลการอบรม GWS Workshop"
        )

    # 1.2 Visual Style Category Selection
    with st.container(border=True):
        st.markdown("**🎨 Visual Style Category**")
        style_category = st.segmented_control(
            "ประเภทสไตล์",
            ["📊 Standard Presets (10 สไตล์)", "✨ Custom Corporate (7 สไตล์)"],
            default="📊 Standard Presets (10 สไตล์)",
            label_visibility="collapsed"
        ) or "📊 Standard Presets (10 สไตล์)"

        if "Standard" in style_category:
            selected_style_dict = STANDARD_STYLES
        else:
            selected_style_dict = CUSTOM_STYLES

        selected_style_label = st.selectbox(
            "เลือกสไตล์ภาพ (Visual Staging):",
            options=list(selected_style_dict.keys())
        )

    # 1.3 Corporate Identity (Branding)
    with st.container(border=True):
        st.markdown("**🛡️ Corporate Identity (Branding)**")
        use_logo = st.toggle("ใส่โลโก้บริษัท (Company Logo)", value=True)

        if use_logo:
            logo_pos_col, logo_size_col = st.columns(2)
            with logo_pos_col:
                st.caption("ตำแหน่งโลโก้")
                logo_pos = st.segmented_control(
                    "ตำแหน่ง",
                    ["ขวาบน", "ซ้ายบน", "ขวาล่าง"],
                    default="ขวาบน",
                    label_visibility="collapsed"
                ) or "ขวาบน"
            with logo_size_col:
                st.caption("ขนาดโลโก้")
                logo_size = st.segmented_control(
                    "ขนาด",
                    ["เล็ก", "กลาง", "ใหญ่"],
                    default="เล็ก",
                    label_visibility="collapsed"
                ) or "เล็ก"
        else:
            logo_pos, logo_size = "ขวาบน", "เล็ก"

        c1, c2 = st.columns(2)
        use_header_line = c1.checkbox("แถบเส้นสี Corporate (Red/Blue)", value=True)
        use_footer = c2.checkbox("Footer: MinebeaMitsumi Confidential", value=True)

# ---------------------------------------------------------
# 8. Master Prompt Generator Logic
# ---------------------------------------------------------
# ดึงข้อมูลสไตล์ที่เลือกอยู่ในปัจจุบันให้ถูกต้อง
current_style_dict = STANDARD_STYLES if "Standard" in style_category else CUSTOM_STYLES
style_info = current_style_dict[selected_style_label]

pos_map = {
    "ขวาบน": "**Top-Right Corner**",
    "ซ้ายบน": "**Top-Left Corner**",
    "ขวาล่าง": "**Bottom-Right Corner**"
}

size_map = {
    "เล็ก": "in a compact and non-intrusive size",
    "กลาง": "in a standard size",
    "ใหญ่": "in a large and prominent size"
}

topic_prompt = topic if topic.strip() else "[Insert Topic]"

# สร้าง Master Prompt
prompt_text = f"""You are an expert Visual Director, Screenwriter, and Graphic Designer.

Please generate a compelling, professional infographic based on the uploaded sources regarding: '{topic_prompt}'.

**Visual Staging ({style_info['name_en']}):**
{style_info['desc']}

**Corporate Branding Guidelines:**"""

if use_logo:
    prompt_text += f"""
- **Logo Placement & Design:** Place the official 'MinebeaMitsumi' corporate logo at the {pos_map[logo_pos]} {size_map[logo_size]}.
  - **Logo Structure (Two Lines):**
    1. **Top Line:** Bold, italicized deep-blue text reading **'MinebeaMitsumi'**.
    2. **Bottom Line (Tagline):** Smaller red and blue italicized text directly underneath reading **'Passion to Create Value through Difference'**."""

if use_header_line:
    prompt_text += "\n- **Header Line:** Include a thin horizontal **Red and Blue corporate accent line** right below the header."

if use_footer:
    prompt_text += "\n- **Footer:** Include subtle watermark text at the bottom center: `'MinebeaMitsumi Confidential'`."

prompt_text += "\n- **Color Application:** Apply primary corporate colors (Deep Blue, Accent Red) strictly to the branding elements, headers, and key callout highlights, while preserving the authentic artistic color scheme and atmospheric lighting of the selected Visual Staging."

# ---------------------------------------------------------
# 9. Preview & Copy Prompt Column (ฝั่งขวา)
# ---------------------------------------------------------
with col2:
    st.subheader(":material/content_copy: 2. Visual Preview & Master Prompt")

    # Track an actual successful clipboard write; the previous third-party
    # component did not return click events to Python.
    copy_key = f"copy_prompt_{abs(hash(prompt_text))}"
    copy_event = copy_button_component(
        text=prompt_text,
        before_copy_label="⚡ คัดลอก Master Prompt",
        after_copy_label="✅ คัดลอกเรียบร้อยแล้ว! นำไป Paste ใน NotebookLM ได้ทันที",
        key=copy_key,
        default=None,
    )

    if isinstance(copy_event, dict) and copy_event.get("copied"):
        event_id = copy_event.get("event_id")
        if event_id and event_id != st.session_state.get("_last_copy_event_id"):
            try:
                supabase.rpc(
                    "record_prompt_copy",
                    {
                        "p_google_sub": google_sub,
                        "p_client_event_id": event_id,
                    },
                ).execute()
                st.session_state["_last_copy_event_id"] = event_id
            except Exception:
                logger.exception("Could not record a prompt copy event")
                st.warning("คัดลอก Prompt แล้ว แต่บันทึกสถิติไม่สำเร็จ")

    st.markdown("---")

    # Header ส่วนภาพพรีวิว + ปุ่มขยายภาพ
    prev_title_col, zoom_btn_col = st.columns([0.7, 0.3], vertical_alignment="center")
    with prev_title_col:
        st.markdown(f"**👁️‍🗨️ ผลลัพธ์สไตล์: {style_info['name_en']}**")
    with zoom_btn_col:
        if st.button("ขยายภาพ", icon=":material/zoom_out_map:", key="btn_zoom", use_container_width=True):
            show_zoom(style_info["name_en"], style_info["image"])

    st.caption("📌 *หมายเหตุ: ภาพตัวอย่างอ้างอิงจากตำแหน่งโลโก้ขวาบน (Top-Right) และขนาด Compact เป็นหลัก*")

    # แสดงภาพในกรอบพรีวิวล็อกสัดส่วน (pv class) — ใช้ภาพย่อเพื่อความเร็ว
    try:
        uri = img_data_uri(preview_path(style_info["image"]))
        st.markdown(f'<div class="pv"><img src="{uri}" alt="{style_info["name_en"]}"></div>', unsafe_allow_html=True)
    except Exception:
        st.info("💡 ระบบกำลังดึงภาพตัวอย่างสไตล์นี้...")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.divider()
st.caption("Trial Version  |  © Developed by Suttichai K. for MinebeaMitsumi")
