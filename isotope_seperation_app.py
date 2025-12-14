import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

st.set_page_config(page_title="Isotope Separation Physics Demo", layout="wide")
st.title("Isotope Separation Physics Demo (Educational)")
st.markdown("**Educational/Theoretical Only** | Demonstrates physics of isotope separation methods. Highly simplified models.")

def value_function(x):
    x = np.clip(x, 1e-10, 0.99999999)
    return (2 * x - 1) * np.log(x / (1 - x))

def swu_calc(product_kg, x_p, x_f, x_t):
    feed = product_kg * (x_p - x_t) / (x_f - x_t)
    swu = product_kg * (value_function(x_p) - ((x_p - x_t)/(x_p - x_f)) * value_function(x_t) -
                        ((x_f - x_t)/(x_p - x_f)) * value_function(x_f))
    return feed, swu

def stages_needed(alpha, x_f, x_p, x_t= None):
    if x_t is None:
        x_t = x_f / 10  # Rough default
    if alpha <= 1:
        return np.inf
    # Approximate ideal cascade stages (enriching + stripping)
    n_enrich = np.log(x_p / x_f) / np.log(alpha)
    n_strip = np.log(x_f / x_t) / np.log(alpha)
    return n_enrich + n_strip

# Predefined examples
examples = {
    "Uranium (U-235/238) - Centrifuge": {"m_light": 235, "m_heavy": 238, "compound": "UF6", "m_add": 6*19, "x_f": 0.00711, "method": "centrifuge"},
    "Uranium (U-235/238) - Gaseous Diffusion": {"m_light": 235, "m_heavy": 238, "compound": "UF6", "m_add": 6*19, "x_f": 0.00711, "method": "diffusion"},
    "Deuterium (Heavy Water Historical)": {"m_light": 2, "m_heavy": 1, "compound": "H2S exchange", "x_f": 0.00015, "method": "chemical", "alpha_cold": 2.33},
    "Lithium-6/7 (Fusion Fuel Example)": {"m_light": 6, "m_heavy": 7, "compound": "Note: Primarily chemical (COLEX)", "x_f": 0.075, "method": "note"},
}

st.header("Generalized Binary Isotope Separation")
example = st.selectbox("Choose Example", list(examples.keys()))
data = examples[example]

col1, col2 = st.columns(2)
with col1:
    x_p = st.slider("Target Light Isotope Fraction (%)", 1.0, 99.0, 4.5 if "Uranium" in example else 30.0) / 100
    product_kg = st.number_input("Product Mass (kg or equivalent)", 1, 100000, 1000)
with col2:
    if data["method"] == "centrifuge":
        alpha = st.slider("Separation Factor α (typical 1.2–1.5)", 1.01, 2.0, 1.4, 0.05)
    elif data["method"] == "diffusion":
        alpha = 1.0043  # Fixed for UF6
        st.info("Gaseous Diffusion α ≈ 1.0043 (fixed for UF6)")
    elif data["method"] == "chemical":
        st.info("Girdler-Sulfide: α ≈ 2.33 (cold) / 1.82 (hot)")
        alpha = 2.0  # Average effective
    else:
        alpha = 1.05
        st.info("Lithium-6 primarily via chemical exchange (historical COLEX, α ≈ 1.05). Not gaseous.")

if st.button("Calculate"):
    x_f = data["x_f"]
    x_t = st.slider("Tails Fraction (%)", 0.01, x_f*100, 0.25 if "Uranium" in example else x_f*10) / 100
    
    feed, swu = swu_calc(product_kg, x_p, x_f, x_t)
    n_stages = stages_needed(alpha, x_f, x_p, x_t)
    
    st.write(f"**Results for {x_p*100:.1f}% enrichment:**")
    st.write(f"Feed required: {feed:.0f} units")
    st.write(f"Separative Work (SWU): {swu:.0f}")
    st.write(f"Approx. stages needed: {n_stages:.0f} {'(centrifuge)' if data['method']=='centrifuge' else '(diffusion – very high!)'}")
    
    if "Diffusion" in example:
        st.warning("Gaseous diffusion needs ~4000+ stages vs. ~50–100 for modern centrifuges – far less efficient!")
    
    # Visualization: enrichment profile (log scale stages)
    assays = np.logspace(np.log10(x_t), np.log10(x_p), int(n_stages) if n_stages < 500 else 200)
    stages_plot = np.arange(len(assays))
    
    fig, ax = plt.subplots()
    ax.semilogy(stages_plot, assays * 100)
    ax.set_xlabel("Stage Number")
    ax.set_ylabel("Light Isotope %")
    ax.set_title("Simplified Cascade Enrichment Profile")
    st.pyplot(fig)

st.markdown("**Note on Lithium for Fusion:** Li-6 enrichment historically used mercury-based chemical exchange (COLEX, banned due to toxicity). Modern research seeks greener alternatives. This demo shows why gaseous methods are impractical for light elements.")

st.markdown("Run: `streamlit run isotope_separation_app.py`")

