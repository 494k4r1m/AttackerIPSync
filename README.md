# 📡 QRadar & MISP Integration/Automation 🛡️

This repository provides a simple yet powerful **Python-based integration** between **QRadar** and **MISP (Malware Information Sharing Platform)**.

## 🎯 Goal
The goal of this tool is to streamline the process of:

1️⃣ Extracting **IP addresses** and **URLs** associated with offenses from QRadar.  
2️⃣ Allowing a human analyst to **approve or reject** the data for further action.  
3️⃣ Adding approved attributes dynamically to **MISP events**.  
4️⃣ Automatically **publishing the updated MISP event** for broader visibility.

## 🔧 How It Works
🗂️ **QRadar Offenses**: The script connects to QRadar and fetches offenses containing threat indicators.  
👩‍💻 **Approval Interface**: Displays IPs and URLs for an analyst to approve using a simple input interface.  
🛠️ **MISP Integration**: Adds approved indicators to a specified MISP event.  
🚀 **Publish Events**: Publishes the updated MISP event automatically.

## ⚠️ Privacy and Security Notice
This script is designed with modularity and privacy in mind. No hardcoded sensitive data is included in the repository. You must provide your **QRadar API**, **MISP API tokens**, and other configurations locally. Please handle your credentials securely.

## 🛠️ Requirements
- Python 3.x  
- Libraries: `requests`, `json`, etc.

## 📝 Disclaimer
This project is provided as-is. It is not affiliated with QRadar or MISP and should be used responsibly within the boundaries of your organization's security policies.
