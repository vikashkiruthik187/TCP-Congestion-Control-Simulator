import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components
import importlib
import random
import io
from datetime import datetime
import engine
importlib.reload(engine)
from engine import run_simulation, calculate_jains_fairness, simulate_cloud_gaming, simulate_multi_flow

# Page Configuration - High Performance Wide Layout
st.set_page_config(
    page_title="TCP Congestion Control Simulator & Telemetry Lab",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Dark Glassmorphism Styling
st.markdown("""
<style>
    /* Streamlit Header clean-up */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 0.8rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1440px !important;
        margin: 0 auto;
    }
    
    /* Header Section */
    .main-header {
        text-align: center;
        padding: 0.1rem 0 0.5rem 0 !important;
        margin-bottom: 0.35rem !important;
        border-bottom: 1px solid rgba(56, 189, 248, 0.15);
    }
    .main-title {
        font-size: 2.15rem !important;
        font-weight: 900 !important;
        letter-spacing: 0.8px !important;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        display: inline-block !important;
        margin-bottom: 0.1rem !important;
    }
    .main-subtitle {
        font-size: 0.84rem;
        color: #94a3b8;
        font-weight: 500;
        margin-top: -2px;
    }

    /* Tabs Styling - Cyber Glass */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.6rem !important;
        justify-content: center;
        border-bottom: 1px solid #1e293b !important;
        margin-bottom: 0.45rem !important;
        background: rgba(15, 23, 42, 0.6);
        padding: 4px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
        padding: 0.38rem 0.9rem !important;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important;
        background: rgba(56, 189, 248, 0.12) !important;
        border-bottom-color: #38bdf8 !important;
    }

    /* Controls Container */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(56, 189, 248, 0.2) !important;
        background-color: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(10px);
        border-radius: 10px !important;
        padding: 0.45rem 0.8rem !important;
        margin-bottom: 0.35rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }
    
    label[data-testid="stWidgetLabel"] p {
        font-size: 0.74rem !important;
        font-weight: 600 !important;
        color: #cbd5e1 !important;
        margin-bottom: 0.1rem !important;
    }

    /* Compact Metric Cards with Glass Neon Trim */
    [data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.22) !important;
        border-radius: 8px !important;
        padding: 0.35rem 0.65rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.72rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 800 !important;
        font-size: 1.25rem !important;
    }

    /* Primary Action Buttons */
    div.stButton > button:first-child {
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
        font-size: 0.82rem;
        border-radius: 6px;
        padding: 0.4rem 0.6rem;
        border: 1px solid #38bdf8;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35);
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%);
        border-color: #7dd3fc;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
    }

    /* Download Buttons */
    div.stDownloadButton > button {
        width: 100%;
        background: rgba(30, 41, 59, 0.9);
        color: #38bdf8;
        font-weight: 600;
        font-size: 0.78rem;
        border-radius: 6px;
        padding: 0.35rem 0.6rem;
        border: 1px solid rgba(56, 189, 248, 0.4);
        transition: all 0.2s;
    }
    div.stDownloadButton > button:hover {
        background: rgba(56, 189, 248, 0.15);
        color: #ffffff;
        border-color: #38bdf8;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- TOP HEADER -----------------
st.markdown("""
<div class="main-header">
    <div class="main-title">TCP Congestion Control Simulator & Telemetry Lab</div>
    <div class="main-subtitle">
        High-Performance Transport Modeling, 3D Topology Visualization, Multi-Flow Competition & Bufferbloat Lab
    </div>
</div>
""", unsafe_allow_html=True)

# Helper function to generate clean Dark-themed 2D Plotly charts
def create_flow_tcp_chart(df, bdp, rwnd, title="TCP Dynamics Over Time"):
    fig = go.Figure()

    # Congestion Window (cwnd)
    fig.add_trace(go.Scatter(
        x=df["Tick"],
        y=df["CongestionWindow"],
        mode="lines",
        name="cwnd",
        line=dict(color="#38bdf8", width=2.4),
        hovertemplate="<b>Tick:</b> %{x}<br><b>cwnd:</b> %{y:.2f} pkts<extra></extra>"
    ))

    # Effective Window: min(cwnd, rwnd)
    fig.add_trace(go.Scatter(
        x=df["Tick"],
        y=df["EffectiveWindow"],
        mode="lines",
        name="Effective [min(cwnd, rwnd)]",
        line=dict(color="#34d399", width=2.0),
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
        paper_bgcolor="#0f172a",
        plot_bgcolor="#090d16",
        template="plotly_dark"
    )
    return fig

# ----------------- TABS SETUP -----------------
nav_dash, nav_tab1, nav_tab2, nav_tab_multi, nav_tab_gaming = st.tabs([
    "Overview & 3D Topology",
    "Single-Flow Dynamics",
    "Protocol Benchmark (Tahoe · Reno · Cubic · BBR)",
    "Multi-Flow Bottleneck & Fairness",
    "Real-Time Latency & Bufferbloat"
])

# ==============================================================================
# TAB 1: EXECUTIVE DASHBOARD & 3D TOPOLOGY
# ==============================================================================
with nav_dash:
    # High-level Executive KPI Ribbon
    ek1, ek2, ek3, ek4 = st.columns(4)
    with ek1:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 8px; padding: 0.55rem 0.8rem;">
            <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Active Protocol Models</div>
            <div style="font-size: 1.22rem; font-weight: 800; color: #f8fafc; margin-top: 1px;">4 Algorithms</div>
            <div style="font-size: 0.7rem; color: #38bdf8;">Tahoe, Reno, Cubic, Google BBR</div>
        </div>
        """, unsafe_allow_html=True)
    with ek2:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(52, 211, 153, 0.25); border-radius: 8px; padding: 0.55rem 0.8rem;">
            <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Bottleneck Capacity</div>
            <div style="font-size: 1.22rem; font-weight: 800; color: #f8fafc; margin-top: 1px;">45 pkts / tick</div>
            <div style="font-size: 0.7rem; color: #34d399;">Physical BDP Pipe Limit</div>
        </div>
        """, unsafe_allow_html=True)
    with ek3:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(251, 191, 36, 0.25); border-radius: 8px; padding: 0.55rem 0.8rem;">
            <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Propagation Latency</div>
            <div style="font-size: 1.22rem; font-weight: 800; color: #f8fafc; margin-top: 1px;">15.0 ms</div>
            <div style="font-size: 0.7rem; color: #fbbf24;">Minimum Physical RTT</div>
        </div>
        """, unsafe_allow_html=True)
    with ek4:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(192, 132, 252, 0.25); border-radius: 8px; padding: 0.55rem 0.8rem;">
            <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Queueing Architecture</div>
            <div style="font-size: 1.22rem; font-weight: 800; color: #f8fafc; margin-top: 1px;">DropTail & Paced</div>
            <div style="font-size: 0.7rem; color: #c084fc;">FIFO vs BBR Zero Bloat</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.45rem; margin-bottom: 0.3rem;">
        <div style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; display: flex; align-items: center; gap: 8px;">
            <span>Interactive 3D Transport Pipeline & Network Hardware Model</span>
            <span style="font-size: 0.72rem; color: #38bdf8; background: rgba(56, 189, 248, 0.15); padding: 2px 7px; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.3);">
                🖱️ Click & Drag to Rotate in 3D
            </span>
        </div>
        <div style="font-size: 0.75rem; color: #94a3b8;">
            <b>Topology:</b> Edge Sender Host ➔ Bottleneck FIFO Router ➔ Destination Receiver
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3D WebGL / Three.js Canvas Component with centered framing
    html_3d_topology = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { margin: 0; padding: 0; overflow: hidden; background: #090d16; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
            #canvas-container { width: 100%; height: 440px; position: relative; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.25); background: radial-gradient(circle at 50% 50%, #0f172a 0%, #090d16 100%); cursor: grab; }
            #canvas-container:active { cursor: grabbing; }
            #hud-overlay { position: absolute; top: 12px; left: 14px; pointer-events: none; }
            .hud-card { background: rgba(15, 23, 42, 0.88); backdrop-filter: blur(8px); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 6px; padding: 6px 12px; font-size: 11px; color: #cbd5e1; }
            .badge-title { font-weight: 800; color: #38bdf8; letter-spacing: 0.5px; }
            #legend-bar { position: absolute; bottom: 10px; right: 14px; background: rgba(15, 23, 42, 0.88); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 6px; padding: 5px 12px; font-size: 11px; color: #cbd5e1; display: flex; gap: 14px; }
            .dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; margin-right: 5px; }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div id="hud-overlay">
                <div class="hud-card">
                    <div class="badge-title">📡 3D TRANSPORT PIPELINE ACTIVE</div>
                    <div><b>Inflight Pipe:</b> 45 pkts | <b>Router Buffer:</b> 30 pkts | <b>Min RTT:</b> 15ms</div>
                </div>
            </div>
            <div id="legend-bar">
                <span><span class="dot" style="background:#38bdf8;"></span>Host A (Sender)</span>
                <span><span class="dot" style="background:#fbbf24;"></span>Bottleneck Router</span>
                <span><span class="dot" style="background:#34d399;"></span>Host B (Receiver)</span>
                <span><span class="dot" style="background:#818cf8;"></span>Flying Packets</span>
            </div>
        </div>

        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x090d16, 0.028);

            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 8.5, 20);
            camera.lookAt(0, 0, 0);

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(renderer.domElement);

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
            scene.add(ambientLight);
            const dirLight = new THREE.DirectionalLight(0x38bdf8, 1.4);
            dirLight.position.set(5, 18, 12);
            scene.add(dirLight);

            // Grid Ground
            const gridHelper = new THREE.GridHelper(40, 32, 0x334155, 0x0f172a);
            gridHelper.position.y = -2.8;
            scene.add(gridHelper);

            // Helper to build 3D Host Server Rack
            function createHost(x, color) {
                const group = new THREE.Group();
                const geom = new THREE.BoxGeometry(2.8, 5.0, 2.2);
                const mat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.3, metalness: 0.8 });
                const mesh = new THREE.Mesh(geom, mat);
                group.add(mesh);

                // LED lights
                for (let i = 0; i < 5; i++) {
                    const ledGeo = new THREE.BoxGeometry(2.1, 0.28, 0.1);
                    const ledMat = new THREE.MeshBasicMaterial({ color: color });
                    const led = new THREE.Mesh(ledGeo, ledMat);
                    led.position.set(0, -1.6 + (i * 0.8), 1.12);
                    group.add(led);
                }

                // Pedestal ring
                const ringGeo = new THREE.RingGeometry(2.0, 2.5, 32);
                const ringMat = new THREE.MeshBasicMaterial({ color: color, side: THREE.DoubleSide });
                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.x = Math.PI / 2;
                ring.position.y = -2.48;
                group.add(ring);

                group.position.x = x;
                group.position.y = 0;
                scene.add(group);
                return group;
            }

            // Router with rotating holographic radar
            function createRouter(x) {
                const group = new THREE.Group();
                const geom = new THREE.CylinderGeometry(2.4, 2.8, 2.6, 16);
                const mat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4, metalness: 0.85 });
                const mesh = new THREE.Mesh(geom, mat);
                group.add(mesh);

                // Buffer Tank (Glass Center)
                const tankGeo = new THREE.CylinderGeometry(1.4, 1.4, 1.9, 16);
                const tankMat = new THREE.MeshBasicMaterial({ color: 0xfbbf24, wireframe: true });
                const tank = new THREE.Mesh(tankGeo, tankMat);
                tank.position.y = 2.1;
                group.add(tank);

                // Holographic Rings
                const ringGeo = new THREE.TorusGeometry(3.2, 0.07, 8, 36);
                const ringMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b });
                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.x = Math.PI / 2.3;
                group.add(ring);

                group.position.set(x, 0, 0);
                scene.add(group);
                return { group, ring };
            }

            const sender = createHost(-9, 0x38bdf8);
            const routerObj = createRouter(0);
            const receiver = createHost(9, 0x34d399);

            // Connecting Data Pipes (Fiber Conduits)
            function createConduit(x1, x2) {
                const curve = new THREE.LineCurve3(new THREE.Vector3(x1, -0.9, 0), new THREE.Vector3(x2, -0.9, 0));
                const geom = new THREE.TubeGeometry(curve, 20, 0.22, 8, false);
                const mat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.5, metalness: 0.7 });
                const mesh = new THREE.Mesh(geom, mat);
                scene.add(mesh);
            }
            createConduit(-9, 0);
            createConduit(0, 9);

            // 3D Moving Packets
            const packets = [];
            const pktGeo = new THREE.SphereGeometry(0.32, 12, 12);
            const pktMat = new THREE.MeshBasicMaterial({ color: 0x818cf8 });

            for (let i = 0; i < 20; i++) {
                const pkt = new THREE.Mesh(pktGeo, pktMat.clone());
                pkt.position.set(-9 + (i * 0.9), -0.9, (Math.random() - 0.5) * 0.3);
                pkt.userData = { speed: 0.09 + Math.random() * 0.03 };
                scene.add(pkt);
                packets.push(pkt);
            }

            // Mouse Interactive Rotation
            let isDragging = false;
            let prevMouseX = 0;
            let prevMouseY = 0;
            let targetRotY = 0;
            let targetRotX = 0.38;

            container.addEventListener('mousedown', (e) => {
                isDragging = true;
                prevMouseX = e.clientX;
                prevMouseY = e.clientY;
            });
            window.addEventListener('mouseup', () => { isDragging = false; });
            window.addEventListener('mousemove', (e) => {
                if (isDragging) {
                    const deltaX = e.clientX - prevMouseX;
                    const deltaY = e.clientY - prevMouseY;
                    targetRotY += deltaX * 0.007;
                    targetRotX = Math.max(0.12, Math.min(1.15, targetRotX + deltaY * 0.005));
                    prevMouseX = e.clientX;
                    prevMouseY = e.clientY;
                }
            });

            function animate() {
                requestAnimationFrame(animate);

                // Smooth camera rotation
                camera.position.x = 20 * Math.sin(targetRotY) * Math.cos(targetRotX);
                camera.position.z = 20 * Math.cos(targetRotY) * Math.cos(targetRotX);
                camera.position.y = 20 * Math.sin(targetRotX);
                camera.lookAt(0, 0, 0);

                // Router animation
                routerObj.ring.rotation.z += 0.025;

                // Move packets along the pipeline
                packets.forEach(p => {
                    p.position.x += p.userData.speed;
                    if (p.position.x > 9) {
                        p.position.x = -9;
                    }
                    if (p.position.x < 0) {
                        p.material.color.setHex(0x38bdf8);
                    } else {
                        p.material.color.setHex(0x34d399);
                    }
                });

                renderer.render(scene, camera);
            }
            animate();

            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });
        </script>
    </body>
    </html>
    """
    components.html(html_3d_topology, height=450, scrolling=False)

# ==============================================================================
# TAB 2: SINGLE SIMULATION
# ==============================================================================
with nav_tab1:
    with st.container(border=True):
        c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 1.8, 1.8, 1.8, 1.8, 1.2, 1.3], vertical_alignment="bottom")

        with c1:
            sim_algo = st.selectbox("Algorithm", ["Cubic", "BBR", "Reno", "Tahoe"], index=0, key="t1_algo")
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
            run_btn = st.button("Run Sim", key="run_sim_btn")

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

    # Export toolbar for Tab 1
    exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 2])
    with exp_col1:
        csv_sim = df_sim.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV Data", csv_sim, f"tcp_{sim_algo}_trace.csv", "text/csv")
    with exp_col2:
        report_md = f"""# TCP Congestion Control Experiment Report
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Protocol:** TCP {sim_algo}
**Duration:** {sim_ticks} ticks | **Loss Rate:** {sim_loss_pct}% | **rwnd:** {sim_rwnd} pkts | **BDP:** {sim_bdp} pkts

## Quantitative Telemetry Results:
- **Average Link Utilization:** {avg_utilization:.2f}%
- **Average Effective Window:** {avg_effective_w:.2f} packets
- **Peak Congestion Window (cwnd):** {max_cwnd:.2f} packets
- **Flow Control Throttled Time:** {flow_throttled_pct:.1f}%
- **Total Packet Drop Events:** {total_losses} drops

## Protocol Analysis:
In this simulation, TCP {sim_algo} operated under a discrete-event network environment.
The effective transmission window was bounded by `min(cwnd, rwnd)`.
"""
        st.download_button("📄 Download Lab Report", report_md, f"TCP_{sim_algo}_Lab_Report.md", "text/markdown")

# ==============================================================================
# TAB 3: PROTOCOL BENCHMARK (TAHOE vs RENO vs CUBIC vs BBR)
# ==============================================================================
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
            cmp_btn = st.button("Compare All 4", key="cmp_run_btn")

    if "cmp_seed" not in st.session_state:
        st.session_state.cmp_seed = 101

    if cmp_btn:
        st.session_state.cmp_seed = random.randint(100, 99999)
        st.toast(f"Benchmark regenerated with seed #{st.session_state.cmp_seed}")

    cmp_loss_rate = cmp_loss_pct / 100.0
    
    tahoe_data = run_simulation(ticks=cmp_ticks, loss_rate=cmp_loss_rate, algorithm="Tahoe", rwnd=cmp_rwnd, bdp=cmp_bdp, seed=st.session_state.cmp_seed)
    reno_data = run_simulation(ticks=cmp_ticks, loss_rate=cmp_loss_rate, algorithm="Reno", rwnd=cmp_rwnd, bdp=cmp_bdp, seed=st.session_state.cmp_seed)
    cubic_data = run_simulation(ticks=cmp_ticks, loss_rate=cmp_loss_rate, algorithm="Cubic", rwnd=cmp_rwnd, bdp=cmp_bdp, seed=st.session_state.cmp_seed)
    bbr_data = run_simulation(ticks=cmp_ticks, loss_rate=cmp_loss_rate, algorithm="BBR", rwnd=cmp_rwnd, bdp=cmp_bdp, seed=st.session_state.cmp_seed)

    df_tahoe = pd.DataFrame(tahoe_data)
    df_reno = pd.DataFrame(reno_data)
    df_cubic = pd.DataFrame(cubic_data)
    df_bbr = pd.DataFrame(bbr_data)

    tahoe_util = df_tahoe["LinkUtilization"].mean()
    reno_util = df_reno["LinkUtilization"].mean()
    cubic_util = df_cubic["LinkUtilization"].mean()
    bbr_util = df_bbr["LinkUtilization"].mean()
    j_index = calculate_jains_fairness([df_reno['EffectiveWindow'].mean(), df_cubic['EffectiveWindow'].mean(), df_bbr['EffectiveWindow'].mean()])

    bk1, bk2, bk3, bk4, bk5 = st.columns(5)
    with bk1:
        st.metric("Tahoe Util (1988)", f"{tahoe_util:.1f}%")
    with bk2:
        st.metric("Reno Util (1990)", f"{reno_util:.1f}%")
    with bk3:
        st.metric("Cubic Util (Linux)", f"{cubic_util:.1f}%", delta=f"{cubic_util - reno_util:+.1f}% vs Reno")
    with bk4:
        st.metric("Google BBR Util", f"{bbr_util:.1f}%", delta=f"{bbr_util - cubic_util:+.1f}% vs Cubic")
    with bk5:
        st.metric("Jain's Fairness Index", f"{j_index:.3f} / 1.0", help="1.0 = Perfect Bandwidth Fairness")

    fig_bench = go.Figure()
    fig_bench.add_trace(go.Scatter(x=df_tahoe["Tick"], y=df_tahoe["EffectiveWindow"], mode="lines", name="TCP Tahoe (1988)", line=dict(color="#f87171", width=1.6)))
    fig_bench.add_trace(go.Scatter(x=df_reno["Tick"], y=df_reno["EffectiveWindow"], mode="lines", name="TCP Reno (1990)", line=dict(color="#fbbf24", width=1.8)))
    fig_bench.add_trace(go.Scatter(x=df_cubic["Tick"], y=df_cubic["EffectiveWindow"], mode="lines", name="TCP Cubic (Modern)", line=dict(color="#38bdf8", width=2.2)))
    fig_bench.add_trace(go.Scatter(x=df_bbr["Tick"], y=df_bbr["EffectiveWindow"], mode="lines", name="Google BBR (Model-Based)", line=dict(color="#34d399", width=2.4)))
    fig_bench.add_trace(go.Scatter(x=[df_tahoe["Tick"].min(), df_tahoe["Tick"].max()], y=[cmp_bdp, cmp_bdp], mode="lines", name="BDP Capacity", line=dict(color="#f43f5e", width=1.6, dash="dot")))

    bench_losses = df_tahoe[df_tahoe["Loss"] == True]
    if not bench_losses.empty:
        fig_bench.add_trace(go.Scatter(x=bench_losses["Tick"], y=[0] * len(bench_losses), mode="markers", name="Shared Drops", marker=dict(symbol="triangle-up", size=7, color="#ef4444")))

    fig_bench.update_layout(
        title=dict(text="<b>Head-to-Head: TCP Tahoe (1988) vs TCP Reno (1990) vs TCP Cubic (Modern Linux) vs Google BBR</b>", x=0.5, font=dict(size=13, color="#f8fafc")),
        xaxis=dict(title="Time (Ticks)", gridcolor="rgba(255, 255, 255, 0.08)", tickfont=dict(size=10, color="#94a3b8")),
        yaxis=dict(title="Effective Window (Packets)", gridcolor="rgba(255, 255, 255, 0.08)", tickfont=dict(size=10, color="#94a3b8")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10, color="#cbd5e1")),
        hovermode="x unified",
        margin=dict(l=35, r=35, t=65, b=25),
        height=365,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#090d16",
        template="plotly_dark"
    )
    st.plotly_chart(fig_bench, use_container_width=True)

# ==============================================================================
# TAB 4: MULTI-FLOW BOTTLENECK & FAIRNESS LAB
# ==============================================================================
with nav_tab_multi:
    with st.container(border=True):
        mf_c1, mf_c2, mf_c3, mf_c4, mf_c5 = st.columns([1.8, 1.8, 1.8, 1.8, 1.2], vertical_alignment="bottom")
        
        with mf_c1:
            num_flows_sel = st.slider("Competing Flows", min_value=2, max_value=5, value=3, step=1, key="mf_num_flows")
        with mf_c2:
            comp_mode = st.selectbox("Flow Preset", ["Mixed (Cubic vs Reno vs BBR)", "All TCP Cubic", "All TCP Reno"], index=0, key="mf_preset")
        with mf_c3:
            shared_bottleneck = st.slider("Bottleneck Capacity", 20, 80, 45, 5, key="mf_capacity")
        with mf_c4:
            router_buffer_size = st.slider("Router Buffer", 10, 50, 25, 5, key="mf_buffer")
        with mf_c5:
            mf_run_btn = st.button("Simulate", key="mf_btn")

    if "mf_seed" not in st.session_state:
        st.session_state.mf_seed = 777

    if mf_run_btn:
        st.session_state.mf_seed = random.randint(100, 99999)
        st.toast(f"Multi-flow competition re-simulated #{st.session_state.mf_seed}")

    if "Mixed" in comp_mode:
        preset_algos = ["Cubic", "Reno", "BBR", "Tahoe"]
    elif "All TCP Cubic" in comp_mode:
        preset_algos = ["Cubic"] * num_flows_sel
    else:
        preset_algos = ["Reno"] * num_flows_sel

    mf_results = simulate_multi_flow(
        num_flows=num_flows_sel,
        ticks=180,
        bottleneck_capacity=float(shared_bottleneck),
        buffer_size=float(router_buffer_size),
        flow_algos=preset_algos,
        seed=st.session_state.mf_seed
    )
    df_mf = pd.DataFrame(mf_results)

    avg_fairness = df_mf["JainsFairness"].mean()
    max_queue_seen = df_mf["RouterQueue"].max()
    queue_overflow_pct = (df_mf["RouterQueue"] >= router_buffer_size).mean() * 100.0

    mk1, mk2, mk3, mk4 = st.columns(4)
    with mk1:
        st.metric("Average Jain's Fairness", f"{avg_fairness:.3f} / 1.0", help="1.0 = Perfectly equal bandwidth distribution")
    with mk2:
        st.metric("Peak Router Queue", f"{max_queue_seen:.1f} pkts", delta=f"{max_queue_seen - router_buffer_size:+.1f} Buffer Overflow" if max_queue_seen > router_buffer_size else "Under Buffer Limit")
    with mk3:
        st.metric("Buffer Overflow Time", f"{queue_overflow_pct:.1f}%")
    with mk4:
        st.metric("Bottleneck Link Cap", f"{shared_bottleneck} pkts/tick")

    # Multi-flow interactive graph
    fig_mf = go.Figure()
    palette = ["#38bdf8", "#fbbf24", "#34d399", "#f87171", "#c084fc"]

    for i in range(num_flows_sel):
        col_cwnd = f"Flow{i+1}_cwnd"
        col_algo = df_mf[f"Flow{i+1}_algo"].iloc[0]
        fig_mf.add_trace(go.Scatter(
            x=df_mf["Tick"],
            y=df_mf[col_cwnd],
            mode="lines",
            name=f"Flow #{i+1} ({col_algo})",
            line=dict(color=palette[i % len(palette)], width=2.0)
        ))

    # Shared Bottleneck & Queue lines
    fig_mf.add_trace(go.Scatter(
        x=[df_mf["Tick"].min(), df_mf["Tick"].max()],
        y=[shared_bottleneck, shared_bottleneck],
        mode="lines",
        name="Bottleneck Capacity",
        line=dict(color="#f43f5e", width=1.8, dash="dot")
    ))
    fig_mf.add_trace(go.Scatter(
        x=df_mf["Tick"],
        y=df_mf["RouterQueue"],
        mode="lines",
        name="Router Queue Depth",
        line=dict(color="#94a3b8", width=1.4, dash="dash")
    ))

    fig_mf.update_layout(
        title=dict(text=f"<b>Multi-Flow Competition: {num_flows_sel} TCP Senders Sharing a {shared_bottleneck} pkts Bottleneck</b>", x=0.5, font=dict(size=13, color="#f8fafc")),
        xaxis=dict(title="Time (Simulation Ticks)", gridcolor="rgba(255, 255, 255, 0.08)", tickfont=dict(size=10, color="#94a3b8")),
        yaxis=dict(title="Window Size & Queue (Packets)", gridcolor="rgba(255, 255, 255, 0.08)", tickfont=dict(size=10, color="#94a3b8")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10, color="#cbd5e1")),
        hovermode="x unified",
        margin=dict(l=35, r=35, t=65, b=25),
        height=365,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#090d16",
        template="plotly_dark"
    )
    st.plotly_chart(fig_mf, use_container_width=True)

# ==============================================================================
# TAB 5: CLOUD GAMING & BUFFERBLOAT KILLER
# ==============================================================================
with nav_tab_gaming:
    with st.container(border=True):
        cg_col1, cg_col2, cg_col3, cg_col4, cg_col5 = st.columns([3.4, 2.0, 2.0, 2.0, 1.3], vertical_alignment="bottom")
        
        with cg_col1:
            cc_selection = st.radio(
                "Congestion Control Status",
                [
                    "❌ Without Congestion Control (Bufferbloat: High Ping & Lag)",
                    "✅ With Google BBR / Paced CC (Zero Queue Bloat: 15ms Smooth)"
                ],
                index=1,
                key="cg_mode_radio"
            )
        with cg_col2:
            cg_base_ping = st.slider("Base Fiber Ping (ms)", 10, 60, 15, 5, key="cg_base_ping")
        with cg_col3:
            cg_bandwidth = st.slider("Link Bandwidth (Mbps)", 20, 100, 50, 10, key="cg_bandwidth")
        with cg_col4:
            cg_ticks = st.slider("Stream Duration", 60, 240, 120, 20, key="cg_ticks")
        with cg_col5:
            cg_run_btn = st.button("Run Stream", key="cg_run_btn")

    if "cg_sim_seed" not in st.session_state:
        st.session_state.cg_sim_seed = 42

    if cg_run_btn:
        st.session_state.cg_sim_seed = random.randint(100, 99999)
        st.toast(f"Cloud gaming stream re-simulated with seed #{st.session_state.cg_sim_seed}")

    is_smart_cc = "✅" in cc_selection

    # Run the Cloud Gaming & Bufferbloat simulation
    cg_results = simulate_cloud_gaming(
        ticks=cg_ticks,
        base_rtt_ms=float(cg_base_ping),
        bandwidth_mbps=float(cg_bandwidth),
        enable_smart_cc=is_smart_cc,
        seed=st.session_state.cg_sim_seed
    )
    df_gaming = pd.DataFrame(cg_results)

    # Real-time KPIs
    last_ping = df_gaming["TotalPing_ms"].iloc[-1]
    avg_ping = df_gaming["TotalPing_ms"].mean()
    avg_queue_delay = df_gaming["QueueDelay_ms"].mean()
    max_queue_pkts = df_gaming["QueuedPackets"].max()
    fps_current = df_gaming["EffectiveFPS"].iloc[-1]
    user_exp = df_gaming["UserExperience"].iloc[-1]

    gk1, gk2, gk3, gk4, gk5 = st.columns(5)
    with gk1:
        st.metric(
            "Total Gaming Ping",
            f"{avg_ping:.1f} ms",
            delta=f"{avg_ping - cg_base_ping:+.1f} ms (Bufferbloat)" if avg_ping > cg_base_ping else "0.0 ms Queue Lag",
            delta_color="inverse"
        )
    with gk2:
        st.metric(
            "Router Queue Delay",
            f"{avg_queue_delay:.1f} ms",
            delta="Buffer Empty" if avg_queue_delay < 5 else "Buffer Overflowing",
            delta_color="inverse"
        )
    with gk3:
        st.metric(
            "Stream FPS",
            f"{fps_current} FPS",
            delta="Smooth 60 FPS" if fps_current >= 55 else f"-{60 - fps_current} FPS Stutter",
            delta_color="normal"
        )
    with gk4:
        st.metric("Router Queue Bloat", f"{max_queue_pkts:.1f} pkts", help="Excess packets queuing in intermediate router FIFO buffer")
    with gk5:
        st.metric("Player Experience", user_exp)

    # Split row: Interactive Cloud Gaming Canvas Stream (Left) + Latency Breakdown Chart (Right)
    game_col_left, game_col_right = st.columns([1.15, 1.0])

    with game_col_left:
        # Dynamic Interactive HTML5 / Canvas Cloud Gaming Stream Simulator
        display_ping = int(avg_ping)
        display_queue = int(max_queue_pkts)
        display_lag = int(avg_queue_delay)

        html_game = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: #090d16;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
                    overflow: hidden;
                    color: #f8fafc;
                }}
                #game-box {{
                    position: relative;
                    width: 100%;
                    height: 340px;
                    border-radius: 8px;
                    border: 1px solid rgba(56, 189, 248, 0.25);
                    background: radial-gradient(circle at 50% 30%, #172554 0%, #090d16 100%);
                    overflow: hidden;
                    outline: none;
                }}
                #canvas {{
                    width: 100%;
                    height: 100%;
                    display: block;
                }}
                .hud-badge {{
                    position: absolute;
                    top: 10px;
                    left: 12px;
                    background: rgba(15, 23, 42, 0.90);
                    border: 1px solid {"#10b981" if is_smart_cc else "#ef4444"};
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 11px;
                    line-height: 1.4;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                }}
                .status-title {{
                    font-weight: 800;
                    letter-spacing: 0.5px;
                    color: {"#34d399" if is_smart_cc else "#f87171"};
                }}
                #controls-bar {{
                    position: absolute;
                    bottom: 8px;
                    left: 12px;
                    right: 12px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background: rgba(15, 23, 42, 0.90);
                    border: 1px solid #334155;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 11px;
                }}
                .steer-btn {{
                    background: {"#0284c7" if is_smart_cc else "#dc2626"};
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    padding: 5px 12px;
                    font-weight: 700;
                    font-size: 11px;
                    cursor: pointer;
                    transition: all 0.15s;
                }}
                .steer-btn:active {{
                    transform: scale(0.94);
                }}
                #alert-toast {{
                    position: absolute;
                    top: 10px;
                    right: 12px;
                    font-size: 11px;
                    font-weight: 700;
                    padding: 5px 10px;
                    border-radius: 6px;
                    background: {"rgba(16, 185, 129, 0.2)" if is_smart_cc else "rgba(239, 68, 68, 0.2)"};
                    border: 1px solid {"#10b981" if is_smart_cc else "#ef4444"};
                    color: {"#34d399" if is_smart_cc else "#f87171"};
                }}
            </style>
        </head>
        <body>
            <div id="game-box" tabindex="0">
                <canvas id="canvas"></canvas>
                <div class="hud-badge">
                    <div class="status-title">
                        {"⚡ GOOGLE BBR / BDP-PACED CONGESTION CONTROL" if is_smart_cc else "⚠️ SEVERE BUFFERBLOAT (UNCONTROLLED TCP)"}
                    </div>
                    <div>
                        <b>Ping:</b> <span style="color:{"#34d399" if is_smart_cc else "#f87171"}; font-weight:800;">{display_ping} ms</span> | 
                        <b>Buffer Delay:</b> <span style="color:{"#38bdf8" if is_smart_cc else "#f87171"};">{display_lag} ms</span> | 
                        <b>Queue Bloat:</b> {display_queue} pkts
                    </div>
                </div>

                <div id="alert-toast">
                    {"60 FPS | 15ms Response" if is_smart_cc else "Stuttering | ~280ms Input Lag"}
                </div>

                <div id="controls-bar">
                    <div>
                        <span>🎮 <b>Steer Test:</b></span>
                        <button class="steer-btn" onclick="steer(-1)">◀ Steer Left</button>
                        <button class="steer-btn" onclick="steer(1)">Steer Right ▶</button>
                    </div>
                    <div style="color: #cbd5e1; font-size: 10px;">
                        {"Click canvas & press ⬅️ / ➡️ keys or click buttons" if is_smart_cc else "Notice delayed reaction (~280ms lag)"}
                    </div>
                </div>
            </div>

            <script>
                const canvas = document.getElementById('canvas');
                const ctx = canvas.getContext('2d');
                const isSmart = {"true" if is_smart_cc else "false"};

                function resize() {{
                    canvas.width = canvas.parentElement.clientWidth;
                    canvas.height = canvas.parentElement.clientHeight;
                }}
                window.addEventListener('resize', resize);
                resize();

                let carX = canvas.width / 2;
                let targetX = carX;
                let pendingSteers = [];
                let stars = [];

                for (let i = 0; i < 45; i++) {{
                    stars.push({{
                        x: Math.random() * canvas.width,
                        y: Math.random() * (canvas.height - 40),
                        z: Math.random() * 4 + 1
                    }});
                }}

                function steer(direction) {{
                    const now = performance.now();
                    const delay = isSmart ? 15 : 280; // Bufferbloat lag delay in ms
                    pendingSteers.push({{
                        target: carX + (direction * 48),
                        execTime: now + delay
                    }});
                }}

                // Focus on click
                document.getElementById('game-box').addEventListener('click', () => {{
                    document.getElementById('game-box').focus();
                }});

                // Keyboard listeners
                window.addEventListener('keydown', (e) => {{
                    if (e.key === 'ArrowLeft' || e.key === 'a') steer(-1);
                    if (e.key === 'ArrowRight' || e.key === 'd') steer(1);
                }});

                function draw() {{
                    if (!isSmart && Math.random() < 0.08) {{
                        requestAnimationFrame(draw); // Skip frame to simulate freeze
                        return;
                    }}

                    const now = performance.now();
                    while (pendingSteers.length > 0 && pendingSteers[0].execTime <= now) {{
                        const act = pendingSteers.shift();
                        targetX = Math.max(50, Math.min(canvas.width - 50, act.target));
                    }}

                    carX += (targetX - carX) * (isSmart ? 0.25 : 0.08);

                    ctx.fillStyle = '#090d16';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    const horizonY = canvas.height * 0.32;
                    const centerX = canvas.width / 2;

                    ctx.strokeStyle = isSmart ? 'rgba(56, 189, 248, 0.25)' : 'rgba(239, 68, 68, 0.25)';
                    ctx.lineWidth = 1.5;
                    for (let x = -3; x <= 3; x++) {{
                        ctx.beginPath();
                        ctx.moveTo(centerX + (x * 20), horizonY);
                        ctx.lineTo(centerX + (x * 160), canvas.height - 35);
                        ctx.stroke();
                    }}

                    ctx.fillStyle = isSmart ? '#38bdf8' : '#f87171';
                    stars.forEach(s => {{
                        s.y += s.z * (isSmart ? 2.5 : 1.2);
                        if (s.y > canvas.height - 40) {{
                            s.y = horizonY;
                            s.x = Math.random() * canvas.width;
                        }}
                        ctx.fillRect(s.x, s.y, s.z, s.z);
                    }});

                    const carY = canvas.height - 70;
                    ctx.save();
                    ctx.translate(carX, carY);

                    // Car shadow
                    ctx.fillStyle = 'rgba(0,0,0,0.5)';
                    ctx.beginPath();
                    ctx.ellipse(0, 16, 28, 8, 0, 0, Math.PI * 2);
                    ctx.fill();

                    // Thruster glow
                    const glowGrad = ctx.createRadialGradient(0, 10, 2, 0, 18, 18);
                    glowGrad.addColorStop(0, isSmart ? '#38bdf8' : '#ef4444');
                    glowGrad.addColorStop(1, 'transparent');
                    ctx.fillStyle = glowGrad;
                    ctx.beginPath();
                    ctx.arc(0, 12, 16, 0, Math.PI * 2);
                    ctx.fill();

                    // Cyber Car Body
                    ctx.fillStyle = isSmart ? '#0284c7' : '#991b1b';
                    ctx.strokeStyle = isSmart ? '#38bdf8' : '#f87171';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(-20, 10);
                    ctx.lineTo(-14, -18);
                    ctx.lineTo(14, -18);
                    ctx.lineTo(20, 10);
                    ctx.closePath();
                    ctx.fill();
                    ctx.stroke();

                    // Windshield
                    ctx.fillStyle = isSmart ? '#67e8f9' : '#fca5a5';
                    ctx.beginPath();
                    ctx.moveTo(-10, -5);
                    ctx.lineTo(-7, -15);
                    ctx.lineTo(7, -15);
                    ctx.lineTo(10, -5);
                    ctx.closePath();
                    ctx.fill();
                    ctx.stroke();

                    ctx.restore();

                    // Glitch line artifacts on Bufferbloat
                    if (!isSmart && Math.random() < 0.25) {{
                        ctx.fillStyle = 'rgba(239, 68, 68, 0.15)';
                        const glitchY = Math.random() * canvas.height;
                        ctx.fillRect(0, glitchY, canvas.width, Math.random() * 12 + 2);
                    }}

                    requestAnimationFrame(draw);
                }}
                draw();
            </script>
        </body>
        </html>
        """
        components.html(html_game, height=350, scrolling=False)

    with game_col_right:
        # Plotly Latency Breakdown Chart: Base Physical Delay vs Router Bufferbloat Delay
        fig_gaming = go.Figure()

        # Base Physical Ping Area (Green / Blue)
        fig_gaming.add_trace(go.Scatter(
            x=df_gaming["Tick"],
            y=df_gaming["BasePing_ms"],
            mode="lines",
            name="Physical Fiber Ping (RTT)",
            line=dict(color="#10b981", width=1.5),
            stackgroup="one",
            fillcolor="rgba(16, 185, 129, 0.25)",
            hovertemplate="<b>Base Ping:</b> %{y:.1f} ms<extra></extra>"
        ))

        # Bufferbloat Queuing Delay (Red / Orange)
        fig_gaming.add_trace(go.Scatter(
            x=df_gaming["Tick"],
            y=df_gaming["QueueDelay_ms"],
            mode="lines",
            name="Bufferbloat Queuing Delay",
            line=dict(color="#ef4444" if not is_smart_cc else "#38bdf8", width=2.0),
            stackgroup="one",
            fillcolor="rgba(239, 68, 68, 0.4)" if not is_smart_cc else "rgba(56, 189, 248, 0.1)",
            hovertemplate="<b>Queue Lag:</b> +%{y:.1f} ms<extra></extra>"
        ))

        # Total Gaming Latency Line
        fig_gaming.add_trace(go.Scatter(
            x=df_gaming["Tick"],
            y=df_gaming["TotalPing_ms"],
            mode="lines",
            name="Total Gaming Ping",
            line=dict(color="#fbbf24", width=2.2, dash="dot"),
            hovertemplate="<b>Total Latency:</b> %{y:.1f} ms<extra></extra>"
        ))

        fig_gaming.update_layout(
            title=dict(
                text=f"<b>Latency Breakdown: Base Ping vs Bufferbloat Queue Delay</b>",
                x=0.5,
                font=dict(size=13, color="#f8fafc")
            ),
            xaxis=dict(title="Stream Timeline (Ticks)", gridcolor="rgba(255, 255, 255, 0.08)", tickfont=dict(size=9, color="#94a3b8")),
            yaxis=dict(title="Latency (Milliseconds)", gridcolor="rgba(255, 255, 255, 0.08)", tickfont=dict(size=9, color="#94a3b8")),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=9, color="#cbd5e1")),
            hovermode="x unified",
            margin=dict(l=30, r=30, t=55, b=25),
            height=350,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#090d16",
            template="plotly_dark"
        )
        st.plotly_chart(fig_gaming, use_container_width=True)