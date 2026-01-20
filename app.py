import streamlit as st
from datetime import datetime
from PIL import Image

# --- 页面配置 ---
st.set_page_config(page_title="小千的刷脂日记", page_icon="🥑", layout="mobile")

# --- 标题区 ---
st.title("🥑 小千的刷脂日记")
st.caption(f"📅 今天是：{datetime.now().strftime('%Y-%m-%d %A')}")
st.write("严谨专家提醒：不知道克数就拍图，或者用'拳头'做单位！")

# --- 初始化 Session State (防止刷新丢失数据) ---
if 'log_data' not in st.session_state:
    st.session_state.log_data = {
        "早餐": {"text": "", "img": None},
        "午餐": {"text": "", "img": None},
        "晚餐": {"text": "", "img": None},
        "加餐/运动": {"text": "", "img": None},
        "体重": 0.0,
    }

# --- 输入区域 ---
with st.container():
    st.header("⚖️ 晨间数据")
    weight = st.number_input("今早空腹体重 (kg)", min_value=0.0, step=0.05, format="%.2f")
    st.session_state.log_data["体重"] = weight

    # 定义一个通用的输入函数
    def meal_input(meal_name, emoji):
        with st.expander(f"{emoji} {meal_name}", expanded=False):
            desc = st.text_area(f"{meal_name}吃了啥？(不知道克数就描述大小)", 
                               placeholder="例：去皮鸡腿饭，饭吃了一半，没喝汤...")
            uploaded_file = st.file_uploader(f"上传{meal_name}截图/照片", type=['png', 'jpg', 'jpeg'], key=meal_name)
            
            # 实时保存到状态
            st.session_state.log_data[meal_name]["text"] = desc
            if uploaded_file is not None:
                st.session_state.log_data[meal_name]["img"] = "已上传图片" # 简化处理，这里标记已上传

    meal_input("早餐", "☕️")
    meal_input("午餐", "🍗")
    meal_input("晚餐", "🥗")
    meal_input("加餐/运动", "🥊")

# --- 一键打包区 ---
st.markdown("---")
if st.button("📦 一键打包发给 AI", type="primary"):
    # 生成格式化文本
    report = f"""
=== 📅 {datetime.now().strftime('%Y-%m-%d')} 饮食运动日报 ===
【晨重】：{st.session_state.log_data['体重']} kg

【☕️ 早餐】
{st.session_state.log_data['早餐']['text'] or "（没吃/只喝了咖啡）"}
[图片状态]：{st.session_state.log_data['早餐']['img'] or "无"}

【🍗 午餐】
{st.session_state.log_data['午餐']['text'] or "（未记录）"}
[图片状态]：{st.session_state.log_data['午餐']['img'] or "无"}

【🥗 晚餐】
{st.session_state.log_data['晚餐']['text'] or "（未记录）"}
[图片状态]：{st.session_state.log_data['晚餐']['img'] or "无"}

【🥊 加餐/运动】
{st.session_state.log_data['加餐/运动']['text'] or "（没练/没加餐）"}

---------------------------
👨‍🏫 教练请分析！(截图我会单独发在聊天框里)
    """
    
    st.success("打包成功！请点击下方按钮复制，然后把截图一起发给我！")
    st.code(report, language="text")
    st.balloons()