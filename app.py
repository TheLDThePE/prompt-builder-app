import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard

# 1. ตั้งค่าหน้าตาของ Streamlit App และใส่ favicon.png
st.set_page_config(
    page_title="NotebookLM Prompt Builder",
    page_icon="favicon.png",
    layout="wide"
)

# 2. Custom CSS: ซ่อน UI เดิม และซ่อน Viewer Badges/Icons มุมขวาล่างอย่างเด็ดขาด
hide_and_custom_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}

    /* ซ่อน Streamlit Community Watermark / Crown & Mascot Badges ขวาล่าง */
    [data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}

    /* สั่งซ่อน Element ทุกตัวที่อยู่ลอยขวาล่างยกเว้น Developer Credit */
    div[class*="viewerBadge"],
    div[class*="styles_viewerBadge"],
    a[class*="viewerBadge"],
    .stApp > iframe,
    iframe[title="streamlit_app"] {
        display: none !important;
    }

    /* ครอบซ่อน Container ลอยล่างขวาของระบบ Streamlit */
    div[data-testid="stActionButtonIcon"] {display: none !important;}
    div[style*="position: fixed"][style*="bottom"] {
        display: none !important;
    }

    /* ดึงเฉพาะ Developer Credit ของเราให้แสดงผลลอยขวาล่างตามปกติ */
    .developer-credit {
        position: fixed !important;
        bottom: 12px !important;
        right: 20px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #555555 !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 5px 14px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
        z-index: 999999 !important;
        display: block !important;
    }

    /* ลดระยะเว้นขอบบนของหน้าเว็บให้กระชับขึ้น */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }
    </style>
"""
st.markdown(hide_and_custom_style, unsafe_allow_html=True)

# ---------------------------------------------------------
# 💡 ฟังก์ชันระบบ Pop-up (Modal Dialogs)
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

# ---------------------------------------------------------
# 3. ส่วน Header แสดงโลโก้บริษัท, ปุ่ม Help (?) และ Credit
# ---------------------------------------------------------
header_col1, header_col2 = st.columns([0.60, 0.40])

with header_col1:
    try:
        st.image("logo.png", width=420)
    except Exception:
        pass

with header_col2:
    btn_col1, btn_col2 = st.columns([0.5, 0.5])
    with btn_col1:
        # ปุ่ม Help เปิด Modal
        if st.button("❓ วิธีการใช้งาน (Help)", use_container_width=True):
            show_help_modal()
    with btn_col2:
        st.markdown(
            """
            <div style="text-align: right; padding-top: 2px;">
                <span style="background-color: #EBF3FE; color: #1E56A0; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 13px;">
                    🚀 Trial Version
                </span>
                <div style="font-size: 12px; color: #666666; margin-top: 4px; font-weight: 500;">
                    © Developed by Suttichai K.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ส่วนแสดง Title พร้อมไอคอน
title_col1, title_col2 = st.columns([0.03, 0.97], gap="small")
with title_col1:
    try:
        st.image("title_icon.png", width=38)
    except Exception:
        pass
with title_col2:
    st.markdown("<h1 style='padding-top: 0px; margin-top: -8px; font-size: 1.95rem;'>NotebookLM Prompt Builder for Corporate Infographics</h1>", unsafe_allow_html=True)

st.caption("ระบบกำหนดค่าโครงสร้าง Master Prompt และการคุมธีม Corporate Identity (CI) สำหรับ NotebookLM")

# ---------------------------------------------------------
# 4. Dictionary เก็บข้อมูลสไตล์
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

# ---------------------------------------------------------
# 5. UI Layout & Form Inputs
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🎛️ 1. ตั้งค่าความต้องการ (Form Inputs)")

    # หัวข้อ Input + ปุ่ม ไอคอน (i)
    lbl_col1, lbl_col2 = st.columns([0.85, 0.15])
    with lbl_col1:
        st.markdown("**📝 หัวข้อ / เนื้อหาหลักที่ต้องการสรุป:**")
    with lbl_col2:
        if st.button("ℹ️ คำแนะนำ", key="btn_topic_info"):
            show_topic_guide_modal()

    topic = st.text_area(
        label="topic_input",
        label_visibility="collapsed",
        placeholder="เช่น สรุปกลไกการทำลายหลอดเลือดออกเป็น 3 ระยะ หรือ สรุปผลการอบรม GWS Workshop"
    )

    st.markdown("### 🎨 Visual Style Category")

    style_category = st.radio(
        "เลือกประเภทของสไตล์ภาพ:",
        ["📊 Standard NotebookLM Presets (10 สไตล์มาตรฐาน)", "✨ Custom Corporate Styles (7 สไตล์เฉพาะองค์กร)"],
        horizontal=False
    )

    if "Standard NotebookLM" in style_category:
        selected_style_dict = STANDARD_STYLES
    else:
        selected_style_dict = CUSTOM_STYLES

    selected_style_label = st.selectbox(
        "เลือกสไตล์ภาพ (Visual Staging):",
        options=list(selected_style_dict.keys())
    )

    st.markdown("### 🛡️ Corporate Identity (Branding)")
    use_logo = st.checkbox("ใส่โลโก้บริษัท (Company Logo)", value=True)

    logo_pos = st.radio(
        "ตำแหน่งโลโก้ (Logo Position):",
        ["Top-Right Corner (ขวาบน) [Standard]", "Top-Left Corner (ซ้ายบน)", "Bottom-Right Corner (ขวาล่าง)"],
        horizontal=True
    )

    logo_size = st.select_slider(
        "ขนาดโลโก้ (Logo Size):",
        options=["Compact (เล็กกำลังดี)", "Medium (มาตรฐาน)", "Large (เด่นชัด)"],
        value="Compact (เล็กกำลังดี)"
    )

    use_header_line = st.checkbox("ใส่แถบเส้นสี Corporate (Red/Blue Accent Line Below Header)", value=True)
    use_footer = st.checkbox("ใส่ Footer Text ('MinebeaMitsumi Confidential')", value=True)

# ---------------------------------------------------------
# 6. ประมวลผล Master Prompt Text
# ---------------------------------------------------------
style_info = selected_style_dict[selected_style_label]

if "Top-Right" in logo_pos:
    pos_text = "**Top-Right Corner**"
elif "Top-Left" in logo_pos:
    pos_text = "**Top-Left Corner**"
else:
    pos_text = "**Bottom-Right Corner**"

if "Compact" in logo_size:
    size_text = "in a compact and non-intrusive size"
elif "Medium" in logo_size:
    size_text = "in a standard size"
else:
    size_text = "in a large and prominent size"

topic_prompt = topic if topic.strip() else "[Insert Topic]"

prompt_text = f"""You are an expert Visual Director, Screenwriter, and Graphic Designer.

Please generate a compelling, professional infographic based on the uploaded sources regarding: '{topic_prompt}'.

**Visual Staging ({style_info['name_en']}):**
- {style_info['desc']}

**Corporate Branding Guidelines:**"""

if use_logo:
    prompt_text += f"""
- **Logo Placement & Design:** Place the official 'MinebeaMitsumi' corporate logo at the {pos_text} {size_text}.
  - **Logo Structure (Two Lines):**
    1. **Top Line:** Bold, italicized deep-blue text reading **'MinebeaMitsumi'**.
    2. **Bottom Line (Tagline):** Smaller red and blue italicized text directly underneath reading **'Passion to Create Value through Difference'**."""

if use_header_line:
    prompt_text += "\n- **Header Line:** Include a thin horizontal **Red and Blue corporate accent line** right below the header."

if use_footer:
    prompt_text += "\n- **Footer:** Include subtle watermark text at the bottom center: `'MinebeaMitsumi Confidential'`."

prompt_text += "\n- **Color Application:** Apply primary corporate colors (Deep Blue, Accent Red) strictly to the branding elements, headers, and key callout highlights, while preserving the authentic artistic color scheme and atmospheric lighting of the selected Visual Staging."

# ---------------------------------------------------------
# 7. ฝั่งขวา: Preview & Copy Prompt
# ---------------------------------------------------------
with col2:
    st.subheader("🖥️ 2. Visual Preview & Master Prompt")

    st.markdown(f"**👁️‍🗨️ ตัวอย่างผลลัพธ์สไตล์: {style_info['name_en']}**")
    st.caption("📌 *หมายเหตุ: ภาพตัวอย่างอ้างอิงจากตำแหน่งโลโก้ขวาบน (Top-Right) และขนาด Compact เป็นหลัก*")

    try:
        st.image(style_info["image"], use_container_width=True)
    except Exception:
        st.info("💡 ระบบกำลังดึงภาพตัวอย่างสไตล์นี้...")

    st.markdown("---")

    st.markdown("#### ⚡ คัดลอก Master Prompt ไปใช้งาน")

    st_copy_to_clipboard(
        prompt_text,
        before_copy_label="⚡ คัดลอก Master Prompt",
        after_copy_label="✅ คัดลอกเรียบร้อยแล้ว! นำไป Paste ใน NotebookLM ได้ทันที"
    )
