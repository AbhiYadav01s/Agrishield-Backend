# Agri-Vyakaroti (Team Trophe) 🌾
**Smart India Hackathon 2026 | Problem Statement: SIH26131**

Agri-Vyakaroti is a 3-tier hybrid AI and community-driven ecosystem for early detection and management of crop diseases, designed specifically to bridge the gap between technical concepts and market-ready GovTech ecosystems.

## 🚀 Live Links
- **Live Prototype:** https://agrivyakaroti-frontend-new.vercel.app/
- **Frontend Repository:** https://github.com/AbhiYadav01s/Agrishield-Frontend-NEW
- **Demonstration Video:** https://youtu.be/elOccKth8zE

## 🧠 Core Architecture
Our solution is built on a 3-tier ecosystem:
1. **Farmer PWA:** A voice-first, multilingual interface for low-literacy users, featuring Edge AI capabilities.
2. **Extension Worker Portal (Regional Dashboard):** Features a live Hotspot Radar, Scrutiny Queue, and Yojana Status tracking for PMFBY claims.
3. **Agronomist Validation Dashboard:** A Tier-3 escalation inbox and AI Retraining Studio for unidentified anomalies.

## 💻 Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** React.js, Tailwind CSS
- **Database:** MongoDB
- **AI/ML:** ResNet-50 (Disease Diagnostics), YOLOv8 (Pest Counting)
- **External APIs:** AgriStack (Identity), Bhashini (Translation), OpenWeatherMap, Leaflet.js

## ⚙️ How to Run Locally (Backend)
```bash
git clone [https://github.com/AbhiYadav01s/Agri-Vyakaroti.git](https://github.com/AbhiYadav01s/Agri-Vyakaroti.git)
cd Agri-Vyakaroti
pip install -r requirements.txt
python app.py
