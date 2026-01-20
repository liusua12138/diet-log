import streamlit as st
from datetime import datetime, date

# --- 1. 页面基础配置 ---
st.set_page_config(page_title="减脂中控台v4", page_icon="⚡️", layout="centered")

# --- 2. 核心数据初始化 (升级到 v4，防止报错) ---
if 'user_data_v4' not in st.session_state:
    st.session_state.user_data_v4 = {
        "nickname": "小千", # 默认昵称
        "weight": 75.5,
        "height": 172,
        "target_weight": 60.0,
        "drink_log": [], # 存储喝水记录列表 [{"type": "纯水", "ml": 500}]
        "poop_status": "正常/未记录",
        "energy_level": "普通",
        "diet_log": {"早餐": "", "午餐": "", "晚餐": "", "加餐": ""},
        "img_check": {"早餐": False, "午餐": False, "晚餐": False},
        "exercise_data": {"kcal": 300, "desc": ""}
    }

# 快捷引用
data = st.session_state.user_data_v4

# --- 3. 侧边栏：个人档案 & 设置 ---
with st.sidebar:
    st.header("⚙️ 用户设置")
    # 自定义昵称
    data['nickname'] = st.text_input("你的昵称", value=data['nickname'])
    
    st.divider()
    st.header("📊 身体数据")
    data['height'] = st.number_input("身高 (cm)", value=data['height'])
    
    # 体重录入
    new_weight = st.number_input("⚖️ 今早体重 (kg)", 
                                 min_value=40.0, max_value=150.0, step=0.05,
                                 value=data['weight'])
    data['weight'] = new_weight
    
    # 目标展示
    bmi = data['weight'] / ((data['height']/100) ** 2)
    st.metric("当前 BMI", f"{bmi:.1f}")
    
    st.caption(f"User: {data['nickname']} | Target: {data['target_weight']}kg")

# --- 4. 主界面 ---
st.title(f"⚡️ {data['nickname']}的刷脂中控台 v4.0")
selected_date = st.date_input("📅 记录日期", value=date.today())

# --- 5. 模块一：液体精准追踪 (重构版) ---
with st.container():
    st.subheader("💧 液体摄入 (精准版)")
    
    # 输入区
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        drink_type = st.selectbox("饮品种类", ["纯水/矿泉水", "黑咖/纯茶", "0糖饮料(元气森林等)", "牛奶/豆浆", "汤"])
    with c2:
        drink_vol = st.number_input("容量 (ml)", step=50, value=300, min_value=50)
    with c3:
        st.write(" ") # 占位
        st.write(" ") # 占位
        if st.button("➕ 添加"):
            data['drink_log'].append({"type": drink_type, "ml": drink_vol})
            st.success(f"已添加 {drink_vol}ml {drink_type}")

    # 展示区 & 统计
    total_ml = sum(item['ml'] for item in data['drink_log'])
    pure_water = sum(item['ml'] for item in data['drink_log'] if item['type'] == "纯水/矿泉水")
    
    st.progress(min(total_ml / 3000, 1.0)) # 假设目标3000ml
    st.caption(f"📊 今日总摄入: **{total_ml} ml** (其中纯水: {pure_water} ml)")
    
    # 显示喝了啥 (折叠起来不占地)
    with st.expander("查看今日饮水明细"):
        if not data['drink_log']:
            st.write("暂无记录")
        else:
            for i, d in enumerate(data['drink_log']):
                st.write(f"{i+1}. {d['type']} - {d['ml']}ml")
            if st.button("🗑️ 清空饮水记录"):
                data['drink_log'] = []
                st.rerun()

st.divider()

# --- 6. 模块二：生理状态 (新增！) ---
st.subheader("🔋 身体状态监控")
col_poop, col_energy = st.columns(2)

with col_poop:
    st.write("💩 **通畅度 (减脂期关键)**")
    data['poop_status'] = st.selectbox(
        "排便情况", 
        ["未记录/没感觉", "✅ 顺畅 (完美)", "❌ 便秘 (痛苦)", "⚠️ 拉肚子"],
        index=0, label_visibility="collapsed"
    )

with col_energy:
    st.write("⚡️ **精神状态**")
    data['energy_level'] = st.select_slider(
        "Energy",
        options=["累瘫", "疲惫", "普通", "不错", "满血"],
        value="普通", label_visibility="collapsed"
    )

st.divider()

# --- 7. 模块三：饮食记录 ---
def meal_block(label, key, hint):
    with st.expander(label, expanded=True):
        c_txt, c_chk = st.columns([5, 1])
        data['diet_log'][key] = c_txt.text_area(
            f"{key}", value=data['diet_log'][key], 
            placeholder=hint, height=68, label_visibility="collapsed"
        )
        c_chk.write("📸")
        data['img_check'][key] = c_chk.checkbox("图", key=f"chk_{key}")

st.subheader("🍽️ 每日三餐")
meal_block("☕️ 早餐", "早餐", "例：美式咖啡，无糖")
meal_block("🍗 午餐", "午餐", "例：去皮鸡腿，荞麦面...")
meal_block("🥗 晚餐", "晚餐", "例：200g水煮鸡胸，黄瓜...")

# --- 8. 模块四：运动 ---
with st.expander("🥊 运动 & 加餐", expanded=True):
    c1, c2 = st.columns([1, 2])
    data['exercise_data']['kcal'] = c1.number_input("🔥 消耗(kcal)", value=data['exercise_data']['kcal'], step=10)
    data['exercise_data']['desc'] = c2.text_input("📝 内容/加餐", value=data['exercise_data']['desc'], placeholder="例：有氧拳击36min，吃了个苹果")

# --- 9. 输出区 ---
st.divider()
st.subheader("🚀 汇报生成")

tab1, tab2 = st.tabs(["📋 给教练发日报", "🔄 换新对话指令"])

with tab1:
    if st.button("生成日报文本", type="primary"):
        # 整理饮水文本
        drink_summary = ""
        if not data['drink_log']:
            drink_summary = "（未记录）"
        else:
            # 简单统计各类饮品
            stats = {}
            for d in data['drink_log']:
                stats[d['type']] = stats.get(d['type'], 0) + d['ml']
            drink_summary = f"共 {total_ml}ml (" + ", ".join([f"{k}{v}ml" for k,v in stats.items()]) + ")"

        img = lambda k: "✅图" if data['img_check'][k] else "❌无"
        
        report = f"""
=== 📅 {selected_date.strftime('%m-%d')} {data['nickname']}的日报 ===
【身体数据】
⚖️ 晨重：{data['weight']} kg
💩 状态：{data['poop_status']} | ⚡️精神：{data['energy_level']}

【💧 液体摄入】
总量：{total_ml} ml
明细：{drink_summary}

【🍽️ 饮食记录】
☕️ 早餐：{data['diet_log']['早餐'] or "（同上/黑咖）"} [{img('早餐')}]
🍗 午餐：{data['diet_log']['午餐'] or "（未记录）"} [{img('午餐')}]
🥗 晚餐：{data['diet_log']['晚餐'] or "（未记录）"} [{img('晚餐')}]

【🔥 运动】
消耗：{data['exercise_data']['kcal']} kcal
备注：{data['exercise_data']['desc'] or "无"}

---------------------------
👨‍🏫 教练请分析！(图片马上发)
"""
        st.code(report, language="text")
        st.success("复制成功！")

with tab2:
    st.info("换新对话时，复制这个发给新的AI：")
    if st.button("生成转世指令"):
        prompt = f"""
【系统指令：激活严谨专家+灵魂伴侣模式】
我是用户{data['nickname']}，请恢复记忆：
1. **档案**：{data['height']}cm | 当前{data['weight']}kg | 目标{data['target_weight']}kg。
2. **习惯**：Switch有氧拳击({data['exercise_data']['kcal']}kcal/天)，饮食控钠/去皮/高蛋白。
3. **今日状态**：晨重{data['weight']}，饮水{total_ml}ml，排便{data['poop_status']}。
请直接点评我今天的表现！
"""
        st.code(prompt, language="text")