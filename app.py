import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang - Ẩn Sidebar để giao diện tập trung vào khung trắng
st.set_page_config(
    page_title="Chiến Lược Văn Học AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Tối giản, thanh lịch, chữ cực kỳ rõ nét
st.markdown("""
    <style>
    /* Ẩn hoàn toàn Sidebar */
    [data-testid="stSidebarNav"], [data-testid="collapsedControl"] {display: none;}
    
    .stApp { background-color: #fffafb; }
    
    /* Tiêu đề chính màu mận chín đậm */
    .main-title {
        color: #880e4f;
        text-align: center;
        font-family: 'Lexend', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        margin-top: -40px;
        margin-bottom: 10px;
    }

    /* Tiêu đề các mục */
    h3 {
        color: #4a001f !important;
        font-weight: bold !important;
        font-size: 1.6rem !important;
        border-bottom: 2px solid #f8bbd0;
        padding-bottom: 10px;
    }
    
    /* Chữ nội dung */
    p, span, label {
        color: #2d2d2d !important;
        font-weight: 500 !important;
    }

    /* Input & Textarea */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 12px !important;
        border: 2px solid #ad1457 !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Nút bấm Chiến Thuật */
    .stButton>button {
        background: linear-gradient(90deg, #d81b60, #ad1457) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.8rem !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0 4px 12px rgba(173, 20, 87, 0.2);
    }
    
    /* Khung phương án làm bài */
    .strategy-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        border-top: 10px solid #880e4f;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        line-height: 1.7;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Nội dung trang chính
st.markdown('<h1 class="main-title">🎓 CHIẾN LƯỢC LÀM BÀI VĂN AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-bottom: 40px;'>Phân tích loại đề và đưa ra phương án triển khai tối ưu nhất</p>", unsafe_allow_html=True)

try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Lỗi: Hãy thêm GEMINI_API_KEY vào mục Secrets.")
    else:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Bố cục 2 cột
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown("### 📋 Phân tích Đề bài")
            topic = st.text_input("Nhập đề bài:", placeholder="Ví dụ: So sánh nhân vật Tràng và Chí Phèo...", label_visibility="collapsed")
            
            st.markdown("### 📚 Ngữ liệu đi kèm (nếu có)")
            context = st.text_area("Nhập đoạn trích:", height=300, placeholder="Dán đoạn thơ/văn cần phân tích tại đây...", label_visibility="collapsed")

        with col2:
            st.markdown("### ⚡ Phương án hành động")
            st.write("AI sẽ xác định dạng đề và hướng dẫn bạn cách tiếp cận sáng tạo nhất.")
            
            if st.button("🔍 Phân Tích Chiến Lược"):
                if topic:
                    with st.spinner('🎯 Đang xác định dạng đề và xây dựng chiến lược...'):
                        prompt = f"""
                        Bạn là một chuyên gia luyện thi học sinh giỏi Ngữ văn.
                        Đề bài: {topic}
                        Ngữ liệu: {context}

                        Nhiệm vụ của bạn:
                        1. Xác định chính xác Dạng đề (Nghị luận văn học, Nghị luận xã hội, So sánh, Liên tưởng, v.v.).
                        2. Đưa ra Phương án làm bài tốt nhất (Nên đi theo hướng nào để đạt điểm cao, tránh rập khuôn).
                        3. Các từ khóa chuyên môn (Key concepts) nên sử dụng để bài viết sâu sắc.
                        4. Cấu trúc triển khai sáng tạo (Gợi ý cách đặt vấn đề và liên hệ mở rộng đặc sắc).
                        
                        Yêu cầu: Trình bày súc tích, chuyên nghiệp, có sử dụng emoji.
                        """
                        response = model.generate_content(prompt)
                        st.success("✅ Đã hoàn tất phương án!")
                        st.markdown(f'<div class="strategy-card">{response.text}</div>', unsafe_allow_html=True)
                        st.balloons()
                else:
                    st.warning("Khang ơi, bạn cần nhập ít nhất là tên Đề bài nhé! 🌸")

except Exception as e:
    st.error(f"Sự cố hệ thống: {e}")
