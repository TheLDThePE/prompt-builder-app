import streamlit as st

# 1. Page Config ต้องอยู่บรรทัดแรกสุด
st.set_page_config(page_title="NotebookLM Prompt Builder", page_icon="🎨", layout="wide")

# แสดงรูปภาพโลโก้บริษัทบนหน้าเว็บ (ถ้ามีไฟล์ logo.png ในโฟลเดอร์)
try:
    st.image("logo.png", width=250)
except Exception:
    pass

# Title & Caption
st.title("🎨 NotebookLM Prompt Builder for Corporate Infographics")
st.caption("แปลงโจทย์งานของคุณให้กลายเป็น Master Prompt สไตล์ต่างๆ พร้อม CI Branding เป๊ะๆ")

# Layout Split: 2 Columns
col_form, col_output = st.columns([1, 1], gap="large")

# ==========================================
# ฝั่งซ้าย: FORM CONTROLS (Dropdown & Inputs)
# ==========================================
with col_form:
    st.header("1. ตั้งค่าความต้องการ (Form Inputs)")

    # 1.1 Content Topic พร้อม Tooltip คำอธิบาย
    topic = st.text_area(
        "📌 หัวข้อ / เนื้อหาหลักที่ต้องการสรุป:",
        placeholder="เช่น สรุปกลไกการทำลายหลอดเลือดออกเป็น 3 ระยะ หรือ สรุปผลการอบรม GWS Workshop",
        height=100,
        help=(
            "💡 **คำแนะนำในการกรอกช่องนี้:**\n\n"
            "ช่องนี้ทำหน้าที่เป็น **Focus Area** สำหรับตีกรอบให้ AI รู้ว่าต้องเน้นประเด็นไหนจากไฟล์ใน NotebookLM\n\n"
            "- **เน้นจุดสำคัญ:** เช่น *'เน้นเฉพาะระยะอักเสบเรื้อรัง'*[cite: 17]\n"
            "- **เน้นโครงสร้าง:** เช่น *'จัดกลุ่มสรุปออกเป็น 3 ระยะ'*[cite: 17]\n"
            "- **หากปล่อยว่างไว้:** AI จะสรุปภาพรวมทั้งหมดของเอกสารให้โดยอัตโนมัติ"
        )
    )

    # 1.2 Visual Style & Emotion
    st.subheader("🎬 Visual Style & Emotion")
    visual_style = st.selectbox(
        "เลือกสไตล์ภาพ (Visual Staging):",
        [
            "Anime Cinematic (แสง Sunset, ดรามาติก, แสงเงาจัด)",
            "Corporate Executive (เรียบหรู, มินิมอล, เน้นข้อมูล)",
            "Cyberpunk Tech (นีออน, ดิจิทัล, ล้ำสมัย)",
            "3D Isomorphic Vector (สไตล์สามมิติ มินิมอล คล้ายโมเดลจำลอง)",
            "Flat Infographic Modern (เน้นเวกเตอร์สีสดใส อ่านง่ายแบบนิตยสาร)",
            "Hand-Drawn Chalkboard (สไตล์วาดกระดานดำ อารมณ์การสอน/สัมมนา)",
            "Vintage Scientific Blueprint (สไตล์พิมพ์เขียวเทคนิค สีน้ำเงิน-ขาว)"
        ]
    )

    # 1.3 Corporate Identity (CI) Settings
    st.subheader("🏢 Corporate Identity (Branding)")

    enable_logo = st.checkbox("ใส่โลโก้บริษัท (Company Logo)", value=True)

    if enable_logo:
        logo_pos = st.radio(
            "ตำแหน่งโลโก้ (Logo Position):",
            ["Top-Right Corner (ขวาบน) [Standard]", "Top-Left Corner (ซ้ายบน)", "Bottom-Right Corner (ขวาล่าง)"],
            horizontal=True
        )
        logo_size = st.select_slider(
            "ขนาดโลโก้ (Logo Size):",
            options=["Compact (เล็กกำลังดี)", "Medium (มาตรฐาน)", "Large (เด่นชัด)"]
        )

    add_accent_line = st.checkbox("ใส่แถบเส้นสี Corporate (Red/Blue Accent Line Below Header)", value=True)
    add_footer = st.checkbox("ใส่ Footer Text ('MinebeaMitsumi Confidential')", value=True)

# ==========================================
# ฝั่งขวา: PROMPT GENERATOR ENGINE & OUTPUT
# ==========================================
with col_output:
    st.header("2. Master Prompt (นำไป Paste ใน NotebookLM)")

    # 1. Persona & Role
    role_prompt = "You are an expert Visual Director, Screenwriter, and Graphic Designer.\n\n"

    # 2. Main Instruction
    task_prompt = f"Please generate a compelling, professional infographic based on the uploaded sources regarding: '{topic if topic else '[Insert Topic]'}'.\n\n"

    # 3. Visual Staging (Conditional)
    if "Anime" in visual_style:
        style_prompt = (
            "**Visual Staging (Anime Cinematic):**\n"
            "- Capture a specific moment with high emotion: relieved and proud expressions.\n"
            "- Dramatic lighting contrast: golden hour sunset, spotlight vs darkness, glowing holographic details.\n\n"
        )
    elif "Corporate" in visual_style:
        style_prompt = (
            "**Visual Staging (Corporate Executive):**\n"
            "- Clean layout, minimalist background, bold data typography, precise structured graphics.\n\n"
        )
    elif "Cyberpunk" in visual_style:
        style_prompt = (
            "**Visual Staging (Cyberpunk Tech):**\n"
            "- Futuristic UI elements, glowing neon accents, dark tech background.\n\n"
        )
    elif "3D" in visual_style:
        style_prompt = (
            "**Visual Staging (3D Isomorphic Vector):**\n"
            "- Clean 3D isometric perspective, smooth lighting, modern clay/toy-like minimal model style.\n\n"
        )
    elif "Flat" in visual_style:
        style_prompt = (
            "**Visual Staging (Vibrant Modern Infographic):**\n"
            "- Bold colorful vector graphics, vibrant modern pop color palette with rich contrast.\n"
            "- Floating glassmorphism cards with soft glowing drop-shadows.\n"
            "- Dynamic isometric 3D/2.5D visual accents and eye-catching graphic elements.\n\n"
        )
    elif "Chalkboard" in visual_style:
        style_prompt = (
            "**Visual Staging (Hand-Drawn Chalkboard):**\n"
            "- Dark chalkboard texture background, detailed hand-drawn chalk illustrations, educational presentation feel.\n\n"
        )
    elif "Blueprint" in visual_style:
        style_prompt = (
            "**Visual Staging (Vintage Scientific Blueprint):**\n"
            "- Deep blue grid blueprint paper texture, precise white technical drawing lines, schematic diagram aesthetic.\n\n"
        )
    else:
        style_prompt = f"**Visual Staging:** {visual_style}\n\n"

    # 4. Branding Rules (CI)
    ci_prompt = "**Corporate Branding Guidelines:**\n"

    if enable_logo:
        # ตรวจสอบตำแหน่งโลโก้
        if "Top-Left" in logo_pos:
            pos_text = "Top-Left Corner"
        elif "Bottom-Right" in logo_pos:
            pos_text = "Bottom-Right Corner"
        else:
            pos_text = "Top-Right Corner"

        # ตรวจสอบขนาดโลโก้
        size_text = "compact and non-intrusive" if "Compact" in logo_size else ("large and prominent" if "Large" in logo_size else "standard")

        # ระบุรายละเอียดโลโก้ 2 บรรทัด (เอาอักขระ [cite] ออกเรียบร้อยแล้ว)
        ci_prompt += (
            f"- **Logo Placement & Design:** Place the official 'MinebeaMitsumi' corporate logo at the **{pos_text}** in a {size_text} size.\n"
            f"  - **Logo Structure (Two Lines):**\n"
            f"    1. **Top Line:** Bold, italicized deep-blue text reading **'MinebeaMitsumi'**.\n"
            f"    2. **Bottom Line (Tagline):** Smaller red and blue italicized text directly underneath reading **'Passion to Create Value through Difference'**.\n"
        )

    if add_accent_line:
        ci_prompt += "- **Header Line:** Include a thin horizontal **Red and Blue corporate accent line** right below the header.\n"

    if add_footer:
        ci_prompt += "- **Footer:** Include subtle watermark text at the bottom center: `'MinebeaMitsumi Confidential'`.\n"

    ci_prompt += "- **Color Palette:** Primary corporate colors (Deep Blue, Accent Red, White Background).\n"

    # Combine All Parts into Master Prompt
    final_master_prompt = role_prompt + task_prompt + style_prompt + ci_prompt

    # Display Master Prompt in Code Block
    st.code(final_master_prompt, language="markdown")

    st.success("💡 **วิธีใช้งาน:** คัดลอก Prompt ด้านบนนี้ ไปเปิดหน้า NotebookLM แล้ววาง (Paste) ลงในช่องสร้าง Infographic , Slide Deck  ได้ทันที!")
