Perfect, Sarab 👌 — here’s a clean, professional set of **delivery notes** you can include with the script.

---

### 📄 `README-INSTALL.md` — LinkedIn Message Scraper (Delivery Notes)

---

## ✅ Overview

This script automates the scraping of **unread LinkedIn messages**, groups all messages by the **latest visible timestamp**, and writes them into a CSV (`linkedin_messages.csv`).
It prevents duplicates and updates existing rows when the sender + timestamp combination already exists.

---

## 📦 1. Requirements

* Windows system (tested on Windows 10+)
* Google Chrome installed
* ChromeDriver (auto-used via Selenium)
* Python 3.8+

---

## 🧪 2. Setup Instructions

### a) Clone or download the script folder.

### b) Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 📄 `requirements.txt` contents:

```txt
selenium
pandas
requests
```

---

### c) Configure the script:

Open the script and update these two variables if your system has different paths:

```python
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = r"C:\chrome-profile"
```

* `CHROME_PATH`: Chrome browser executable
* `USER_DATA_DIR`: New or existing Chrome profile (to preserve login session)

---

## 🔐 3. First Time Manual Login (Only Once)

1. The script will open Chrome in remote debugging mode.
2. On the **first run**, it will ask you to log in to [linkedin.com](https://linkedin.com).
3. After login is successful, press **ENTER** in the terminal.
4. From now on, the script will keep you logged in via the saved profile.

---

## ▶️ 4. Run the Script

```bash
python linkedin_scraper.py
```

---

## 🧠 5. How It Works

* Detects **only unread** chats
* Opens each unread chat
* Extracts **only messages grouped under the most recent visible timestamp**
* Writes messages to `linkedin_messages.csv`

  * If `Sender + Timestamp` already exists → the row is **updated**
  * Else → new row is **added**
* Prevents duplicates using hash-based memory set

---

## 📁 6. Output File

**`linkedin_messages.csv`**

| Sender        | Timestamp | Message                        |
| ------------- | --------- | ------------------------------ |
| Sarabjit Deol | 2:07 PM   | Hi\nThis is sarb\nThank you... |

---

## ✅ 7. Tips

* The script runs in an infinite loop by default (`CHECK_INTERVAL = 2` seconds).
* You can increase the wait time to reduce LinkedIn load.
* To exit, press `CTRL + C` in the terminal.

---

Let me know if you also want:

* A zipped delivery folder with this inside
* A Google Drive backup link
* Or a short onboarding video/script for your client

You’re ready to deliver like a pro 🔥
