import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang - Ẩn Sidebar
st.set_page_config(
    page_title="Phân Tích Ngữ Liệu AI",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Giao diện Xanh biển chuyên nghiệp
st.markdown("""
    <style>
    /* Ẩn Sidebar hoàn toàn */
    [data-testid="stSidebarNav"], [data-testid="collapsedControl"] {display: none;}
    
    /* Nền xanh nhạt thanh lịch */
    .stApp {
        background-color: #f0f4f8;
    }
    
    /* Tiêu đề chính xanh biển đậm */
    .main-title {
        color: #0d47a1;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 3rem;
        font-weight: 800;
        margin-top: -50px;
    }

    /* Tiêu đề mục h3 */
    h3 {
        color: #1565c0 !important;
        font-weight: bold !important;
        font-size: 1.6rem !important;
        border-bottom: 3px solid #bbdefb;
        padding-bottom: 10px;
    }
    
    /* Chữ nội dung */
    p, span, label {
        color: #1e3a5f !important;
        font-weight: 500 !important;
    }

    /* Ô nhập liệu */
    .stTextArea>div>div>textarea {
        border-radius: 12px !important;
        border: 2px solid #1976d2 !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        font-size: 1.1rem !important;
    }

    /* Nút bấm Xanh biển */
    .stButton>button {
        background: linear-gradient(90deg, #1976d2, #0d47a1) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.8rem !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.2);
    }
    
    /* Khung kết quả phân tích */
    .analysis-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        border-left: 10px solid #0d47a1;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Tiêu đề trang
st.markdown('<h1 class="main-title">📘 TRÌNH PHÂN TÍCH NGỮ LIỆU VĂN HỌC</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 40px;'>Gợi ý ý tưởng và dàn ý chi tiết từ văn bản của bạn</p>", unsafe_allow_html=True)

try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Lỗi: Chưa cấu hình GEMINI_API_KEY trong Secrets!")
    else:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Dùng Gemini 2.5 Flash như Khang mong muốn
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Bố cục 2 cột cân đối
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown("### 📖 INPUT NGỮ LIỆU 📚🖋️")
            context = st.text_area("", height=400, placeholder="Dán đoạn văn, bài thơ, hoặc ngữ liệu cần phân tích vào đây...", label_visibility="collapsed")
            
            if st.button("🚀 PHÂN TÍCH NGAY"):
                if context.strip():
                    with st.spinner('💎 AI đang thực hiện bóc tách ngữ liệu...'):
                        prompt = f"""
                        Bạn là một chuyên gia phê bình văn học. Hãy phân tích chuyên sâu ngữ liệu sau:
                        {context}

                        Nội dung phân tích cần có:
                        1. Chủ đề chính và nội dung bao quát.
                        2. Các biện pháp tu từ nổi bật (nêu rõ tác dụng).
                        3. Đặc sắc về ngôn từ, hình ảnh hoặc cấu trúc.
                        4. Gợi ý 3 hướng khai thác (đề bài) từ ngữ liệu này kèm dàn ý nhanh.
                        
                        Hãy trình bày bằng các gạch đầu dòng rõ ràng, sử dụng emoji phù hợp.
                        """
                        response = model.generate_content(prompt)
                        st.session_state.analysis_result = response.text
                        st.success("✅ Đã hoàn tất phân tích!")
                else:
                    st.warning("Khang ơi, hãy dán nội dung vào để AI có cái mà phân tích nhé! 📘")

        with col2:
            st.markdown("### KẾT QUẢ PHÂN TÍCH")
            if 'analysis_result' in st.session_state:
                st.markdown(f'<div class="analysis-card">{st.session_state.analysis_result}</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.info("Kết quả phân tích sẽ hiển thị tại đây sau khi bạn nhấn nút bên trái. ✨")

except Exception as e:
    st.error(f"Sự cố hệ thống: {e}")
