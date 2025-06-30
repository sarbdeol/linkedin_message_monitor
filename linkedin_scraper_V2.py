import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# Configs
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = r"C:\chrome-profile"
REMOTE_PORT = 9222
CHECK_INTERVAL = 2  # seconds between checks
BUFFER_TIMEOUT = 60  # seconds to wait before printing

message_buffer = {}

def is_remote_debugging_running():
    try:
        response = requests.get(f"http://127.0.0.1:{REMOTE_PORT}/json/version", timeout=2)
        return response.status_code == 200
    except:
        return False

def launch_chrome():
    print("Launching Chrome with remote debugging...")
    cmd = f'"{CHROME_PATH}" --remote-debugging-port={REMOTE_PORT} --user-data-dir="{USER_DATA_DIR}"'
    subprocess.Popen(cmd)
    time.sleep(5)

# Launch or attach to Chrome
if not is_remote_debugging_running():
    launch_chrome()
    while not is_remote_debugging_running():
        time.sleep(1)
    print("Chrome launched and ready.")
else:
    print("Chrome already running with remote debugging.")

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{REMOTE_PORT}")
driver = webdriver.Chrome(options=chrome_options)

# Go to LinkedIn
driver.get("https://www.linkedin.com/feed/")
time.sleep(3)

# Login check
if "login" in driver.current_url:
    print("Please log in manually.")
    input("After login is complete, press ENTER to continue...")
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(3)
    if "login" in driver.current_url:
        print("Still not logged in. Exiting.")
        driver.quit()
        exit()
    print("Login successful.")
else:
    print("Already logged in.")

# Messaging page
driver.get("https://www.linkedin.com/messaging/")
time.sleep(5)

while True:
    try:
        # Flush any expired user message batches
        current_time = time.time()
        expired_users = []
        for user, data in message_buffer.items():
            if current_time - data['last_received_time'] >= BUFFER_TIMEOUT:
                print({
                    "Sender": user,
                    "Timestamp": data["timestamp"],
                    "Messages": data["messages"]
                })
                expired_users.append(user)

        for user in expired_users:
            del message_buffer[user]

        # Get unread conversations
        unread_convos = driver.find_elements(By.XPATH, '//div[contains(@class, "msg-conversation-card__convo-item-container--unread")]')
        if unread_convos:
            print(f"Found {len(unread_convos)} unread chats.")

        for convo in unread_convos:
            try:
                convo.click()
                time.sleep(3)

                # Sender name
                try:
                    chat_name = driver.find_element(By.CSS_SELECTOR, "h2#thread-detail-jump-target").text.strip()
                except NoSuchElementException:
                    chat_name = "Unknown Chat"

                # Get all message blocks and timestamps
                message_blocks = driver.find_elements(By.CSS_SELECTOR, "li.msg-s-message-list__event")
                timestamps_all = driver.find_elements(By.CSS_SELECTOR, "time.msg-s-message-group__timestamp")

                if timestamps_all:
                    latest_timestamp = timestamps_all[-1].text.strip()
                else:
                    latest_timestamp = "Unknown"

                # Find index of latest timestamp block
                latest_index = -1
                for i in range(len(message_blocks)):
                    try:
                        ts = message_blocks[i].find_element(By.CSS_SELECTOR, "time.msg-s-message-group__timestamp").text.strip()
                        if ts == latest_timestamp:
                            latest_index = i
                    except NoSuchElementException:
                        continue

                grouped_messages = []
                for block in message_blocks[latest_index:]:
                    try:
                        try:
                            message_text = block.find_element(By.CSS_SELECTOR, "p.msg-s-event-listitem__body").text.strip()
                        except NoSuchElementException:
                            message_text = ""
                        grouped_messages.append(message_text)
                    except:
                        continue

                if grouped_messages:
                    if chat_name not in message_buffer:
                        message_buffer[chat_name] = {
                            "timestamp": latest_timestamp,
                            "messages": [],
                            "last_received_time": current_time
                        }

                    existing = message_buffer[chat_name]["messages"]


                    # Append only unique new messages
                    for msg in grouped_messages:
                        if msg not in existing:
                            existing.append(msg)

                    # Update last received time
                    message_buffer[chat_name]["last_received_time"] = current_time

                # Optional: mark as read
                try:
                    driver.find_element(By.CSS_SELECTOR, "div.msg-form__contenteditable").click()
                    time.sleep(1)
                except:
                    pass

            except (NoSuchElementException, StaleElementReferenceException):
                continue

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("Error: Please restart the script.")
        time.sleep(10)
