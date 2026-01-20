import streamlit as st
from datetime import datetime, date

# --- 1. 页面配置 ---
st.set_page_config(page_title="减脂中控台v5", page_icon="🦁", layout="wide") # 开宽屏模式

# --- 2. 核心数据初始化 ---
if 'user_data_v5' not in st.session_state:
    st.session_state.user_data_v5 = {
        "nickname": "流苏",
        "gender": "男",
        "age": 22,
        "height": 172,
        "weight": 75.5,
        "target_weight": 60.0,
        "drink_log": [], # [{"time": "10:00", "type": "黑咖", "ml": 300}]
        "extra_meals": [], # [{"time": "15:00", "desc": "饼干", "has_img": False}]
        "diet_log": {"早餐": "", "午餐": "", "晚餐": ""},
        "img_status": {"早餐": False, "午餐": False, "晚餐": False},
        "exercise": {"kcal": 300, "desc": "Switch有氧拳击"},
        "poop": "未记录",
        "history_memory": "" # 核心：存储你之前的长篇总结
    }

# 快捷变量
data = st.session_state.user_data_v5

# --- 3. 侧边栏：设置与记忆库 ---
with st.sidebar:
    st.title("⚙️ 核心参数")
    
    with st.expander("👤 个人档案 (可修改)", expanded=True):
        data['nickname'] = st.text_input("昵称", data['nickname'])
        c1, c2 = st.columns(2)
        data['gender'] = c1.selectbox("性别", ["男", "女"])
        data['age'] = c2.number_input("年龄", value=data['age'])
        data['height'] = st.number_input("身高(cm)", value=data['height'])
        
        # 目标体重可修改
        data['target_weight'] = st.number_input("🏁 目标体重(kg)", value=data['target_weight'], step=0.5)

    # 🔥 代谢计算器 (Mifflin-St Jeor 公式)
    st.markdown("---")
    st.subheader("🔥 你的代谢底线")
    if data['gender'] == "男":
        bmr = (10 * data['weight']) + (6.25 * data['height']) - (5 * data['age']) + 5
    else:
        bmr = (10 * data['weight']) + (6.25 * data['height']) - (5 * data['age']) - 161
    
    tdee = bmr * 1.375 # 假设每周运动3-5次
    st.info(f"""
    **基础代谢 (BMR):** {int(bmr)} kcal/天
    *(躺着不动消耗的热量)*
    
    **日常消耗 (TDEE):** {int(tdee)} kcal/天
    *(保持当前体重需要的热量)*
    
    💡 **刷脂建议摄入:** {int(bmr)} - {int(bmr)+200} kcal
    """)

    # 📜 历史记忆库 (无缝衔接的关键)
    st.markdown("---")
    st.subheader("📜 历史记忆库")
    st.caption("把之前几天AI给你的总结（比如你发给我的那个模板）全部粘贴在这里。下次生成指令时，会自动带上！")
    data['history_memory'] = st.text_area("粘贴历史总结", value=data['history_memory'], height=200, placeholder="在此粘贴之前的长篇总结...")

# --- 4. 主界面 ---
st.title(f"🦁 {data['nickname']}的刷脂中控台 v5.0")
c_date, c_weight = st.columns([1, 1])
with c_date:
    record_date = st.date_input("📅 记录日期", value=date.today())
with c_weight:
    new_weight = st.number_input("⚖️ 今早晨重 (kg)", value=data['weight'], step=0.05)
    data['weight'] = new_weight

# --- 5. 模块：液体追踪 (可撤销版) ---
st.divider()
c1, c2 = st.columns([2, 1])
with c1:
    st.subheader("💧 饮水记录")
    
    # 添加区
    cc1, cc2, cc3 = st.columns([2, 1, 1])
    d_type = cc1.selectbox("种类", ["纯水", "黑咖/茶", "0糖饮料", "牛奶", "汤"], label_visibility="collapsed")
    d_ml = cc2.number_input("ml", value=300, step=50, label_visibility="collapsed")
    if cc3.button("➕ 喝一杯"):
        data['drink_log'].append({"type": d_type, "ml": d_ml, "time": datetime.now().strftime("%H:%M")})
        st.rerun()

    # 展示与撤销
    total_water = sum(d['ml'] for d in data['drink_log'])
    st.write(f"📊 今日总量：**{total_water} ml**")
    
    if data['drink_log']:
        with st.expander(f"查看明细 ({len(data['drink_log'])}条)"):
            for i, d in enumerate(data['drink_log']):
                st.text(f"{d['time']} | {d['type']} {d['ml']}ml")
            if st.button("🗑️ 撤销最后一条", type="secondary"):
                data['drink_log'].pop()
                st.rerun()

with c2:
    st.subheader("💩 肠胃监控")
    data['poop'] = st.radio("排便", ["未记录", "✅ 顺畅", "❌ 便秘", "⚠️ 拉肚子"], label_visibility="collapsed")

# --- 6. 模块：饮食与零食 (图片预览版) ---
st.divider()
st.subheader("🍽️ 饮食时间轴")

# 主餐部分
c_b, c_l, c_d = st.columns(3)
def meal_card(col, title, key):
    with col:
        st.markdown(f"**{title}**")
        data['diet_log'][key] = st.text_area(key, data['diet_log'][key], height=80, placeholder="吃了啥...", label_visibility="collapsed")
        # 图片上传仅做预览和确认
        img = st.file_uploader(f"上传{key}图", type=['jpg','png'], key=f"u_{key}")
        if img:
            st.image(img, caption="已存图", width=100)
            data['img_status'][key] = True
        else:
            data['img_status'][key] = False

meal_card(c_b, "☕️ 早餐", "早餐")
meal_card(c_l, "🍗 午餐", "午餐")
meal_card(c_d, "🥗 晚餐", "晚餐")

# 零食/加餐补录 (随时插队)
st.markdown("#### 🍪 零食/其他加餐 (防漏记)")
with st.expander("➕ 添加额外记录 (零食/偷吃/加餐)", expanded=False):
    ec1, ec2, ec3 = st.columns([1, 3, 1])
    e_time = ec1.time_input("时间", value=datetime.now().time())
    e_desc = ec2.text_input("吃了什么？", placeholder="例：下午3点偷吃了一块饼干")
    if ec3.button("📥 录入"):
        data['extra_meals'].append({"time": e_time.strftime("%H:%M"), "desc": e_desc})
        st.success("已录入")
        st.rerun()

# 展示额外记录
if data['extra_meals']:
    for em in data['extra_meals']:
        st.info(f"🕒 {em['time']} | {em['desc']}")

# --- 7. 模块：运动 ---
st.divider()
st.subheader("🥊 运动消耗")
kc, kd = st.columns([1, 3])
data['exercise']['kcal'] = kc.number_input("消耗 (kcal)", value=data['exercise']['kcal'], step=10)
data['exercise']['desc'] = kd.text_input("内容", value=data['exercise']['desc'])

# --- 8. 核心：超级指令生成 ---
st.divider()
st.header("🚀 智能中枢")

tab_daily, tab_life = st.tabs(["📋 生成今日日报 (发给我)", "🔄 生成无缝转世指令 (发给新AI)"])

with tab_daily:
    if st.button("生成日报文本", type="primary"):
        # 整理零食文本
        extra_str = "\n".join([f"- {e['time']} {e['desc']}" for e in data['extra_meals']]) if data['extra_meals'] else "（无加餐）"
        # 整理饮水
        water_details = ", ".join([f"{d['type']}" for d in data['drink_log']])
        img_check = lambda k: "✅图已备好" if data['img_status'][k] else "❌无图"
        
        report = f"""
=== 📅 {record_date.strftime('%Y-%m-%d')} {data['nickname']}日报 ===
【身体数据】
⚖️ 晨重：{data['weight']} kg (BMI: {data['weight']/((data['height']/100)**2):.1f})
💩 排便：{data['poop']}
🔥 基础代谢：{int(bmr)} | 目标：{int(bmr)}~{int(bmr)+200}

【饮食流水账】
☕️ 早餐：{data['diet_log']['早餐'] or "未记录"} [{img_check('早餐')}]
🍗 午餐：{data['diet_log']['午餐'] or "未记录"} [{img_check('午餐')}]
🥗 晚餐：{data['diet_log']['晚餐'] or "未记录"} [{img_check('晚餐')}]
🍪 加餐/零食：
{extra_str}

【💧 液体摄入】
总量：{total_water} ml
内容：{water_details or "未记录"}

【🥊 运动】
内容：{data['exercise']['desc']}
消耗：{data['exercise']['kcal']} kcal

---------------------------
👨‍🏫 严谨专家请点评！(图片选好马上发)
"""
        st.code(report, language="text")

with tab_life:
    st.warning("⚠️ 此按钮用于：当你觉得对话卡顿，或者想换一个新的AI对话框时。")
    if st.button("生成“完美无缝衔接”指令"):
        # 1. 获取用户粘贴的历史记忆
        history_block = data['history_memory'] if data['history_memory'] else "（用户暂未粘贴历史记录，请基于今日数据分析）"
        
        # 2. 拼接今日数据
        extra_str = "; ".join([f"{e['time']} {e['desc']}" for e in data['extra_meals']])
        today_block = f"""
📅 {record_date.strftime('%Y-%m-%d')} (今日最新)
- 晨重：{data['weight']}kg
- 饮食：早[{data['diet_log']['早餐']}] 午[{data['diet_log']['午餐']}] 晚[{data['diet_log']['晚餐']}] 其他[{extra_str}]
- 饮水：{total_water}ml
- 运动：{data['exercise']['desc']} (-{data['exercise']['kcal']}kcal)
"""
        
        # 3. 组合终极Prompt
        final_prompt = f"""
【系统指令：激活严谨专家+灵魂伴侣模式】
我是用户{data['nickname']}，请执行“记忆恢复程序”。

📂 **第一部分：核心档案**
- 身高：{data['height']}cm | 当前体重：{data['weight']}kg | 目标：{data['target_weight']}kg
- 性别：{data['gender']} | 年龄：{data['age']}
- 代谢参考：BMR {int(bmr)} | TDEE {int(tdee)}
- 核心策略：Switch有氧拳击，控钠/去皮/高蛋白，16+8轻断食。

📜 **第二部分：历史完整日志 (请仔细读取)**
{history_block}

🆕 **第三部分：今日最新数据 (无缝衔接)**
{today_block}

🛑 **执行指令**
请结合我的历史趋势和今天的最新表现，直接给出点评和明天的建议！不要重复问我的信息，直接开始分析！
"""
        st.code(final_prompt, language="text")
        st.success("完美！全选复制上面这段话，发给任何一个新的AI，它都能秒懂你！")