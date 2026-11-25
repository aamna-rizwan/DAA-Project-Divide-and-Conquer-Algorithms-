import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import sys

# Ensure src/ directory is accessible
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "src"))

from helpers import load_closest_pair_dataset, load_karatsuba_dataset
from closest_pair import solve_closest_pair
from karatsuba import solve_karatsuba

# Page Configuration
st.set_page_config(
    page_title="DAA Project — Algorithm Visualizer & Benchmarks",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E88E5; }
    .sub-header { font-size: 1.1rem; color: #555555; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">DAA Algorithm Visualizer & Benchmark Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Divide & Conquer: Closest Pair of Points (O(n log n)) and Karatsuba Multiplication (O(n^1.585))</div>', unsafe_allow_html=True)
st.write("---")

DATASETS_DIR = BASE_DIR / "datasets"
RESULTS_DIR = BASE_DIR / "results"

tab1, tab2, tab3 = st.tabs([
    "📍 Closest Pair of Points",
    "🔢 Karatsuba Integer Multiplication",
    "📊 Empirical Benchmark Graphs"
])

# ==========================================
# TAB 1: CLOSEST PAIR OF POINTS
# ==========================================
with tab1:
    st.header("Algorithm 1: Closest Pair of Points")

    cp_files = sorted([f.name for f in DATASETS_DIR.glob("cp*.txt")])
    selected_cp = st.selectbox("Select Input Dataset", ["-- Select File --"] + cp_files, key="cp_select")

    if selected_cp != "-- Select File --":
        pts = load_closest_pair_dataset(DATASETS_DIR / selected_cp)
        n_pts = len(pts)
        st.info(f"Loaded File: **{selected_cp}** | Total Points (n): **{n_pts:,}**")

        is_large = n_pts >= 100000
        if is_large:
            st.warning("⚠️ **Large Input Dataset Detected**: Displaying summarized final results and execution time.")

        if st.button("Run Closest Pair Algorithm", type="primary", key="run_cp_btn"):
            with st.spinner(f"Executing Closest Pair on {n_pts:,} points..."):
                res = solve_closest_pair(pts, capture_trace=(n_pts <= 500))
            st.session_state["cp_res"] = res
            st.session_state["cp_file"] = selected_cp
            trace_len = len(res.get("trace") or [])
            if trace_len > 0:
                st.session_state["cp_step_slider"] = trace_len
            else:
                st.session_state.pop("cp_step_slider", None)

        cp_res = st.session_state.get("cp_res")
        if cp_res is not None and st.session_state.get("cp_file") == selected_cp:
            # Display Key Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Point 1", f"({cp_res['point1'][0]:.2f}, {cp_res['point1'][1]:.2f})")
            m2.metric("Point 2", f"({cp_res['point2'][0]:.2f}, {cp_res['point2'][1]:.2f})")
            m3.metric("Minimum Distance (δ)", f"{cp_res['distance']:.6f}")
            m4.metric("Execution Time", f"{cp_res['time']:.6f} s")

            # Plot Visualizations
            st.subheader("Visual Output")
            fig, ax = plt.subplots(figsize=(9, 5))

            if n_pts <= 2000:
                xs, ys = zip(*pts)
                ax.scatter(xs, ys, c='#1f77b4', s=20, alpha=0.6, label='Input Points')
            else:
                sample_pts = pts[:2000]
                xs, ys = zip(*sample_pts)
                ax.scatter(xs, ys, c='#1f77b4', s=10, alpha=0.3, label=f'Point Sample (First 2,000 of {n_pts:,})')

            p1, p2 = cp_res["point1"], cp_res["point2"]
            ax.scatter([p1[0], p2[0]], [p1[1], p2[1]], c='red', s=80, zorder=5, label='Closest Pair')
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r--', lw=2, zorder=4)

            ax.set_title(f"Closest Pair Visualization — {selected_cp} (n={n_pts:,})")
            ax.set_xlabel("X Coordinate")
            ax.set_ylabel("Y Coordinate")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig)
            plt.close(fig)

            # Step-by-Step Execution for Small Inputs
            trace_steps = cp_res.get("trace") or []
            if trace_steps and n_pts <= 500:
                st.write("---")
                st.subheader("🔍 Step-by-Step Divide & Conquer Execution Trace")
                st.write("Below is the step-by-step breakdown of how the algorithm divided the space and combined results:")

                total_steps = len(trace_steps)
                if "cp_step_slider" not in st.session_state or not (1 <= st.session_state["cp_step_slider"] <= total_steps):
                    st.session_state["cp_step_slider"] = total_steps

                step_idx = st.slider(
                    "Navigate Recursive Merge Steps",
                    min_value=1,
                    max_value=total_steps,
                    key="cp_step_slider"
                )

                step_data = trace_steps[step_idx - 1]
                st.write(f"**Step {step_idx} of {total_steps}** | Type: `{step_data['type']}`")

                if step_data['type'] == 'base_case':
                    st.json({
                        "Base Case Points": step_data["points"],
                        "Calculated Closest Pair": step_data["closest"],
                        "Distance": step_data["dist"]
                    })
                elif step_data['type'] == 'recursive_merge':
                    st.json({
                        "Median Dividing Line (x)": step_data["mid_x"],
                        "Delta (min left/right distance)": step_data["delta"],
                        "Strip Points Count": len(step_data["strip"]),
                        "Best Pair Found": step_data["best_pair"],
                        "Updated Minimum Distance": step_data["dist"]
                    })


# ==========================================
# TAB 2: KARATSUBA MULTIPLICATION
# ==========================================
with tab2:
    st.header("Algorithm 2: Karatsuba Integer Multiplication")

    im_files = sorted([f.name for f in DATASETS_DIR.glob("im*.txt")])
    selected_im = st.selectbox("Select Input Dataset", ["-- Select File --"] + im_files, key="im_select")

    if selected_im != "-- Select File --":
        num1, num2 = load_karatsuba_dataset(DATASETS_DIR / selected_im)
        len1, len2 = len(num1), len(num2)
        st.info(f"Loaded File: **{selected_im}** | Operand Digits: **{len1:,} × {len2:,}**")

        is_large_im = max(len1, len2) >= 100000
        if is_large_im:
            st.warning("⚠️ **Large Input Dataset Detected**: Showing running time and truncated output preview.")

        if st.button("Run Karatsuba Multiplication", type="primary", key="run_im_btn"):
            with st.spinner(f"Computing product of {len1:,} x {len2:,} digit numbers..."):
                res = solve_karatsuba(num1, num2, max_digits=100000, capture_trace=(max(len1, len2) <= 300))
            st.session_state["im_res"] = res
            st.session_state["im_file"] = selected_im

        im_res = st.session_state.get("im_res")
        if im_res is not None and st.session_state.get("im_file") == selected_im:
            if im_res.get("limited"):
                st.error(f"Execution Limit Reached: {im_res['reason']}")
            else:
                prod = im_res["product"]
                prod_len = len(prod)

                # Metrics
                km1, km2, km3 = st.columns(3)
                km1.metric("Input Digits (A)", f"{len1:,}")
                km2.metric("Input Digits (B)", f"{len2:,}")
                km3.metric("Execution Time", f"{im_res['time']:.6f} s")

                st.metric("Product Digit Length", f"{prod_len:,}")

                # Large vs Small Output Handling
                st.subheader("Calculated Product Output")
                if prod_len > 3000:
                    st.write("**Product Preview (First 1,000 and Last 1,000 digits):**")
                    preview_text = f"{prod[:1000]}\n\n... [{prod_len - 2000:,} digits truncated for rendering speed] ...\n\n{prod[-1000:]}"
                    st.code(preview_text, language="text")

                    st.download_button(
                        label="📥 Download Full Product Text File (.txt)",
                        data=prod,
                        file_name=f"{selected_im}_product.txt",
                        mime="text/plain"
                    )
                else:
                    st.text_area("Full Product Output", prod, height=180)

                # Step-by-Step Recursive Working for Small Inputs
                if im_res.get("trace") and max(len1, len2) <= 300:
                    st.write("---")
                    st.subheader("🔍 Step-by-Step Karatsuba Decomposition Trace")
                    st.write("Below is the recursive breakdown showing how numbers are split into High/Low parts and combined:")

                    for step in im_res["trace"]:
                        with st.expander(f"Recursion Level {step['depth']}: Multiplying {len(step['x'])} digits × {len(step['y'])} digits"):
                            c1, c2 = st.columns(2)
                            with c1:
                                st.write("**Operand Splits:**")
                                st.json({
                                    "Number 1 High (a)": step['high1'],
                                    "Number 1 Low (b)": step['low1'],
                                    "Number 2 High (c)": step['high2'],
                                    "Number 2 Low (d)": step['low2']
                                })
                            with c2:
                                st.write("**Intermediate Products:**")
                                st.json({
                                    "z2 (a * c)": step['z2'],
                                    "z0 (b * d)": step['z0'],
                                    "z1 ((a+b)(c+d) - z2 - z0)": step['z1'],
                                    "Combined Result": step['result']
                                })


# ==========================================
# TAB 3: BENCHMARK GRAPHS & COMPLEXITY
# ==========================================
with tab3:
    st.header("Empirical Benchmark Results & Time Complexity Analysis")
    st.write("This tab displays performance graphs generated across the benchmark datasets.")

    cp_csv = RESULTS_DIR / "cp_results.csv"
    im_csv = RESULTS_DIR / "im_results.csv"

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("1. Closest Pair: O(n log n)")
        if cp_csv.exists():
            df_cp = pd.read_csv(cp_csv)
            st.dataframe(df_cp, use_container_width=True)

            fig_cp, ax_cp = plt.subplots(figsize=(6, 4))
            ax_cp.plot(df_cp["Points"], df_cp["Time (s)"], 'o-', color='#1E88E5', label='Measured Time')
            ax_cp.set_xlabel("Number of Points (n)")
            ax_cp.set_ylabel("Execution Time (seconds)")
            ax_cp.set_title("Closest Pair Benchmark Curve")
            ax_cp.grid(True, linestyle='--')
            ax_cp.legend()
            st.pyplot(fig_cp)
            plt.close(fig_cp)
        else:
            st.info("Run `python src/benchmark.py` in your terminal to generate Closest Pair benchmark data.")

    with col_g2:
        st.subheader("2. Karatsuba: O(n^1.585)")
        if im_csv.exists():
            df_im = pd.read_csv(im_csv)
            st.dataframe(df_im, use_container_width=True)

            fig_im, ax_im = plt.subplots(figsize=(6, 4))
            ax_im.plot(df_im["Digits A"], df_im["Time (s)"], 's-', color='#D81B60', label='Measured Time')
            ax_im.set_xlabel("Number of Digits (n)")
            ax_im.set_ylabel("Execution Time (seconds)")
            ax_im.set_title("Karatsuba Multiplication Benchmark Curve")
            ax_im.grid(True, linestyle='--')
            ax_im.legend()
            st.pyplot(fig_im)
            plt.close(fig_im)
        else:
            st.info("Run `python src/benchmark.py` in your terminal to generate Karatsuba benchmark data.")


