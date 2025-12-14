# Isotope Separation Physics Demo (Educational)

**Educational & Theoretical Physics Tool Only**

This interactive demo illustrates the fundamental physics of binary isotope separation using simplified models. It supports:
- Gas centrifuge and gaseous diffusion for uranium (U-235/U-238)
- Historical heavy water (deuterium) production via chemical exchange
- Lithium-6/7 separation challenges (fusion fuel context – shown for educational comparison only)

**Important Note:** All models are highly simplified and use publicly available textbook formulas. This tool is strictly for understanding separation physics and efficiency differences between methods.

## Features

- Generalized separative work unit (SWU) calculations
- Comparison of separation factors (α) and required stages
- Visual enrichment cascade profiles
- Pre-loaded examples: uranium centrifuge vs. diffusion, heavy water, lithium-6

## Quick Start

```bash
git clone https://github.com/yourusername/isotope-separation-demo.git
cd isotope-separation-demo
pip install -r requirements.txt
streamlit run app.py

The app will open in your browser.Examples & InsightsGaseous diffusion requires ~4,000 stages for LEU vs. ~50–100 for modern centrifuges
Chemical exchange (e.g., historical Girdler-Sulfide for deuterium) achieves higher α per stage
Lithium-6 enrichment historically used toxic mercury-based COLEX process (now banned) – illustrates why fusion fuel separation remains challenging

Disclaimer

This is an educational physics demonstration only. It is not intended for, nor capable of, supporting real-world isotope separation activities.LicenseMIT License – see LICENSE for details.

