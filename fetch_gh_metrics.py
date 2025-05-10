"""
GitHub Releases Metrics Viewer

This app allows users to enter a GitHub account and repository name, fetches all releases via
the GitHub API (with pagination support), and displays metrics such as total downloads and 
release count. It also shows a version-wise breakdown of download totals in an interactive table.

Author: Askushi
Date: 2025-05-09
"""

from ctypes import alignment
import requests
import streamlit as st
import pandas as pd

### Uncomment this block if you don't need pagination
# @st.cache_data(ttl=300)
# def fetch_releases(account, repo):
#     url = f"https://api.github.com/repos/{account}/{repo}/releases"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

#Fetch data with pagination
@st.cache_data(ttl=300)
def fetch_releases(account, repo):
    all_releases = []
    per_page = 100
    page = 1

    while True:
        url = f"https://api.github.com/repos/{account}/{repo}/releases"
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        releases = response.json()

        if not releases:
            break

        all_releases.extend(releases)
        page += 1

    return all_releases


def process_data(releases):
    version_downloads = {}
    total_downloads = 0

    for release in releases:
        version = release["tag_name"]
        version_total = sum(asset["download_count"] for asset in release.get("assets", []))
        total_downloads += version_total
        version_downloads[version] = version_total

    df = pd.DataFrame([
        {"Version": v, "Total Downloads": d}
        for v, d in version_downloads.items()
    ])
    df.sort_values(by="Version", ascending=False, inplace=True)
    return df, total_downloads, len(version_downloads)

# Streamlit App
# Create two columns for the header
col1, col2 = st.columns([1, 5])  # Adjust the ratios for spacing

# Place the image in the first column
with col1:
    st.image("https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png",width=100)

# Place the title in the second column
with col2:
    st.title("GitHub Releases")
    st.subheader("Download Metrics")


# Input Form
with st.form("repo_form"):
    github_account = st.text_input("GitHub Account", placeholder="github_account")
    repo = st.text_input("Repository Name", placeholder="repo_name")
    submitted = st.form_submit_button("Fetch Releases")

if submitted:
    try:
        releases = fetch_releases(github_account, repo)
        df, total_downloads, total_releases = process_data(releases)

        col1, col2 = st.columns(2)
        col1.metric("Total Downloads", total_downloads)
        col2.metric("Total Releases", total_releases)

        st.dataframe(df, use_container_width=True, hide_index=True)

    except requests.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
