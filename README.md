# Project Overview

This project involves extracting and analyzing insights from 10-K filings using various tools and methodologies.

## Tasks and Tools Overview

### Understanding 10-K Filings and Company Tickers

- **Concept**: Familiarized with 10-K filings and company ticker symbols to uniquely identify publicly traded shares.

### Exploring SEC-EDGAR

- **Tool**: Used the SEC-EDGAR system to access financial filings.

### Downloading and Formatting Filings

- **Library**: Utilized the `sec_edgar_downloader` library to download 10-K filings.
- **Formatting**: Applied HTML formatting to make documents human-readable.

### Organizing and Renaming Files

- **Scripting**: Developed a Python script to organize and rename HTML files by year.

### Introduction to RAG (Retrieval Augmented Generation)

- **Technique**: Implemented RAG to retrieve insights from documents unseen by the LLM, aiming to build a chatbot-like interface.

### Experimenting with Models

- **Models**: Evaluated multiple models, including OpenAI, HuggingFace, and local models (LLaMa2, LLaMa3, Phi3, Mistral), and Anthropic AI's Claude-3-Opus.

### Front-end Development with Streamlit

- **Framework**: Used Streamlit for its Python integration and multi-page application support, managing session states and variables.

## Tasks Breakdown

### Task 1.1: Data Retrieval

- **Companies**: Apple, Microsoft, Visa, Nvidia.
- **Process**: Downloaded and processed 10-K filings, organized HTML files, and created a FAISS database for similarity searches.

```python
ticker = input("Enter company ticker: ")

from sec_edgar_downloader import Downloader

dl = Downloader("MyCompanyName", "my_mail@email_provider.com")

dl.get("10-K", ticker, after="1995-01-01", before="2023-12-31", download_details=True)
