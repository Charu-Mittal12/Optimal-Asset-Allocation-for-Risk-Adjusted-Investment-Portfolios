# 📊 Portfolio Optimization Dashboard

An interactive **Streamlit-based Portfolio Optimization Tool** that integrates asset management, data fetching, optimization, and portfolio analysis into one seamless interface.  

This project provides a modular, extensible framework for exploring various **optimization algorithms** (like Mean-Variance and Covariance Shrinkage) and visualizing their results interactively.

---

## 🚀 Demo Video
🎥 **[Watch the Demo](https://your-demo-video-link.com)**  
*(Replace this link with your uploaded video on Google Drive, YouTube, or GitHub release.)*

---

## 🧩 Project Overview

The project follows a modular, object-oriented architecture for maintainability and scalability.

### 📁 Directory Structure
```bash
assets/
├── asset_interface.py
├── asset_factory.py
├── asset_collection.py
├── stock.py
├── bond.py
├── etf.py
└── crypto.py

data_fetcher/
├── data_fetcher_interface.py
├── data_factory.py
├── yahoo_fetcher.py
├── fred_fetcher.py
└── binance_fetcher.py

optimizer/
├── optimizer_interface.py
├── optimizer_factory.py
├── mean_variance_optimizer.py
└── covariance_optimizer.py

portfolio/
├── manager.py
└── rebalance.py

portfolio_analyzer/
├── analyzer_interface.py
├── portfolio_analyzer.py
├── return_calculator.py
└── volatility_calculator.py

visualization/
└── streamlit_dashboard.py

app.py
requirements.txt


## ⚙️ Installation

# Clone this repository
git clone https://github.com/your-username/portfolio-optimization-dashboard.git
cd portfolio-optimization-dashboard

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

# Install Required Dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py



