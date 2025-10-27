# 🛡️ PhishGuard – AI-Powered Phishing URL Detection System

> **End-to-End Machine Learning Project** built with **FastAPI**, **MongoDB**, and **scikit-learn**, capable of detecting phishing websites through automated feature extraction, model training, and real-time prediction APIs.

---

## 🚀 Overview

PhishGuard is a **machine learning–based phishing detection system** that analyzes 30+ web and network-level features to classify websites as **Legitimate** or **Phishing**.  
It supports both **batch predictions (CSV upload)** and **real-time predictions via API** or **browser extension**.

---

## 🧩 Key Features

✅ **Fully Automated ML Pipeline** – data ingestion → preprocessing → model training → evaluation → deployment  
✅ **Batch Prediction** – upload a CSV of URLs for classification  
✅ **Real-Time URL Prediction API** – detect phishing instantly using `/predict_url`  
✅ **FastAPI Backend** – blazing-fast REST API with CORS support  
✅ **MongoDB Integration** – store ingestion and training metadata  
✅ **WHOIS & SSL Feature Extraction** – analyzes domain age, HTTPS, redirection, subdomains, etc. 

---

## 🧠 Tech Stack

| Layer | Technology |
|:------|:------------|
| **Backend** | FastAPI |
| **Modeling / ML** | scikit-learn, pandas, numpy |
| **Database** | MongoDB |
| **Environment** | Python 3.10+, dotenv |
| **Deployment (optional)** | Render / Railway / Deta Space |

---

## independent fertures

having_IP_Address, URL_Length, Shortining_Service, having_At_Symbol, 
double_slash_redirecting, Prefix_Suffix, having_Sub_Domain, SSLfinal_State, 
Domain_registeration_length, Favicon, port, HTTPS_token, Request_URL, 
URL_of_Anchor, Links_in_tags, SFH, Submitting_to_email, Abnormal_URL, Redirect, 
on_mouseover, RightClick, popUpWidnow, Iframe, age_of_domain, DNSRecord, 
web_traffic, Page_Rank, Google_Index, Links_pointing_to_page, Statistical_report

