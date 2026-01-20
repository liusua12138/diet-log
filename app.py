import streamlit as st
from datetime import datetime
# 如果报错 no module named 'PIL'，请在 requirements.txt 里加上: Pillow
from PIL import Image

# --- 1. 页面配置 (这里改好了！) ---
# layout="centered" 是手机浏览的最佳模式
st.set_page_config(page_title="小千的刷脂日记", page_icon="🥑", layout="centered")

# --- 2. 标题区 ---
st.title("🥑 小千的刷脂日记")
st.caption(f"📅 今天是：{datetime.now().strftime('%Y-%m-%d %A')}")
st.info("💡 严谨专家提醒：不知道克数就拍图，或者用'拳头'做单位！")

# --- 3. 初始化 Session State (防止刷新丢失数据) ---
if 'log_data' not in st.session_state:
    st.session_state.log_data = {
        "早餐": {"text": "", "uploaded": False},
        "午餐": {"text": "", "uploaded": False},
        "晚餐": {"text": "", "uploaded": False},
        "加餐/运动": {"text": "", "uploaded": False},
        "体重": 0.0,
    }

# --- 4. 输入区域 ---
with st.container():
    st.header("⚖️ 晨间数据")
    weight = st.number_input("今早空腹体重 (kg)", min_value=0.0, step=0.05, format="%.2f")
    # 更新体重数据
    st.session_state.log_data["体重"] = weight

    # 定义一个通用的输入函数
    def meal_input(meal_name, emoji):
        with st.expander(f"{emoji} {meal_name}", expanded=False):
            # 文本输入
            desc = st.text_area(
                f"{meal_name}吃了啥？", 
                placeholder="例：去皮鸡腿饭，饭吃了一半...",
                key=f"text_{meal_name}" # 唯一的key防止冲突
            )
            
            # 图片上传
            uploaded_file = st.file_uploader(f"上传{meal_name}截图", type=['png', 'jpg', 'jpeg'], key=f"file_{meal_name}")
            
            # 实时保存到状态（只要有输入或者有文件，就更新）
            if desc:
                st.session_state.log_data[meal_name]["text"] = desc
            if uploaded_file is not None:
                st.session_state.log_data[meal_name]["uploaded"] = True

    meal_input("早餐", "☕️")
    meal_input("午餐", "🍗")
    meal_input("晚餐", "🥗")
    meal_input("加餐/运动", "🥊")

# --- 5. 一键打包区 ---
st.markdown("---")
if st.button("📦 一键打包发给 AI", type="primary"):
    # 获取图片状态文字
    def get_img_status(key):
        return "✅ 已存图" if st.session_state.log_data[key]["uploaded"] else "❌ 无图"

    # 生成格式化文本
    report = f"""
=== 📅 {datetime.now().strftime('%Y-%m-%d')} 饮食运动日报 ===
【⚖️ 晨重】：{st.session_state.log_data['体重']} kg

【☕️ 早餐】
{st.session_state.log_data['早餐']['text'] or "（未记录/同上）"}
[图片]：{get_img_status('早餐')}

【🍗 午餐】
{st.session_state.log_data['午餐']['text'] or "（未记录）"}
[图片]：{get_img_status('午餐')}

【🥗 晚餐】
{st.session_state.log_data['晚餐']['text'] or "（未记录）"}
[图片]：{get_img_status('晚餐')}

【🥊 加餐/运动】
{st.session_state.log_data['加餐/运动']['text'] or "（没练/没加餐）"}

---------------------------
👨‍🏫 教练请分析！(截图我会单独发在聊天框里)
    """
    
    st.success("打包成功！请点击下方【复制】按钮，然后发给我！")
    st.code(report, language="text")
    st.balloons()