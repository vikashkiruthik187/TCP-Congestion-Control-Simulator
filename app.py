import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components
import importlib
import random
import engine
importlib.reload(engine)
from engine import run_simulation, calculate_jains_fairness

# Page Configuration - Single Screen Fit
st.set_page_config(
    page_title="NetPlus 3D | TCP Simulator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Ultra-Compact Styling for Zero Page Scrolling
st.markdown("""
<style>
    /* Hide Streamlit default header so our title isn't covered or pushed off */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .block-container {
        padding-top: 0.9rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1420px !important;
        margin: 0 auto;
    }
    
    /* Header Section */
    .main-header {
        text-align: center;
        padding: 0 0 0.5rem 0 !important;
        margin-bottom: 0.4rem !important;
    }
    .main-title {
        font-size: 2.1rem !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        display: inline-block !important;
        margin-bottom: 0.1rem !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.8rem !important;
        justify-content: center;
        border-bottom: 1px solid #1f2937 !important;
        margin-bottom: 0.45rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        color: #94a3b8 !important;
        padding: 0.3rem 0.75rem !important;
    }
    .stTabs [aria-selected="true"] {
        color: #60a5fa !important;
        border-bottom-color: #60a5fa !important;
    }

    /* Compact Controls Container */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #1f2937 !important;
        background-color: #111827 !important;
        border-radius: 10px !important;
        padding: 0.45rem 0.75rem !important;
        margin-bottom: 0.35rem !important;
    }
    
    label[data-testid="stWidgetLabel"] p {
        font-size: 0.73rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        margin-bottom: 0.1rem !important;
    }

    /* Compact Metric Cards */
    [data-testid="stMetric"] {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 8px !important;
        padding: 0.28rem 0.6rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.7rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 800 !important;
        font-size: 1.25rem !important;
    }

    /* Primary Button Polish */
    div.stButton > button:first-child {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        font-size: 0.82rem;
        border-radius: 6px;
        padding: 0.38rem 0.6rem;
        border: 1px solid #3b82f6;
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        border-color: #60a5fa;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- COMPACT TOP HEADER -----------------
st.markdown("""
<div class="main-header">
    <div class="main-title">NetPlus 3D</div>
</div>
""", unsafe_allow_html=True)

# ----------------- TABS (Existing 3 Kept Exactly As They Were + 2 Extra 3D Tabs Added) -----------------
nav_tab1, nav_tab2, nav_tab3, nav_tab4, nav_tab5 = st.tabs([
    "Single Simulation",
    "Protocol Benchmark (Tahoe vs Reno vs Cubic)",
    "Event Log & Metrics",
    "3D Network Digital Twin",
    "3D State Trajectory Space"
])

# Helper function to generate clean Dark-themed 2D Plotly charts
def create_flow_tcp_chart(df, bdp, rwnd, title="TCP Dynamics Over Time"):
    fig = go.Figure()

    # Congestion Window (cwnd)
    fig.add_trace(go.Scatter(
        x=df["Tick"],
        y=df["CongestionWindow"],
        mode="lines",
        name="cwnd",
        line=dict(color="#38bdf8", width=2.3),
        hovertemplate="<b>Tick:</b> %{x}<br><b>cwnd:</b> %{y:.2f} pkts<extra></extra>"
    ))

    # Effective Window: min(cwnd, rwnd)
    fig.add_trace(go.Scatter(
        x=df["Tick"],
        y=df["EffectiveWindow"],
        mode="lines",
        name="Effective [min(cwnd, rwnd)]",
        line=dict(color="#10b981", width=2.0),
        hovertemplate="<b>Tick:</b> %{x}<br><b>Effective Send:</b> %{y:.2f} pkts<extra></extra>"
    ))

    # Slow Start Threshold (ssthresh)
    fig.add_trace(go.Scatter(
        x=df["Tick"],
        y=df["Ssthresh"],
        mode="lines",
        name="ssthresh",
        line=dict(color="#fbbf24", width=1.6, dash="dash"),
        hovertemplate="<b>Tick:</b> %{x}<br><b>ssthresh:</b> %{y:.2f}<extra></extra>"
    ))

    # Receiver Window (rwnd) Limit Line (Flow Control)
    fig.add_trace(go.Scatter(
        x=[df["Tick"].min(), df["Tick"].max()],
        y=[rwnd, rwnd],
        mode="lines",
        name="rwnd Limit",
        line=dict(color="#c084fc", width=1.8, dash="dashdot"),
        hoverinfo="name"
    ))

    # BDP Optimal Pipe Capacity Line
    fig.add_trace(go.Scatter(
        x=[df["Tick"].min(), df["Tick"].max()],
        y=[bdp, bdp],
        mode="lines",
        name="BDP Capacity",
        line=dict(color="#f43f5e", width=1.8, dash="dot"),
        hoverinfo="name"
    ))

    # Packet Loss Markers
    loss_events = df[df["Loss"] == True]
    if not loss_events.empty:
        fig.add_trace(go.Scatter(
            x=loss_events["Tick"],
            y=loss_events["CongestionWindow"],
            mode="markers",
            name="Packet Loss",
            marker=dict(symbol="x", size=7, color="#ef4444", line=dict(width=1.5, color="#f87171")),
            hovertemplate="<b>Packet Loss!</b><br>Tick: %{x}<br>cwnd: %{y:.2f}<extra></extra>"
        ))

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=14, color="#f8fafc")
        ),
        xaxis=dict(
            title=dict(text="Time (Simulation Ticks)", font=dict(size=11, color="#94a3b8")),
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(size=10, color="#94a3b8"),
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="Window Size (Packets)", font=dict(size=11, color="#94a3b8")),
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(size=10, color="#94a3b8"),
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color="#cbd5e1", size=10)
        ),
        hovermode="x unified",
        margin=dict(l=35, r=35, t=65, b=25),
        height=365,
        paper_bgcolor="#111827",
        plot_bgcolor="#0b0f19",
        template="plotly_dark"
    )
    return fig


# ----------------- TAB 1: SINGLE SIMULATION (UNCHANGED ORIGINAL LAYOUT) -----------------
with nav_tab1:
    with st.container(border=True):
        c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 1.8, 1.8, 1.8, 1.8, 1.2, 1.3], vertical_alignment="bottom")

        with c1:
            sim_algo = st.selectbox("Algorithm", ["Cubic", "Reno", "Tahoe"], index=0, key="t1_algo")
        with c2:
            sim_ticks = st.slider("Duration", min_value=50, max_value=400, value=180, step=10, key="t1_ticks")
        with c3:
            sim_loss_pct = st.slider("Loss Rate (%)", min_value=0.5, max_value=20.0, value=4.0, step=0.5, key="t1_loss")
        with c4:
            sim_rwnd = st.slider("rwnd (Receiver)", min_value=10, max_value=80, value=35, step=5, key="t1_rwnd")
        with c5:
            sim_bdp = st.slider("BDP Capacity", min_value=10, max_value=60, value=25, step=2, key="t1_bdp")
        with c6:
            initial_ssthresh = st.number_input("ssthresh", min_value=4, max_value=48, value=16, step=2, key="t1_ssthresh")
        with c7:
            run_btn = st.button("Run", key="run_sim_btn")

    if "sim_seed" not in st.session_state:
        st.session_state.sim_seed = 42

    if run_btn:
        st.session_state.sim_seed = random.randint(100, 99999)
        st.toast(f"Simulation generated with new seed #{st.session_state.sim_seed}")

    # Run Simulation
    loss_rate = sim_loss_pct / 100.0
    sim_data = run_simulation(
        ticks=sim_ticks,
        loss_rate=loss_rate,
        algorithm=sim_algo,
        initial_ssthresh=initial_ssthresh,
        rwnd=sim_rwnd,
        bdp=sim_bdp,
        seed=st.session_state.sim_seed
    )
    df_sim = pd.DataFrame(sim_data)

    # Compact Centered KPIs
    total_losses = int(df_sim["Loss"].sum())
    max_cwnd = df_sim["CongestionWindow"].max()
    avg_effective_w = df_sim["EffectiveWindow"].mean()
    avg_utilization = df_sim["LinkUtilization"].mean()
    flow_throttled_pct = (df_sim["LimitingFactor"] == "Flow Control (rwnd)").mean() * 100.0

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric("Avg Link Utilization", f"{avg_utilization:.1f}%")
    with kpi2:
        st.metric("Avg Effective Window", f"{avg_effective_w:.1f} pkts")
    with kpi3:
        st.metric("Peak cwnd", f"{max_cwnd:.1f} pkts")
    with kpi4:
        st.metric("Flow Throttled", f"{flow_throttled_pct:.1f}%")
    with kpi5:
        st.metric("Loss Events", f"{total_losses} drops")

    # Centered Graph Box
    fig_sim = create_flow_tcp_chart(
        df_sim,
        bdp=sim_bdp,
        rwnd=sim_rwnd,
        title=f"TCP {sim_algo} with Flow Control (rwnd = {sim_rwnd}) & BDP ({sim_bdp} pkts)"
    )
    st.plotly_chart(fig_sim, use_container_width=True)


# ----------------- TAB 2: PROTOCOL BENCHMARK (UNCHANGED ORIGINAL LAYOUT) -----------------
with nav_tab2:
    with st.container(border=True):
        cmp_c1, cmp_c2, cmp_c3, cmp_c4, cmp_c5 = st.columns([2, 2, 2, 2, 1.5], vertical_alignment="bottom")

        with cmp_c1:
            cmp_ticks = st.slider("Duration", 50, 400, 180, 10, key="cmp_ticks")
        with cmp_c2:
            cmp_loss_pct = st.slider("Loss Rate (%)", 0.5, 20.0, 4.0, 0.5, key="cmp_loss")
        with cmp_c3:
            cmp_rwnd = st.slider("rwnd Limit", 10, 80, 45, 5, key="cmp_rwnd")
        with cmp_c4:
            cmp_bdp = st.slider("BDP Capacity", 10, 60, 30, 2, key="cmp_bdp")
        with cmp_c5:
            cmp_btn = st.button("Compare All", key="cmp_run_btn")

    if "cmp_seed" not in st.session_state:
        st.session_state.cmp_seed = 101

    if cmp_btn:
        st.session_state.cmp_seed = random.randint(100, 99999)
        st.toast(f"Benchmark regenerated with seed #{st.session_state.cmp_seed}")

    cmp_loss_rate = cmp_loss_pct / 100.0
    
    tahoe_data = run_simulation(ticks=cmp_ticks, loss_rate=cmp_loss_rate, algorithm="Tahoe", rwnd=cmp_rwnd, bdp=cmp_bdp, seed=st.session_state.cmp_seed)
    reno_data = run_simulation(ticks=cmp_ticks, loss_rate=cmp_loss_rate, algorithm="Reno", rwnd=cmp_rwnd, bdp=cmp_bdp, seed=st.session_state.cmp_seed)
    cubic_data = run_simulation(ticks=cmp_ticks, loss_rate=cmp_loss_rate, algorithm="Cubic", rwnd=cmp_rwnd, bdp=cmp_bdp, seed=st.session_state.cmp_seed)

    df_tahoe = pd.DataFrame(tahoe_data)
    df_reno = pd.DataFrame(reno_data)
    df_cubic = pd.DataFrame(cubic_data)

    tahoe_util = df_tahoe["LinkUtilization"].mean()
    reno_util = df_reno["LinkUtilization"].mean()
    cubic_util = df_cubic["LinkUtilization"].mean()
    j_index = calculate_jains_fairness([df_reno['EffectiveWindow'].mean(), df_cubic['EffectiveWindow'].mean()])

    bk1, bk2, bk3, bk4 = st.columns(4)
    with bk1:
        st.metric("Tahoe Util (1988)", f"{tahoe_util:.1f}%")
    with bk2:
        st.metric("Reno Util (1990)", f"{reno_util:.1f}%")
    with bk3:
        st.metric("Cubic Util (Modern)", f"{cubic_util:.1f}%", delta=f"{cubic_util - reno_util:+.1f}% vs Reno")
    with bk4:
        st.metric("Jain's Fairness Index", f"{j_index:.3f} / 1.0", help="1.0 = Perfect Bandwidth Fairness")

    fig_bench = go.Figure()
    fig_bench.add_trace(go.Scatter(x=df_tahoe["Tick"], y=df_tahoe["EffectiveWindow"], mode="lines", name="TCP Tahoe (1988)", line=dict(color="#f87171", width=1.8)))
    fig_bench.add_trace(go.Scatter(x=df_reno["Tick"], y=df_reno["EffectiveWindow"], mode="lines", name="TCP Reno (1990)", line=dict(color="#34d399", width=2.0)))
    fig_bench.add_trace(go.Scatter(x=df_cubic["Tick"], y=df_cubic["EffectiveWindow"], mode="lines", name="TCP Cubic (Modern)", line=dict(color="#38bdf8", width=2.4)))
    fig_bench.add_trace(go.Scatter(x=[df_tahoe["Tick"].min(), df_tahoe["Tick"].max()], y=[cmp_bdp, cmp_bdp], mode="lines", name="BDP Capacity", line=dict(color="#f43f5e", width=1.6, dash="dot")))

    bench_losses = df_tahoe[df_tahoe["Loss"] == True]
    if not bench_losses.empty:
        fig_bench.add_trace(go.Scatter(x=bench_losses["Tick"], y=[0] * len(bench_losses), mode="markers", name="Shared Drops", marker=dict(symbol="triangle-up", size=7, color="#fbbf24")))

    fig_bench.update_layout(
        title=dict(text="<b>Head-to-Head: TCP Tahoe (1988) vs TCP Reno (1990) vs TCP Cubic (Modern Linux)</b>", x=0.5, font=dict(size=14, color="#f8fafc")),
        xaxis=dict(title="Time (Ticks)", gridcolor="rgba(255, 255, 255, 0.08)", tickfont=dict(size=10, color="#94a3b8")),
        yaxis=dict(title="Effective Window (Packets)", gridcolor="rgba(255, 255, 255, 0.08)", tickfont=dict(size=10, color="#94a3b8")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10, color="#cbd5e1")),
        hovermode="x unified",
        margin=dict(l=35, r=35, t=65, b=25),
        height=365,
        paper_bgcolor="#111827",
        plot_bgcolor="#0b0f19",
        template="plotly_dark"
    )
    st.plotly_chart(fig_bench, use_container_width=True)


# ----------------- TAB 3: EVENT LOG & METRICS (UNCHANGED ORIGINAL LAYOUT) -----------------
with nav_tab3:
    col_filter1, col_filter2 = st.columns([4, 1.2], vertical_alignment="center")
    with col_filter1:
        show_losses_only = st.checkbox("Show only Packet Loss events", value=False)
    with col_filter2:
        csv_data = df_sim.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export CSV",
            data=csv_data,
            file_name=f"tcp_{sim_algo.lower()}_simulation.csv",
            mime="text/csv"
        )

    display_df = df_sim[df_sim["Loss"] == True] if show_losses_only else df_sim

    st.dataframe(
        display_df,
        column_config={
            "Tick": st.column_config.NumberColumn("Tick", format="%d"),
            "CongestionWindow": st.column_config.NumberColumn("cwnd", format="%.2f"),
            "ReceiverWindow": st.column_config.NumberColumn("rwnd", format="%.2f"),
            "EffectiveWindow": st.column_config.NumberColumn("Effective", format="%.2f"),
            "Ssthresh": st.column_config.NumberColumn("ssthresh", format="%.2f"),
            "LinkUtilization": st.column_config.NumberColumn("Util (%)", format="%.1f%%"),
            "LimitingFactor": st.column_config.TextColumn("Constraint"),
            "Event": st.column_config.TextColumn("Event"),
            "Loss": st.column_config.CheckboxColumn("Drop?"),
            "Phase": st.column_config.TextColumn("Phase")
        },
        use_container_width=True,
        height=470
    )


# ----------------- TAB 4: EXTRA ATTRACTIVE 3D NETWORK DIGITAL TWIN -----------------
with nav_tab4:
    with st.container(border=True):
        t3_c1, t3_c2, t3_c3, t3_c4, t3_c5 = st.columns([2, 2.5, 2.5, 2.5, 1.5], vertical_alignment="bottom")
        with t3_c1:
            t3d_algo = st.selectbox("3D Protocol", ["Cubic", "Reno", "Tahoe"], index=0, key="t3d_algo")
        with t3_c2:
            t3d_rwnd = st.slider("3D rwnd Limit", 10, 80, 40, 5, key="t3d_rwnd")
        with t3_c3:
            t3d_bdp = st.slider("3D BDP Pipe Size", 10, 60, 25, 2, key="t3d_bdp")
        with t3_c4:
            t3d_loss = st.slider("3D Drop Rate (%)", 0.5, 15.0, 3.5, 0.5, key="t3d_loss")
        with t3_c5:
            t3d_btn = st.button("Update 3D", key="t3d_btn")

    if "t3d_seed" not in st.session_state:
        st.session_state.t3d_seed = 42

    if t3d_btn:
        st.session_state.t3d_seed = random.randint(100, 99999)
        st.toast(f"3D Digital Twin updated with seed #{st.session_state.t3d_seed}")

    # Run Simulation for 3D state
    sim_data_3d = run_simulation(
        ticks=180,
        loss_rate=t3d_loss / 100.0,
        algorithm=t3d_algo,
        initial_ssthresh=16,
        rwnd=t3d_rwnd,
        bdp=t3d_bdp,
        seed=st.session_state.t3d_seed
    )
    df_3d = pd.DataFrame(sim_data_3d)

    # Metric HUD
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Peak cwnd", f"{df_3d['CongestionWindow'].max():.1f} pkts")
    with k2:
        st.metric("Avg Effective Window", f"{df_3d['EffectiveWindow'].mean():.1f} pkts")
    with k3:
        st.metric("Link Saturation", f"{df_3d['LinkUtilization'].mean():.1f}%")
    with k4:
        st.metric("Buffer Capacity", f"{t3d_bdp} pkts")
    with k5:
        st.metric("Packet Drops", f"{int(df_3d['Loss'].sum())} events")

    # Interactive 3D WebGL Three.js Component
    html_3d = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                overflow: hidden;
                background-color: #0b0f19;
                font-family: monospace;
            }}
            #canvas-container {{
                width: 100%;
                height: 360px;
                position: relative;
                border-radius: 8px;
                border: 1px solid #1f2937;
            }}
            #hud-overlay {{
                position: absolute;
                top: 8px;
                left: 12px;
                color: #38bdf8;
                font-size: 11px;
                line-height: 1.4;
                background: rgba(17, 24, 39, 0.8);
                padding: 5px 10px;
                border-radius: 6px;
                border: 1px solid #374151;
                pointer-events: none;
            }}
            #tip {{
                position: absolute;
                bottom: 8px;
                right: 12px;
                color: #64748b;
                font-size: 10px;
                pointer-events: none;
            }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div id="hud-overlay">
                <b>NETPLUS 3D DIGITAL TWIN</b> | 
                PROTOCOL: <span style="color:#fff">{t3d_algo}</span> | 
                CWND: <span style="color:#38bdf8">{df_3d['CongestionWindow'].max():.1f}</span> | 
                RWND: <span style="color:#c084fc">{t3d_rwnd}</span>
            </div>
            <div id="tip">🖱️ Left Click Drag to Rotate in 360° | Scroll to Zoom</div>
        </div>

        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x0b0f19, 0.035);

            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 6, 18);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(renderer.domElement);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;

            // Lights
            scene.add(new THREE.AmbientLight(0xffffff, 0.6));
            const pLight1 = new THREE.PointLight(0x38bdf8, 2, 20);
            pLight1.position.set(-7, 3, 2);
            scene.add(pLight1);

            const pLight2 = new THREE.PointLight(0xa855f7, 2.5, 20);
            pLight2.position.set(0, 3, 0);
            scene.add(pLight2);

            const pLight3 = new THREE.PointLight(0x10b981, 2, 20);
            pLight3.position.set(7, 3, 2);
            scene.add(pLight3);

            // Ground Grid
            const grid = new THREE.GridHelper(26, 26, 0x1f2937, 0x111827);
            grid.position.y = -2;
            scene.add(grid);

            // 1. Client Sender (Cyan Sphere + Orbital Ring)
            const clientGroup = new THREE.Group();
            clientGroup.position.set(-7, 0, 0);
            const clientMesh = new THREE.Mesh(
                new THREE.SphereGeometry(1.0, 32, 32),
                new THREE.MeshStandardMaterial({{ color: 0x0284c7, metalness: 0.8, roughness: 0.2 }})
            );
            clientGroup.add(clientMesh);
            const ring1 = new THREE.Mesh(
                new THREE.TorusGeometry(1.5, 0.04, 16, 100),
                new THREE.MeshBasicMaterial({{ color: 0x38bdf8, wireframe: true }})
            );
            ring1.rotation.x = Math.PI / 2.5;
            clientGroup.add(ring1);
            scene.add(clientGroup);

            // 2. Router Buffer Cylinder
            const routerGroup = new THREE.Group();
            routerGroup.position.set(0, 0, 0);
            const shellMesh = new THREE.Mesh(
                new THREE.CylinderGeometry(1.3, 1.3, 3.0, 32, 1, true),
                new THREE.MeshPhysicalMaterial({{ color: 0x475569, transparent: true, opacity: 0.35, roughness: 0.1 }})
            );
            routerGroup.add(shellMesh);
            const bufRatio = Math.min(1.0, Math.max(0.15, {df_3d['CongestionWindow'].max()} / Math.max(1, {t3d_bdp})));
            const innerMesh = new THREE.Mesh(
                new THREE.CylinderGeometry(1.15, 1.15, 2.8 * bufRatio, 32),
                new THREE.MeshStandardMaterial({{ color: 0x9333ea, emissive: 0x6b21a8, roughness: 0.3 }})
            );
            innerMesh.position.y = -1.4 + (1.4 * bufRatio);
            routerGroup.add(innerMesh);
            scene.add(routerGroup);

            // 3. Server Receiver (Emerald Octahedron)
            const serverGroup = new THREE.Group();
            serverGroup.position.set(7, 0, 0);
            const serverMesh = new THREE.Mesh(
                new THREE.OctahedronGeometry(1.1),
                new THREE.MeshStandardMaterial({{ color: 0x059669, metalness: 0.8, roughness: 0.2 }})
            );
            serverGroup.add(serverMesh);
            const ring2 = new THREE.Mesh(
                new THREE.TorusGeometry(1.5, 0.04, 16, 100),
                new THREE.MeshBasicMaterial({{ color: 0x34d399, wireframe: true }})
            );
            ring2.rotation.y = Math.PI / 3;
            serverGroup.add(ring2);
            scene.add(serverGroup);

            // 4. Data Conduit Fiber Splines
            const curve1 = new THREE.CatmullRomCurve3([
                new THREE.Vector3(-7, 0, 0),
                new THREE.Vector3(-3.5, 1.2, 0),
                new THREE.Vector3(0, 0, 0)
            ]);
            const curve2 = new THREE.CatmullRomCurve3([
                new THREE.Vector3(0, 0, 0),
                new THREE.Vector3(3.5, 1.2, 0),
                new THREE.Vector3(7, 0, 0)
            ]);
            const conduitMat = new THREE.MeshBasicMaterial({{ color: 0x1e293b, wireframe: true }});
            scene.add(new THREE.Mesh(new THREE.TubeGeometry(curve1, 30, 0.12, 8, false), conduitMat));
            scene.add(new THREE.Mesh(new THREE.TubeGeometry(curve2, 30, 0.12, 8, false), conduitMat));

            // 5. 3D Packets In Flight
            const packets = [];
            const pktGeo = new THREE.SphereGeometry(0.18, 16, 16);
            const pMat1 = new THREE.MeshBasicMaterial({{ color: 0x38bdf8 }});
            const pMat2 = new THREE.MeshBasicMaterial({{ color: 0x34d399 }});

            for (let i = 0; i < 30; i++) {{
                const isFirst = i % 2 === 0;
                const pMesh = new THREE.Mesh(pktGeo, isFirst ? pMat1 : pMat2);
                pMesh.userData = {{
                    curve: isFirst ? curve1 : curve2,
                    progress: Math.random(),
                    speed: 0.007 + Math.random() * 0.005
                }};
                scene.add(pMesh);
                packets.push(pMesh);
            }}

            // Render Loop
            function animate() {{
                requestAnimationFrame(animate);
                ring1.rotation.z += 0.015;
                clientMesh.rotation.y += 0.01;
                routerGroup.rotation.y += 0.008;
                ring2.rotation.x += 0.015;
                serverMesh.rotation.y -= 0.012;

                packets.forEach(pkt => {{
                    pkt.userData.progress += pkt.userData.speed;
                    if (pkt.userData.progress > 1) pkt.userData.progress = 0;
                    pkt.position.copy(pkt.userData.curve.getPoint(pkt.userData.progress));
                }});

                controls.update();
                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_3d, height=365, scrolling=False)


# ----------------- TAB 5: EXTRA ATTRACTIVE 3D STATE TRAJECTORY SPACE (PLOTLY 3D) -----------------
with nav_tab5:
    with st.container(border=True):
        tc1, tc2, tc3, tc4 = st.columns([2.5, 2.5, 2.5, 2], vertical_alignment="bottom")
        with tc1:
            traj_algo = st.selectbox("Trajectory Protocol", ["Cubic", "Reno", "Tahoe"], index=0, key="traj_algo")
        with tc2:
            traj_ticks = st.slider("Timeline Ticks", 50, 300, 160, 10, key="traj_ticks")
        with tc3:
            traj_loss = st.slider("Drop Probability (%)", 0.5, 15.0, 4.0, 0.5, key="traj_loss")
        with tc4:
            traj_btn = st.button("Render 3D Space", key="traj_btn")

    if "traj_seed" not in st.session_state:
        st.session_state.traj_seed = 42

    if traj_btn:
        st.session_state.traj_seed = random.randint(100, 99999)
        st.toast(f"3D Space refreshed with seed #{st.session_state.traj_seed}")

    df_traj = pd.DataFrame(run_simulation(
        ticks=traj_ticks,
        loss_rate=traj_loss / 100.0,
        algorithm=traj_algo,
        rwnd=40,
        bdp=25,
        seed=st.session_state.traj_seed
    ))

    # 3D Coordinate Ribbon Chart
    fig_3d = go.Figure()

    # 3D Line Ribbon
    fig_3d.add_trace(go.Scatter3d(
        x=df_traj["Tick"],
        y=df_traj["Ssthresh"],
        z=df_traj["CongestionWindow"],
        mode="lines",
        name=f"TCP {traj_algo} 3D Trajectory",
        line=dict(
            color=df_traj["CongestionWindow"],
            colorscale="Viridis",
            width=5
        ),
        hovertemplate="<b>Tick:</b> %{x}<br><b>ssthresh:</b> %{y:.1f}<br><b>cwnd:</b> %{z:.2f}<extra></extra>"
    ))

    # 3D Loss Points
    loss_3d = df_traj[df_traj["Loss"] == True]
    if not loss_3d.empty:
        fig_3d.add_trace(go.Scatter3d(
            x=loss_3d["Tick"],
            y=loss_3d["Ssthresh"],
            z=loss_3d["CongestionWindow"],
            mode="markers",
            name="3D Loss Events",
            marker=dict(size=5, color="#ef4444", symbol="diamond"),
            hovertemplate="<b>3D Loss Point:</b> Tick %{x}<extra></extra>"
        ))

    fig_3d.update_layout(
        title=dict(
            text=f"<b>Rotatable 3D State-Space Trajectory: Time × ssthresh × cwnd ({traj_algo})</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=14, color="#f8fafc")
        ),
        scene=dict(
            xaxis=dict(title="Time (Ticks)", gridcolor="#1e293b", backgroundcolor="#0b0f19", showbackground=True),
            yaxis=dict(title="ssthresh Threshold", gridcolor="#1e293b", backgroundcolor="#0b0f19", showbackground=True),
            zaxis=dict(title="cwnd Window Size", gridcolor="#1e293b", backgroundcolor="#0b0f19", showbackground=True),
            camera=dict(eye=dict(x=1.6, y=1.5, z=1.2))
        ),
        margin=dict(l=0, r=0, t=35, b=0),
        height=385,
        paper_bgcolor="#111827",
        template="plotly_dark"
    )
    st.plotly_chart(fig_3d, use_container_width=True)