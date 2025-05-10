
# GitHub Releases Metrics Viewer

This Streamlit app fetches and visualizes GitHub release metrics for any public repository.

![demo](gh_metrics_demo.gif)

## 📋 Features

- 🔍 Input any GitHub account and repository
- 📦 Fetches all releases (handles GitHub API pagination)
- 📈 Displays:
  - Total number of downloads
  - Total number of releases
- 📊 Interactive table:
  - Version-wise download counts
  - Sortable, filterable, and color-coded using AgGrid

## 🚀 Getting Started

### 1. Clone this repository or copy the script

### 2. Install dependencies

```bash
pip install streamlit requests pandas streamlit-aggrid
```

### 3. Run the app

```bash
streamlit run fetch_gh_metrics_documented.py
```

## 🛠️ Configuration

When the app starts, enter:
- GitHub account name (e.g. `adaptivescale`)
- Repository name (e.g. `rosetta`)

Click **Fetch Releases** to retrieve and display data.

## 📌 Notes

- The app uses GitHub’s REST API with pagination (100 items per page).
- Caching is enabled to reduce API calls (`ttl=300` seconds).
- Supports only public repositories.

## 📄 License

MIT License
