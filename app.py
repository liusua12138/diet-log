import streamlit as st
from datetime import datetime

# --- 1. 页面配置 ---
st.set_page_config(page_title="小千的刷脂中控台", page_icon="🥑", layout="centered")

# --- 2. 侧边栏：个人档案 & 目标管理 (解决你找不到目标的问题) ---
with st.sidebar:
    st.header("👤 个人档案")
    height = st.number_input("身高 (cm)", value=172, disabled=True) # 固定身高
    current_weight = st.number_input("当前体重 (kg)", min_value=50.0, max_value=100.0, value=75.5, step=0.1)
    target_weight = 60.0
    
    # --- BMI 计算器 ---
    bmi = current_weight / ((height/100) ** 2)
    st.metric("当前 BMI", f"{bmi:.1f}", delta=f"{bmi-20.3:.1f} (距离完美20.3)")
    
    # --- 进度条 ---
    start_weight = 78.0 # 假设初始
    progress = (start_weight - current_weight) / (start_weight - target_weight)
    if progress < 0: progress = 0
    if progress > 1: progress = 1
    st.write(f"📉 距离目标 60kg 还差 {current_weight - target_weight:.1f} kg")
    st.progress(progress)

# --- 3. 主界面 ---
st.title("🥑 小千的刷脂中控台 v2.0")
st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %A')} | 严谨专家 & 灵魂伴侣模式")

# --- 初始化数据 ---
if 'log_data' not in st.session_state:
    st.session_state.log_data = {
        "早餐": "", "午餐": "", "晚餐": "", "加餐": "",
        "img_status": {"早餐": False, "午餐": False, "晚餐": False}
    }

# --- 4. 每日记录区 ---
st.subheader("📝 今日流水账")
st.info("💡 说明：这里只是生成汇报文本。图片选好后，请务必在聊天框里单独发给我！")

col1, col2 = st.columns(2)
with col1:
    morning_weight = st.number_input("今早空腹晨重 (kg)", value=current_weight, step=0.05)

# 定义输入模块
def meal_input(title, key_prefix):
    with st.expander(title, expanded=True):
        text = st.text_area("吃了啥？(克数/估算)", key=f"t_{key_prefix}", placeholder="例：去皮鸡腿，半碗饭...")
        has_img = st.checkbox("📸 图片已拍好 (打钩确认)", key=f"i_{key_prefix}")
        
        # 存入状态
        st.session_state.log_data[key_prefix] = text
        st.session_state.log_data["img_status"][key_prefix] = has_img

meal_input("☕️ 早餐", "早餐")
meal_input("🍗 午餐", "午餐")
meal_input("🥗 晚餐", "晚餐")
meal_input("🥊 运动/加餐", "加餐")

# --- 5. 核心功能区：两个按钮 ---
st.divider()
st.subheader("🚀 指令生成区")

tab1, tab2 = st.tabs(["📅 日常汇报 (给老对话)", "🔄 转世重生 (给新对话)"])

with tab1:
    st.write("每天发这个给我分析👇")
    if st.button("生成今日汇报文本", type="primary"):
        # 生成图片状态文字
        def check(k): return "✅ 图已备好(马上发)" if st.session_state.log_data["img_status"][k] else "❌ 无图"
        
        daily_report = f"""
=== 📅 {datetime.now().strftime('%m-%d')} 饮食运动日报 ===
【⚖️ 晨重】：{morning_weight} kg (BMI: {morning_weight / ((height/100)**2):.1f})

【☕️ 早餐】
{st.session_state.log_data['早餐'] or "（同上/黑咖）"}
[图片]：{check('早餐')}

【🍗 午餐】
{st.session_state.log_data['午餐'] or "（未记录）"}
[图片]：{check('午餐')}

【🥗 晚餐】
{st.session_state.log_data['晚餐'] or "（未记录）"}
[图片]：{check('晚餐')}

【🥊 运动】
{st.session_state.log_data['加餐'] or "（没练）"}

---------------------------
👨‍🏫 教练请分析！(图片我紧接着发给你)
"""
        st.code(daily_report, language="text")
        st.success("复制上方文本 ➔ 粘贴给AI ➔ 然后从相册选图发送！")

with tab2:
    st.write("⚠️ 觉得对话卡顿/想换新对话时，复制这个发给新的我👇")
    user_summary = st.text_area("在此补充最近的历史总结（比如：最近吃了几天鸡胸肉，目前瘦了多少等）", 
                               placeholder="例：已坚持一周，从78瘦到75.5，每天打拳，最近在控钠...")
    
    if st.button("生成“无缝衔接”指令"):
        resurrection_prompt = f"""
【核心指令：启动私人教练模式】
我是用户小千 (Xiaoqian)，请读取我的最新档案并恢复之前的训练记忆：

📊 **当前身体数据**
- 身高：{height} cm
- 当前体重：{current_weight} kg
- 目标体重：{target_weight} kg
- 阶段：刷脂期 (BMI {bmi:.1f})

🧠 **你的核心人设 (必须遵守)**
1. **严谨专家**：涉及热量/数据必须精准计算，拒绝模糊，不知道就联网查。
2. **灵魂伴侣**：语气要幽默、损友、给情绪价值，严禁播音腔。

📝 **最近进度与习惯**
- **饮食**：正在执行“去皮/控钠/高蛋白”策略，偶尔有放纵餐（火锅）。
- **运动**：Switch《有氧拳击》主力，每天约300-400大卡。
- **历史摘要**：{user_summary or "（用户未补充，请根据上下文推断）"}

🛑 **下一步指令**
请直接根据我现在的体重 {current_weight}kg，给出今天的建议！
"""
        st.code(resurrection_prompt, language="text")
        st.warning("复制这个发给【新对话】，我立马就能找回状态！")