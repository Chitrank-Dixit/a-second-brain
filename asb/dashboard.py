# asb/dashboard.py
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from asb.brain.insight_db import InsightDB

st_autorefresh = st.sidebar.checkbox("🔁 Auto-refresh every 60s", value=False)
if st_autorefresh:
    st.experimental_rerun()

st.set_page_config(page_title="Agentic Second Brain", layout="wide", page_icon="🧠")

st.title("🧠 Agentic Second Brain Dashboard")
st.caption("Visualizing reflections, insights, and cognitive evolution")

# ---- Load Insight Data ----
db_path = "./data/insights.db"
if not os.path.exists(db_path):
    st.error("No insights database found. Run some reflections or research first.")
    st.stop()

db = InsightDB(db_path)
conn = db.conn
df = pd.read_sql_query("SELECT * FROM insights ORDER BY date DESC", conn)
conn.close()

# ---- Sidebar Filters ----
topics = ["All"] + sorted(df["topic"].dropna().unique().tolist())
selected_topic = st.sidebar.selectbox("Filter by Topic", topics)
if selected_topic != "All":
    df = df[df["topic"] == selected_topic]

st.sidebar.info(f"🗂️ Showing {len(df)} insights")

# ---- Recent Insights ----
st.subheader("🧩 Recent Insights")
for _, row in df.head(5).iterrows():
    with st.expander(f"**{row['topic']}** — {row['question']} ({row['date']})"):
        st.write(row["answer"])
        if row.get("tags"):
            st.caption(f"🏷️ {row['tags']}")

# ---- Reflection Metrics ----
metrics_path = "./data/metrics/self_scores.csv"

if os.path.exists(metrics_path):
    try:
        # Flexible parse
        metrics = pd.read_csv(
            metrics_path,
            engine="python",
            on_bad_lines="skip",
            header=None
        )

        # Define safe column names dynamically
        default_cols = [
            "timestamp",
            "file",
            "clarity",
            "novelty",
            "actionability",
            "redundancy",
            "topics",
            "suggestions"
        ]

        # Trim or extend column names based on file width
        num_cols = len(metrics.columns)
        metrics.columns = default_cols[:num_cols]

        # 🧩 Try to coerce numeric columns if they exist
        for col in ["clarity", "novelty", "actionability", "redundancy"]:
            if col in metrics.columns:
                metrics[col] = pd.to_numeric(metrics[col], errors="coerce")

        # Drop rows missing all numeric fields
        available_cols = [c for c in ["clarity", "novelty", "actionability", "redundancy"] if c in metrics.columns]
        if available_cols:
            metrics = metrics.dropna(subset=available_cols, how="all")

        # Limit to most recent 50 entries
        metrics = metrics.tail(50)

    except Exception as e:
        st.error(f"Failed to parse metrics file: {e}")
        metrics = None
else:
    metrics = None

if metrics is not None and not metrics.empty:
    st.subheader("📊 Reflection Quality Trends")

    # only plot numeric columns that exist
    numeric_cols = [c for c in ["clarity", "novelty", "actionability", "redundancy"] if c in metrics.columns]

    if numeric_cols:
        try:
            fig = px.line(
                metrics,
                x="timestamp",
                y=numeric_cols,
                markers=True,
                title="Reflection Quality Over Time"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Could not render chart: {e}")
    else:
        st.info("No numeric reflection metrics found yet. Run `uv run asb evaluate` to generate them.")

# ---- Reflection Timeline ----
st.subheader("🕰️ Reflection Timeline")
timeline_dir = "./data/reflections"
if os.path.exists(timeline_dir):
    reflections = sorted(
        [f for f in os.listdir(timeline_dir) if f.endswith(".md")],
        reverse=True
    )
    selected_reflection = st.selectbox("Select a reflection", reflections)
    if selected_reflection:
        with open(os.path.join(timeline_dir, selected_reflection)) as f:
            st.markdown(f.read())
else:
    st.warning("No reflections found. Run `uv run asb reflect` to create one.")

# ---- Tags Overview ----
if "tags" in df.columns:
    tag_counts = (
        df["tags"].dropna().str.split(",").explode().str.strip().value_counts().head(15)
    )
    st.subheader("🏷️ Top Tags")
    st.bar_chart(tag_counts)

st.sidebar.markdown("---")
st.sidebar.success("✅ Dashboard ready — live view of your Second Brain.")


# ---- Semantic Search ----
from asb.brain.memory import Memory
from asb.brain.agent import ASBAgent

st.markdown("---")
st.subheader("🔍 Semantic Search — Ask Your Brain")

query = st.text_input("Ask anything you've reflected, researched, or learned:")
if query:
    memory = Memory()
    results = memory.collection.query(query_texts=[query], n_results=3)
    if results["documents"]:
        st.success("Top related insights:")
        for i, doc in enumerate(results["documents"][0]):
            st.write(f"**{i+1}.** {doc}")
    else:
        st.warning("No semantic matches found.")


# ---- Knowledge Graph Visualization ----
import networkx as nx
from pyvis.network import Network
import tempfile

st.markdown("---")
st.subheader("🕸 Knowledge Graph")

if not df.empty:
    G = nx.Graph()
    for _, row in df.iterrows():
        topic = row["topic"] or "misc"
        question = row["question"][:80]
        G.add_node(topic, color="#1f77b4", size=20)
        G.add_node(question, color="#ff7f0e", size=10)
        G.add_edge(topic, question)

    net = Network(height="600px", width="100%", bgcolor="#111", font_color="white")
    net.from_nx(G)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        st.components.v1.html(open(tmp_file.name, "r", encoding="utf-8").read(), height=600)
else:
    st.info("No insights found for graph visualization.")


# ---- Insight Analytics ----
st.markdown("---")
st.subheader("📈 Insight Analytics")

if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    daily_counts = df.groupby(df["date"].dt.date).size().reset_index(name="insights")
    fig = px.bar(daily_counts, x="date", y="insights", title="Reflections & Insights Over Time")
    st.plotly_chart(fig, use_container_width=True)

    top_topics = df["topic"].value_counts().head(10)
    st.write("### 🔝 Top 10 Topics")
    st.bar_chart(top_topics)
else:
    st.warning("No insights to analyze yet.")