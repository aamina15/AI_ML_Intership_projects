import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------

st.set_page_config(
    page_title="Google Play Store Dashboard",
    page_icon="📱",
    layout="wide"
)

# -----------------------------------------
# CUSTOM CSS
# -----------------------------------------

st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#EEF7FF,#FFFFFF,#F5FAFF);
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

.title{
font-size:42px;
font-weight:bold;
color:#0F62FE;
text-align:center;
}

.subtitle{
font-size:18px;
color:gray;
text-align:center;
margin-bottom:25px;
}

.card{
background:white;
padding:15px;
border-radius:15px;
box-shadow:0px 4px 12px rgba(0,0,0,0.08);
}

</style>
""",unsafe_allow_html=True)

# -----------------------------------------
# TITLE
# -----------------------------------------

st.markdown("""
<div class="title">
📱 Google Play Store Analytics Dashboard
</div>

<div class="subtitle">
Interactive Data Visualization of Google Play Store Applications
</div>
""",unsafe_allow_html=True)

# -----------------------------------------
# LOAD DATA
# -----------------------------------------

@st.cache_data
def load_data():
    df=pd.read_csv("googleplaystore.csv")
    return df

df=load_data()

# -----------------------------------------
# DATA CLEANING
# -----------------------------------------

df=df.drop_duplicates()

df["Rating"]=pd.to_numeric(df["Rating"],errors="coerce")

df["Reviews"]=pd.to_numeric(df["Reviews"],errors="coerce")

df["Installs"]=(
df["Installs"]
.astype(str)
.str.replace("+","",regex=False)
.str.replace(",","",regex=False)
)

df["Installs"]=pd.to_numeric(df["Installs"],errors="coerce")

df["Price"]=(
df["Price"]
.astype(str)
.str.replace("$","",regex=False)
)

df["Price"]=pd.to_numeric(df["Price"],errors="coerce")

df=df.dropna()

# -----------------------------------------
# SIDEBAR
# -----------------------------------------

st.sidebar.title("Filters")

category=st.sidebar.selectbox(
"Category",
["All"]+sorted(df["Category"].unique())
)

app_type=st.sidebar.selectbox(
"Type",
["All"]+sorted(df["Type"].unique())
)

if category!="All":
    df=df[df["Category"]==category]

if app_type!="All":
    df=df[df["Type"]==app_type]

# -----------------------------------------
# KPI CARDS
# -----------------------------------------

c1,c2,c3,c4=st.columns(4)

c1.metric("📱 Total Apps",len(df))

c2.metric("⭐ Avg Rating",
round(df["Rating"].mean(),2))

c3.metric("📂 Categories",
df["Category"].nunique())

c4.metric("⬇ Total Installs",
f"{int(df['Installs'].sum()):,}")

st.divider()

# -----------------------------------------
# CHART 1
# -----------------------------------------

st.subheader("⭐ Rating Distribution")

fig1=px.histogram(
df,
x="Rating",
nbins=20,
color_discrete_sequence=["royalblue"]
)

fig1.update_layout(height=350)

st.plotly_chart(fig1,use_container_width=True)

# -----------------------------------------
# CHART 2
# -----------------------------------------

st.subheader("📂 Top Categories")

cat=df.groupby("Category")["App"].count().sort_values(
ascending=False
).head(10)

fig2=px.bar(
cat,
x=cat.values,
y=cat.index,
orientation="h",
color=cat.values,
color_continuous_scale="Blues"
)

fig2.update_layout(height=420)

st.plotly_chart(fig2,use_container_width=True)

# -----------------------------------------
# CHART 3
# -----------------------------------------

st.subheader("📥 Installs by Category")

install=df.groupby("Category")["Installs"].sum().sort_values(
ascending=False
).head(10)

fig3=px.bar(
install,
x=install.index,
y=install.values,
color=install.values,
color_continuous_scale="Viridis"
)

fig3.update_layout(height=420)

st.plotly_chart(fig3,use_container_width=True)
# -----------------------------------------
# CHART 4
# -----------------------------------------

st.subheader("💲 Price vs Rating")

fig4 = px.scatter(
    df,
    x="Price",
    y="Rating",
    color="Type",
    hover_name="App",
    size="Reviews",
    height=450
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------
# CHART 5
# -----------------------------------------

st.subheader("📝 Reviews vs Rating")

fig5 = px.scatter(
    df,
    x="Reviews",
    y="Rating",
    color="Category",
    hover_name="App",
    height=450
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------------------
# CHART 6
# -----------------------------------------

st.subheader("📱 Free vs Paid Apps")

type_df = (
    df["Type"]
    .value_counts()
    .reset_index()
)

type_df.columns = ["Type","Count"]

fig6 = px.pie(
    type_df,
    names="Type",
    values="Count",
    hole=0.45
)

fig6.update_layout(height=400)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------------------
# CHART 7
# -----------------------------------------

st.subheader("👥 Content Rating")

content = (
    df["Content Rating"]
    .value_counts()
    .reset_index()
)

content.columns = ["Content Rating","Count"]

fig7 = px.bar(
    content,
    x="Content Rating",
    y="Count",
    color="Count"
)

fig7.update_layout(height=400)

st.plotly_chart(fig7, use_container_width=True)

# -----------------------------------------
# SEARCH APP
# -----------------------------------------

st.divider()

st.subheader("🔍 Search an App")

search = st.text_input("Enter App Name")

if search:

    result = df[
        df["App"]
        .str.contains(search,
                      case=False,
                      na=False)
    ]

    if len(result):

        st.dataframe(
            result,
            use_container_width=True
        )

    else:

        st.warning("No matching app found.")

# -----------------------------------------
# DATASET
# -----------------------------------------

st.divider()

with st.expander("📄 View Complete Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )

# -----------------------------------------
# BUSINESS INSIGHTS
# -----------------------------------------

st.divider()

st.subheader("📈 Business Insights")

st.info("""
• Most Play Store apps are Free.

• Higher installs do not always result in higher ratings.

• Several paid apps have excellent ratings but fewer installs.

• Family, Game and Tools are among the largest categories.

• Rating generally lies between 4.0 and 4.6.
""")

# -----------------------------------------
# ABOUT PROJECT
# -----------------------------------------

st.divider()

st.markdown("""
### 📖 About the Project

This dashboard analyzes the Google Play Store dataset to identify
the factors that influence an application's success.

The dashboard provides interactive visualizations,
filters and business insights using Python,
Pandas, Plotly and Streamlit.
""")

# -----------------------------------------
# TECHNOLOGIES
# -----------------------------------------

st.divider()

st.subheader("🛠 Technologies Used")

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Language","Python")
c2.metric("Library","Pandas")
c3.metric("Visualization","Plotly")
c4.metric("Framework","Streamlit")
c5.metric("IDE","Google Colab")

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.divider()

st.markdown(
"""
<div style='text-align:center;color:gray;'>

### 📱 Google Play Store Analytics Dashboard

Built with ❤️ using Python • Streamlit • Plotly • Pandas

</div>
""",
unsafe_allow_html=True
)
