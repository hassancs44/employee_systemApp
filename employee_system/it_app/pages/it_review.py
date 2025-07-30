from pathlib import Path
import os
import streamlit as st
import pandas as pd

# --------------------------------------------
# 1) حدد BASE_DIR → يصل إلى مجلّد employee_system/
# --------------------------------------------
BASE_DIR      = Path(__file__).resolve().parent.parent.parent
REQUESTS_XLS  = BASE_DIR / "employee_requests.xlsx"
ATTACH_DIR    = BASE_DIR / "attachments"

# --------------------------------------------
# 2) تأكد من وجود مجلّد المرفقات المشترك
# --------------------------------------------
ATTACH_DIR.mkdir(parents=True, exist_ok=True)

# إعداد صفحة عرض طلبات الموظفين
st.set_page_config(page_title="قسم IT", layout="wide")
st.markdown("<h2 style='color:#006db3;'>قسم تقنية المعلومات - الطلبات الواردة</h2>", unsafe_allow_html=True)
st.markdown("---")

# قراءة البيانات من Excel المشترك
if not REQUESTS_XLS.exists():
    st.warning("📂 لا توجد بيانات حتى الآن.")
else:
    df = pd.read_excel(REQUESTS_XLS)
    if df.empty:
        st.info("لا توجد طلبات حالياً.")
    else:
        for idx, row in df.iterrows():
            with st.expander(f"🔹 {row['الاسم']} - {row['رقم الهوية']}"):
                st.write(f"**الجنسية:** {row['الجنسية']}")
                st.write(f"**تاريخ الإرسال:** {row['تاريخ الإرسال']}")
                st.write(f"**الحالة:** {row['الحالة']}")

                # زر تحميل المرفق من المجلد المشترك
                attachment_name = row.get('اسم الملف', '')
                if pd.notnull(attachment_name) and attachment_name:
                    file_path = ATTACH_DIR / attachment_name
                    if file_path.exists():
                        with open(file_path, 'rb') as f:
                            st.download_button(
                                label="📥 تحميل النموذج المرفق",
                                data=f,
                                file_name=attachment_name,
                                mime="application/octet-stream"
                            )
                    else:
                        st.error("❌ المرفق غير موجود.")
