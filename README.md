# 💳 Credit Card Fraud Detection Dashboard  
### *Interactive Streamlit Dashboard for Fraud Pattern Analysis*

---

## 🚀 Project Overview
This project analyzes real-world credit card transactions to identify patterns that differentiate **fraudulent** from **legitimate** activity.  
It includes:

- Data Cleaning & Preprocessing  
- Exploratory Data Analysis (EDA)  
- Interactive Streamlit Dashboard  
- Insights on Customer, Merchant, Time, and Geographical fraud patterns  
- Actionable recommendations for fraud detection  

---

## 📁 Repository Structure
├── app.py # Streamlit Dashboard
├── clean_transactions.csv # Cleaned dataset
├── streamlit_dashboard.ipynb
├── README.md # Documentation
└── notebook/
└── bank_fraud_analysis.ipynb # Full analysis notebook 

---

## 🛠️ Tech Stack
- **Python**
- **Streamlit**
- **pandas, NumPy**
- **Plotly (Express + Choropleth maps)**  
- **Custom CSS (Dark Mode + Smoky Purple Theme)**

---

## 🧹 Data Cleaning & Feature Engineering
### ✔ Cleaning
- Removed unnecessary & PII columns  
- Cleaned merchant/category names  
- Converted state abbreviations  
- Handled missing values  

### ✔ Engineered Features
- Time features: hour, day, month, quarter, season  
- Age & age groups  
- Distance calculation using Haversine formula  
- Distance bands (Local, Close, Far, Very Far)

---

## 📊 Dashboard Tabs

### **1️⃣ Overview**
- Fraud vs Non-Fraud distribution  
- Age distribution  
- Transaction amount patterns  
- Gender breakdown  

### **2️⃣ Customer Insights**
- Age groups with highest fraud cases  
- Gender-based fraud rate  
- Avg transaction amount by gender  

### **3️⃣ Merchant & Category Insights**
- Category transaction volume  
- Fraud concentration by category  
- High-risk merchants  
- Avg transaction by category  

### **4️⃣ Geographical Analysis**
- Distance band distribution  
- Fraud contribution by distance  
- Top fraud-heavy states  
- U.S. state fraud rate map  

### **5️⃣ Time-Based Patterns**
- Fraud by hour  
- Normal activity by hour  
- Fraud by weekday  
- Seasonal fraud patterns  

### **6️⃣ Summary Dashboard**
- Key insights  
- Recommendations  
- Final takeaway  

---

## 🔍 Key Findings
- Fraud spikes at **night (10 PM–3 AM)**  
- Seniors are the **most vulnerable age group**  
- Fraud clusters in **Pennsylvania, New York, Michigan**  
- Targeted categories: **shopping_net, misc_net, grocery_pos**  
- Long-distance transactions show higher fraud probability  

---

## 🛡️ Recommendations
- Increase monitoring during **night hours** and **weekends**  
- Apply **distance-based risk scoring**  
- Add extra checks for **high-risk merchants**  
- Strengthen authentication for **senior customers**  
- Use behavior clustering for model improvements  

---

## ▶️ How to Run the Dashboard

### 1️⃣ Clone the repo
git clone https://github.com/ALAAMEKAWY56/Credit-Card-Fraud-Detection-Dashboard.git

cd Credit-Card-Fraud-Detection-Dashboard


### 2️⃣ Install dependencies
pip install -r requirements.txt

### 3️⃣ Run Streamlit
streamlit run app.py

---
### requirements.txt
- streamlit
- pandas
- numpy
- plotly

---


## 👩‍💻 Author

**Alaa Mekawi**  
Data Science & AI Engineer  

🔗 **LinkedIn:**  
https://www.linkedin.com/in/alaa-mekawi  

🔗 **GitHub:**  
https://github.com/ALAAMEKAWY56

Special thanks to **@Epsilon-AI-Institute** for providing training and support during this project.


