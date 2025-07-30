from pathlib import Path
import os
import streamlit as st
import pandas as pd
from datetime import datetime

# --------------------------------------------
# 1) حدد BASE_DIR → يصل إلى مجلّد employee_system/
# --------------------------------------------
BASE_DIR     = Path(__file__).resolve().parent.parent.parent
REPORTS_XLS  = BASE_DIR / "reports_data.xlsx"
REPATT_DIR   = BASE_DIR / "reports_attachments"

# 2) تأكد من وجود مجلّد مرفقات البلاغات المشترك
REPATT_DIR.mkdir(parents=True, exist_ok=True)

# إعداد الصفحة
st.set_page_config(page_title="إرسال بلاغ IT", layout="centered")
st.markdown(
    "<h1 style='text-align:center; color:#006db3;'>نموذج إرسال بلاغ لقسم تقنية المعلومات</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# قائمة المستشفيات
hospitals = [
    "مستشفى السلام",
    "مستشفى الحرم",
    "مركز باب جبريل",
    "مركز الصافية"
]

# مدخلات النموذج
hospital   = st.selectbox("اختر المستشفى", options=hospitals)
department = st.text_input("اسم القسم")
issue_desc = st.text_area("تفاصيل البلاغ")
attachment = st.file_uploader("إرفاق ملف (اختياري)", type=["png", "jpg", "pdf", "docx", "xlsx"])

# عند النقر على زر الإرسال
if st.button("إرسال البلاغ"):
    if not department or not issue_desc:
        st.error("يرجى ملء جميع الحقول المطلوبة قبل الإرسال.")
    else:
        # حفظ المرفق في المجلد المشترك
        filename = ""
        if attachment is not None:
            ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{ts}_{attachment.name}"
            path     = REPATT_DIR / filename
            with open(path, "wb") as f:
                f.write(attachment.getbuffer())

        # قراءة أو إنشاء DataFrame
        if REPORTS_XLS.exists():
            df = pd.read_excel(REPORTS_XLS)
        else:
            df = pd.DataFrame(
                columns=["timestamp", "hospital", "department", "description", "attachment"]
            )

        # إضافة السجل الجديد
        new_report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hospital": hospital,
            "department": department,
            "description": issue_desc,
            "attachment": filename
        }
        df = pd.concat([df, pd.DataFrame([new_report])], ignore_index=True)
        df.to_excel(REPORTS_XLS, index=False)

        st.success("✅ تم إرسال البلاغ بنجاح.")
