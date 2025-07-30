from pathlib import Path
import os
import streamlit as st
import pandas as pd
from datetime import datetime

# --------------------------------------------
# 1) حدد BASE_DIR → يصل إلى مجلّد employee_system/
# --------------------------------------------
BASE_DIR     = Path(__file__).resolve().parent.parent.parent
REQUESTS_XLS = BASE_DIR / "employee_requests.xlsx"
ATTACH_DIR   = BASE_DIR / "attachments"

# 2) تأكد من وجود مجلّد المرفقات المشترك
ATTACH_DIR.mkdir(parents=True, exist_ok=True)

# إعداد الصفحة
st.set_page_config(page_title="نموذج موظف جديد", layout="centered")
st.markdown("<h2 style='color:#006db3;'>نموذج تسجيل موظف جديد</h2>", unsafe_allow_html=True)
st.markdown("---")

# إنشاء ملف Excel إذا لم يكن موجودًا
if not REQUESTS_XLS.exists():
    pd.DataFrame(
        columns=["الاسم", "رقم الهوية", "الجنسية", "تاريخ الإرسال", "اسم الملف", "الحالة"]
    ).to_excel(REQUESTS_XLS, index=False)

# نموذج الإدخال
with st.form("employee_form"):
    name         = st.text_input("الاسم")
    id_number    = st.text_input("رقم الهوية")
    nationality  = st.text_input("الجنسية")
    uploaded_file= st.file_uploader("أرفق النموذج الورقي (PDF أو صورة)", type=["pdf", "png", "jpg", "jpeg"])

    submitted = st.form_submit_button("إرسال")

    if submitted:
        if not (name and id_number and nationality and uploaded_file):
            st.error("🛑 يرجى تعبئة جميع الحقول وإرفاق النموذج.")
        else:
            # حفظ الملف في المجلد المشترك
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename  = f"{id_number}_{timestamp}_{uploaded_file.name}"
            target    = ATTACH_DIR / filename
            with open(target, "wb") as f:
                f.write(uploaded_file.read())

            # إضافة السجل إلى ملف Excel المشترك
            df = pd.read_excel(REQUESTS_XLS)
            new_row = {
                "الاسم": name,
                "رقم الهوية": id_number,
                "الجنسية": nationality,
                "تاريخ الإرسال": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "اسم الملف": filename,
                "الحالة": "بانتظار المعالجة من IT"
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(REQUESTS_XLS, index=False)

            st.success("✅ تم إرسال البيانات بنجاح.")
