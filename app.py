import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from ai import generate_coaching
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from avatar import generate_avatar
from streamlit_mic_recorder import mic_recorder
from voice import transcribe_audio
from voice_ai import analyze_reflection
from pdf_report import create_pdf
st.set_page_config(
    page_title="Life-OS",
    page_icon="📱",
    layout="wide"
)
if "reflection" not in st.session_state:
    st.session_state.reflection = ""

if "mood" not in st.session_state:
    st.session_state.mood = "🙂 Neutral"
st.markdown("""
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
""", unsafe_allow_html=True)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
df = pd.read_csv("screentime.csv")
df["Date"] = pd.to_datetime(df["Date"])

from datetime import datetime

today = datetime.now().strftime("%A, %d %B %Y")

st.markdown(
    f"""
<div style="
padding:32px;
border-radius:22px;
background: linear-gradient(135deg, #169C8C, #0F766E);
color:white;
box-shadow: 0 12px 30px rgba(15, 118, 110, 0.18);
">

<div style="display:flex;justify-content:space-between;align-items:center;">

<div>

<div style="
display:inline-block;
padding:7px 15px;
border-radius:30px;
background:rgba(255,255,255,.18);
backdrop-filter:blur(10px);
font-size:12px;
font-weight:700;
letter-spacing:1px;
margin-bottom:18px;
">
DIGITAL WELLBEING
</div>

<h1 style="margin:0;font-size:44px;">
📱 Life-OS Dashboard
</h1>

<p style="
margin-top:12px;
font-size:18px;
opacity:.9;
max-width:700px;
">
Track your digital habits, discover healthier routines and receive
personalized AI coaching.
</p>

</div>

<div style="
background:rgba(255,255,255,.15);
backdrop-filter:blur(8px);
padding:20px 24px;
border-radius:16px;
text-align:center;
min-width:200px;
box-shadow:0 8px 20px rgba(0,0,0,.08);
">

<div style="font-size:13px;opacity:.8;">
TODAY
</div>

<div style="
margin-top:8px;
font-size:17px;
font-weight:600;
">
{today}
</div>

</div>

</div>

</div>
""",
    unsafe_allow_html=True,
)
st.divider()

dates = sorted(df["Date"].dt.date.unique(), reverse=True)

with st.sidebar:

    st.markdown(
        """
<div style="
padding:20px;
border-radius:18px;
background:linear-gradient(135deg,#169C8C,#0F766E);
color:white;
text-align:center;
margin-bottom:25px;
">

<h2 style="margin-bottom:6px;">
📱 Life-OS
</h2>

<p style="font-size:14px;opacity:.9;">
Digital Wellbeing Dashboard
</p>

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("### 🎛 Dashboard Controls")

    selected_date = st.selectbox(
        "📅 Select Date",
        dates
    )

    daily_goal = st.slider(
        "🎯 Daily Screen Time Goal",
        1,
        12,
        5,
        help="Set your ideal maximum daily screen time."
    )

    st.divider()

    

  

    st.markdown("### 💡 Wellness Tip")

    st.info(
        "Small habits create big changes. Even reducing screen time by 30 minutes today can improve your focus tomorrow."
    )

    st.divider()

    st.caption("Life-OS • AI Builder Internship 2026")

day_df = df[df["Date"].dt.date == selected_date]

total_minutes = day_df["Minutes_Used"].sum()
total_hours = round(total_minutes / 60, 1)

most_used_app = (
    day_df.groupby("App_Name")["Minutes_Used"]
    .sum()
    .idxmax()
)

goal_minutes = daily_goal * 60
category_usage = (
    day_df.groupby("Category")["Minutes_Used"]
    .sum()
    .sort_values(ascending=False)
)
difference = total_minutes - goal_minutes

social = category_usage.get("Social Media", 0)
entertainment = category_usage.get("Entertainment", 0)
coding = category_usage.get("Coding", 0)
education = category_usage.get("Education", 0)
productivity = category_usage.get("Productivity", 0)

score = 100

score -= social * 0.18
score -= entertainment * 0.15

score += coding * 0.08
score += education * 0.06
score += productivity * 0.05

if total_minutes > goal_minutes:
    score -= (total_minutes - goal_minutes) * 0.10

score = max(0, min(100, round(score)))

productive_minutes = coding + education + productivity

daily_usage = (
    df.groupby("Date")["Minutes_Used"]
    .sum()
    .sort_index()
)

streak = 0

for minutes in reversed(daily_usage.tolist()):

    if minutes <= goal_minutes:
        streak += 1
    else:
        break

if difference > 0:
    delta = f"+{difference} min"
else:
    delta = f"{difference} min"

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric(
            "🕒 Screen Time",
            f"{total_hours} hrs",
            f"{round(total_hours-8,1)} hrs vs ideal"
        )

with col2:
    with st.container(border=True):
        st.metric(
            "📱 Most Used",
            most_used_app,
            f"{day_df['Minutes_Used'].max()} mins"
        )

with col3:
    with st.container(border=True):
        st.metric(
            "🎯 Goal",
            f"{daily_goal} hrs",
            delta,
            delta_color="inverse"
        )
with col4:
    with st.container(border=True):
        st.metric(
            "💡 Productivity Score",
            f"{score}%",
            f"{productive_minutes} productive mins"
        )
    

   

     
trend = (
    df.groupby("Date")["Minutes_Used"]
    .sum()
    .reset_index()
)


summary = (
    day_df
    .groupby("Category")["Minutes_Used"]
    .sum()
    .to_string()
)
top_apps = (
    day_df.groupby("App_Name")["Minutes_Used"]
    .sum()
    .sort_values(ascending=False)
)

    
line_chart = px.line(
    trend,
    x="Date",
    y="Minutes_Used",
    markers=True
)

line_chart.update_traces(

    line=dict(
        width=4,
        color="#14B8A6"
    ),

    marker=dict(
        size=8,
        color="#14B8A6"
    ),

    fill="tozeroy",
    fillcolor="rgba(20,184,166,.12)"
)

line_chart.update_layout(
    template="plotly_dark" if st.get_option("theme.base")=="dark" else "plotly_white",
    xaxis=dict(

    showgrid=False,

    zeroline=False

    ),

    yaxis=dict(

        gridcolor="rgba(128,128,128,.15)",

        zeroline=False

    ),
    height=380,
    margin=dict(l=10,r=10,t=20,b=10),
    xaxis_title="",
    yaxis_title="Minutes",
    legend_title=""
)

bar_chart = px.bar(
    x=category_usage.index,
    y=category_usage.values,
    color=category_usage.values,
    color_discrete_sequence=["#14B8A6"]
)

bar_chart.update_layout(
    template="plotly_dark" if st.get_option("theme.base")=="dark" else "plotly_white",
    showlegend=False,
    xaxis=dict(

    showgrid=False,

    zeroline=False

    ),

    yaxis=dict(

        gridcolor="rgba(128,128,128,.15)",

        zeroline=False

    ),
    height=380,
    margin=dict(l=10,r=10,t=20,b=10),
    xaxis_title="",
    yaxis_title="Minutes"
)

bar_chart.update_coloraxes(showscale=False)
donut = go.Figure(
    data=[
        go.Pie(

    labels=category_usage.index,

    values=category_usage.values,

    hole=.72,

    marker=dict(

        colors=[
            "#14B8A6",
            "#22C55E",
            "#06B6D4",
            "#F59E0B",
            "#EF4444"
        ]

    )

)
    ]
)

donut.update_layout(
    template="plotly_dark" if st.get_option("theme.base")=="dark" else "plotly_white",
    height=420,
    xaxis=dict(

    showgrid=False,

    zeroline=False

    ),

    yaxis=dict(

        gridcolor="rgba(128,128,128,.15)",

        zeroline=False

    ),
    margin=dict(l=10,r=10,t=20,b=10)
)
apps = px.bar(
    x=top_apps.values,
    y=top_apps.index,
    orientation="h",
    color=top_apps.values,
    color_discrete_sequence=["#22C55E"]
)

apps.update_layout(
    template="plotly_dark" if st.get_option("theme.base")=="dark" else "plotly_white",
    showlegend=False,
    xaxis=dict(

    showgrid=False,

    zeroline=False

    ),

    yaxis=dict(

        gridcolor="rgba(128,128,128,.15)",

        zeroline=False

    ),
    height=420,
    margin=dict(l=10,r=10,t=20,b=10),
    xaxis_title="Minutes",
    yaxis_title=""
)

apps.update_coloraxes(showscale=False)
weekly = (
    df.groupby("Category")["Minutes_Used"]
    .sum()
    .sort_values(ascending=False)
)


left,right=st.columns([3,1])

with left:
    with st.container(border=True):
        st.subheader("📈 Weekly Trend")
        st.plotly_chart(line_chart,use_container_width=True)

with right:
    with st.container(border=True):
        st.subheader("📊 Categories")
        st.plotly_chart(bar_chart,use_container_width=True)



left,right=st.columns(2)

with left:
    with st.container(border=True):
        st.subheader("🥯 Category Distribution")
        st.plotly_chart(donut,use_container_width=True)

with right:
    with st.container(border=True):
        st.subheader("📱 Top Apps")
        st.plotly_chart(apps,use_container_width=True)
        
weekly_avg = round(
    df.groupby("Date")["Minutes_Used"].sum().mean() / 60,
    1
)

with st.container(border=True):

    st.subheader("📈 Weekly Insights")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "🏆 Top Category",
            weekly.index[0]
        )

    with c2:
        st.metric(
            "⏳ Avg Daily",
            f"{weekly_avg} hrs"
        )

    with c3:
        st.metric(
            "📱 Apps Used",
            df["App_Name"].nunique()
        )
with st.container(border=True):

    st.subheader("🔥 Focus Streak")

    if streak == 0:
        st.error("No active streak")

        st.caption(
            "Stay within your goal tomorrow to begin a new streak."
        )

    else:
        st.metric(
            "Current Streak",
            f"{streak} Days"
        )

        st.progress(min(streak / 7, 1.0))

        st.caption(
            "You're building a healthier digital routine."
        )          

with st.container(border=True):

    st.subheader("📋 Today's Activity")
    activity_df = day_df.copy()

    activity_df["Date"] = activity_df["Date"].dt.strftime("%d %b %Y")

    activity_df = activity_df.rename(
        columns={
            "App_Name": "Application",
            "Minutes_Used": "Minutes"
        }
    )

    icons = {
        "Coding": "💻 Coding",
        "Social Media": "📱 Social Media",
        "Entertainment": "🎬 Entertainment",
        "Education": "📚 Education",
        "Productivity": "📈 Productivity"
    }

    activity_df["Category"] = activity_df["Category"].map(icons)

    activity_df = activity_df.sort_values(
        "Minutes",
        ascending=False
    )
    st.dataframe(
        activity_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Date": st.column_config.TextColumn("📅 Date"),
            "Application": st.column_config.TextColumn("📱 App"),
            "Category": st.column_config.TextColumn("📂 Category"),
            "Minutes (min)": st.column_config.ProgressColumn(
                "⏱ Minutes",
                min_value=0,
                max_value=300
            )
        }
    )

st.divider()

with st.container(border=True):
   
    title_col, badge_col = st.columns([5, 1])

    with title_col:
        st.subheader("🧠 AI Wellness Report")

    with badge_col:

        if total_minutes <= goal_minutes:
            badge = "🟢 Healthy"
            color = "#22C55E"

        elif total_minutes <= goal_minutes + 120:
            badge = "🟡 Moderate"
            color = "#F59E0B"

        else:
            badge = "🔴 High Screen Time"
            color = "#EF4444"

        st.markdown(
            f"""
    <div style="
    display:flex;
    justify-content:flex-end;
    align-items:center;
    height:55px;
    ">

    <div style="
    padding:8px 16px;
    background:{color}20;
    border:1px solid {color};
    border-radius:999px;
    color:{color};
    font-size:13px;
    font-weight:600;
    white-space:nowrap;
    ">
    {badge}
    </div>

    </div>
    """,
            unsafe_allow_html=True,
        )
    st.write(
        "Your personalized digital wellness analysis based on today's activity."
    )
    
    if st.button(
    "Generate AI Report",
    use_container_width=True
):

      with st.spinner("Life-OS is analyzing your habits..."):
          
            try:
              report = generate_coaching(
    summary,
    total_hours,
    score,
    most_used_app,
    difference,
    st.session_state.get("reflection", "")
)
              
            except Exception as e:
                st.error("Unable to generate AI report.")
                st.exception(e)
                st.stop()
      

            st.metric(
                "🧠 Wellness Score",
                f"{report['score']}/100"
            )

            c1, c2 = st.columns(2)

            with c1:

                st.success("### ✅ What's Going Well")

                for item in report["strengths"]:
                    st.write(f"• {item}")

            with c2:

                st.error("### ⚠ Needs Attention")

                for item in report["issues"]:
                    st.write(f"• {item}")

            st.info("### 🎯 Action Plan")

            for action in report["actions"]:
                st.write(f"✓ {action}")

            st.warning("### 🌅 Tomorrow's Challenge")

            st.write(report["challenge"])
            pdf_name = "LifeOS_Report.pdf"

            create_pdf(
                pdf_name,
                selected_date,
                total_hours,
                score,
                most_used_app,
                report
            )

            with open(pdf_name, "rb") as pdf:

                st.download_button(
                    "📄 Download Wellness Report",
                    pdf,
                    file_name="LifeOS_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
st.divider()


with st.container(border=True):

    st.subheader("🔗 Share Today's Progress")

    st.write(
    "Copy this link and share today's wellness report with a friend or accountability partner."
)

    base_url = "https://digital-wellbeing-dashboard.streamlit.app/"

    share_link = (
        f"{base_url}"
        f"?date={selected_date}"
        f"&screen_time={total_minutes}"
        f"&score={score}"
    )

    st.code(share_link)

    st.caption(
    "The link includes today's date, screen time and productivity score."
)
st.divider()    
with st.container(border=True):

    st.subheader("🎨 Today's Digital Avatar")

    if st.button(
        "Generate Avatar",
        use_container_width=True
    ):

       

            try:
               with st.spinner("🎨 Creating your digital avatar..."):
                avatar_url = generate_avatar(score)

                titles = {
                    "good": "🛡️ Digital Warrior",
                    "medium": "⚖️ Balance Keeper",
                    "low": "📱 Distracted Explorer",
                    "bad": "🧟 Screen-Time Zombie"
                }

                if score >= 80:
                    st.subheader(titles["good"])

                elif score >= 60:
                    st.subheader(titles["medium"])

                elif score >= 40:
                    st.subheader(titles["low"])

                else:
                    st.subheader(titles["bad"])

                st.image(
                    avatar_url,
                    width=450
                )

                if score >= 80:

                    st.success(
                        "Outstanding! Your digital habits today reflected focus, balance and productivity."
                    )

                elif score >= 60:

                    st.info(
                        "You're maintaining a healthy balance, but there's still room to reduce distractions."
                    )

                elif score >= 40:

                    st.warning(
                        "Distractions are beginning to affect your productivity. Try limiting unnecessary screen time."
                    )

                else:

                    st.error(
                        "Your screen habits today indicate excessive digital consumption. Consider taking regular breaks and spending time offline."
                    )

            except Exception:

                st.warning(
                    "⚠️ We couldn't generate your avatar right now."
                )

                if score >= 80:

                    st.info(
                        "Your productivity score indicates a **Digital Warrior**. Try generating the avatar again in a few moments."
                    )

                elif score >= 60:

                    st.info(
                        "Your productivity score indicates a **Balance Keeper**. Try generating the avatar again in a few moments."
                    )

                elif score >= 40:

                    st.info(
                        "Your productivity score indicates a **Distracted Explorer**. Try generating the avatar again in a few moments."
                    )

                else:

                    st.info(
                        "Your productivity score indicates a **Screen-Time Zombie**. Try generating the avatar again in a few moments."
                    )
st.divider()

with st.container(border=True):

    st.subheader("🎙 Daily Voice Journal")

    st.info("""
🎤 Take 10–20 seconds to answer:

• What distracted you today?

• Why did you spend more time on your phone?

• What's one thing you'll improve tomorrow?
""")

    audio = mic_recorder(
        start_prompt="🎙 Start Recording",
        stop_prompt="⏹ Stop Recording",
        key="voice"
    )

    if audio:

        st.success("✅ Recording completed")

        with st.spinner("Transcribing your voice..."):

            st.session_state.reflection = transcribe_audio(audio["bytes"])

            reflection = st.session_state.reflection

        reflection_lower = reflection.lower()

        if any(word in reflection_lower for word in [
            "happy","great","good","productive","excited","motivated"
        ]):
            mood = "😊 Positive"
            mood_color = "#22C55E"

        elif any(word in reflection_lower for word in [
            "stress","stressed","anxious","pressure","overwhelmed"
        ]):
            mood = "😟 Stressed"
            mood_color = "#EF4444"

        elif any(word in reflection_lower for word in [
            "tired","sleepy","lazy","exhausted"
        ]):
            mood = "😴 Tired"
            mood_color = "#F59E0B"

        elif any(word in reflection_lower for word in [
            "sick","fever","ill","cold","headache"
        ]):
            mood = "🤒 Recovering"
            mood_color = "#3B82F6"

        else:
            mood = "🙂 Neutral"
            mood_color = "#14B8A6"

        title_col, badge_col = st.columns([5,1])

        with title_col:
            st.subheader("📝 Today's Reflection")

        with badge_col:
            st.markdown(
                f"""
<div style="
display:flex;
justify-content:flex-end;
align-items:center;
height:55px;
">

<div style="
padding:7px 16px;
background:{mood_color}20;
border:1px solid {mood_color};
border-radius:999px;
color:{mood_color};
font-size:13px;
font-weight:600;
">
{mood}
</div>

</div>
""",
                unsafe_allow_html=True
            )

        st.chat_message("user").write(reflection)

        with st.spinner("🤖 Understanding your reflection..."):

            insight = analyze_reflection(
                reflection,
                mood
            )

        st.subheader("🤖 AI Reflection")

        st.markdown(
    f"""
<div style="
padding:20px;
border-radius:16px;
background:rgba(20,184,166,.08);
border-left:5px solid #14B8A6;
margin-top:10px;
">

<h4 style="margin-top:0;">
🧠 Life-OS Insight
</h4>

<p style="font-size:16px;line-height:1.8;">
{insight}
</p>

</div>
""",
    unsafe_allow_html=True
)
        
       