# PowerScan ⚡🔬

**PowerScan** is a lightning-fast file scanning tool that helps you search for specific keywords in large file directories. 🚀 It features an interactive web interface, PowerShell backend processing, and real-time progress tracking. Whether you're a cybersecurity professional, researcher, or data analyst, **PowerScan** makes searching through massive datasets a breeze! 🔎💡

---

## Features 🛠️✨

- **Web-Based UI 🌐** – Simple, user-friendly interface to input keywords and view results.
- **Fast PowerShell Backend ⚡** – Efficient scanning using a PowerShell script.
- **Real-Time Progress Tracking 📊** – Stay updated with live scan progress.
- **Advanced Filtering 🔍** – Include or exclude specific words to refine results.
- **Multi-Format Export 📄** – Save results as TXT or CSV.
- **Interactive Logs 📜** – View scan logs and track system events.
- **Shutdown Button 🔴** – Easily stop the scan or shut down the system.

---

## Installation & Setup 🚀

### Prerequisites 📌
- **Windows OS** (PowerShell is required)
- **Python 3+ 🐍** (For running the backend server)
- **Web Browser 🌍** (To access the interface)

### Step 1: Clone the Repository 📂
```sh
 git clone https://github.com/yourusername/PowerScan.git
 cd PowerScan
```

### Step 2: Install Dependencies 📦
Run the following command to install Python dependencies:
```sh
 pip install -r requirements.txt
```

### Step 3: Run PowerScan 🏃‍♂️💨
Start the server using:
```sh
 run.bat
```
This will:
✅ Start the Python backend
✅ Launch PowerShell for scanning
✅ Open the web interface in your browser

---

## How to Use ❓🤔
1. **Enter Keywords 📝** – Type the keyword(s) to search for.
2. **Set Max Results 📏** – Choose how many matches you want to retrieve.
3. **Choose Match Type 🎯** – Select **Partial** or **Exact** match.
4. **Optional Filters 🎛️** – Include or exclude specific words.
5. **Click 'Start Scan' 🚀** – Watch real-time progress and logs.
6. **View & Export Results 📂** – Download as TXT or CSV.

---

## File Structure 📁🗂️
```
PowerScan/
│── index.html        # Web Interface
│── server.py         # Python Backend Server
│── FileScanner.ps1   # PowerShell Script for Scanning
│── run.bat           # Startup Script
│── requirements.txt  # Python Dependencies
│── Refined_Results/  # Folder for scan results
│── logs.txt          # System Log File
```

---

## Troubleshooting & FAQs 🛠️🤖

### 1️⃣ Scan Doesn't Start? ❌
- Ensure **PowerShell execution policy** allows scripts:
```sh
 Set-ExecutionPolicy Bypass -Scope Process -Force
```

### 2️⃣ Results Not Showing? 📉
- Check the `Refined_Results` folder for output files.
- Refresh the web page.

### 3️⃣ Stuck or Frozen? 🥶
- Use the **Stop Scan** button.
- Restart the server (`run.bat`).

---

## Credits & Acknowledgment 🙌🎖️
This project was developed with the help of **ChatGPT o3-mini-high**. 🤖💡 Special thanks to all contributors who helped improve PowerScan! 🚀💙

---

## License 📜🔓
PowerScan is **open-source** and licensed under the **MIT License**. Feel free to modify and improve it!

📌 **GitHub Repo**:(https://github.com/smartboy223/PowerScan)

Happy Scanning! 🎉🔍

