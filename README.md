# 🔥 Tor IP Changer – Python Script

### Hey there, awesome people! 👋 Welcome to my project! I’m **Ally**, and I made this for all of you who love tech, privacy, and cool Python scripts! 🚀

**A fully automated Python script that changes your IP using Tor at custom intervals. Works on Windows without requiring admin permissions! 🔥**  

🔗 **Check out my YouTube channel for more awesome projects:** [**My Channel**](https://www.youtube.com/@Ally-released) ❤️


---

## 📌 Features
✅ **Automatically starts Tor & routes Firefox traffic**  
✅ **IP changes at custom intervals (user-defined time in seconds)**  
✅ **Displays new IP directly in CMD (no browser pop-ups)**  
✅ **Uses clean & professional UI with color coding**  
✅ **No admin permissions required**  

---

## ⚙️ How It Works
1️⃣ **Starts Tor** and ensures it's running  
2️⃣ **Opens Firefox once** to verify the first connection  
3️⃣ **Changes your IP automatically** at the set interval  
4️⃣ **Displays the new IP in CMD** after every change  

---

## 🎯 Installation Guide
### **1️⃣ Install Dependencies**
Run the following command to install all required Python libraries:  
```bash
pip install -U selenium stem pysocks requests colorama
```

### **2️⃣ Download & Run the Script**
```bash
git clone https://github.com/YOUR-USERNAME/Tor-IP-Changer.git
cd Tor-IP-Changer
python ip_changer.py
```

---

## 🎮 Usage Instructions
When you run the script, it will **ask for two things**:  
1️⃣ **Seconds between IP changes** (Example: `5` means change every 5 seconds)  
2️⃣ **How many times to change the IP** (Example: `10` changes or `0` for unlimited)  

```
Welcome to the Tor IP Changer
==================================================
Enter seconds between IP changes: 5
Enter how many times to change IP (0 for unlimited): 10
==================================================
```

---

## 🔥 Example Output in CMD
```
[INFO] Starting Tor... ...
[SUCCESS] Tor is running!
[INFO] Opening Firefox for initial verification...
[SUCCESS] Verified Tor connection in Firefox!
[SUCCESS] Initial Tor IP: 185.220.101.6

[SUCCESS] New Tor IP: 198.51.100.42
[INFO] IP changed 1 times. Waiting 5 seconds...

[SUCCESS] New Tor IP: 203.0.113.77
[INFO] IP changed 2 times. Waiting 5 seconds...
```

---

## 📜 Code Explanation

### **🔹 1️⃣ Checking if Tor is Running**
```python
def is_tor_running():
    """Check if Tor is running by trying to connect to the SOCKS proxy."""
    try:
        response = requests.get(
            "http://check.torproject.org",
            proxies={"http": f"socks5h://{TOR_SOCKS_PROXY}", "https": f"socks5h://{TOR_SOCKS_PROXY}"},
            timeout=5
        )
        return response.status_code == 200
    except requests.RequestException:
        return False
```
📢 **Explanation:**  
- This **sends a request through Tor** to check if it's working.  
- If it gets a **response (status code 200), Tor is running!** ✅  

---

### **🔹 2️⃣ Starting Tor with a Loading Animation**
```python
def start_tor():
    """Ensure Tor is running before launching Firefox."""
    tor_executable = os.path.join(TOR_DIR, "tor.exe")

    if not os.path.exists(tor_executable):
        print(f"{ERROR} Tor binary not found! Please check the installation.")
        exit(1)

    print(f"{INFO} Starting Tor... ", end="", flush=True)
    tor_process = subprocess.Popen(
        [tor_executable, "--SocksPort", "9050", "--ControlPort", "9051"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    for _ in range(15):
        if is_tor_running():
            print(f"\r{SUCCESS} Tor is running!            ")
            return tor_process
        print(".", end="", flush=True)
        time.sleep(2)

    print(f"\n{ERROR} Tor failed to start!")
    exit(1)
```
📢 **Explanation:**  
- It **starts Tor in the background** and waits until it's ready.  
- The **animated dots ("...")** give a **professional loading effect** instead of freezing.  
- If Tor **fails to start**, the script **exits gracefully** with an error message.  

---

## 📚 Technologies Used
- **Python** 🐍  
- **Tor** 🕵️‍♂️  
- **Selenium** 🖥️  
- **STEM (Tor Controller)** 🔄  
- **Colorama (CMD UI Enhancements)** 🎨  

---

## 🛠️ Troubleshooting
❌ **Tor is not starting?**  
➡️ Make sure **Tor is installed** and located in the correct directory.  

❌ **GeckoDriver error?**  
➡️ Ensure the correct **GeckoDriver version** is installed for your **Firefox browser**.  

❌ **Firewall blocks Tor?**  
➡️ Try **disabling your firewall** temporarily and rerun the script.  

---

## 📜 License
**MIT License** - Feel free to use and modify this script for personal or educational purposes.  

---

## 📩 Contact & Contributions
Got suggestions or improvements? Feel free to **fork** this project and submit a **pull request**!  
💬 **Need help?** Open an issue on GitHub!  

🔗 **Subscribe for more cool projects!** [**My Channel**](https://www.youtube.com/@Ally-released) ❤️

