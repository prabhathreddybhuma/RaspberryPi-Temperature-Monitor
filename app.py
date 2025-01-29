import RPi.GPIO as GPIO
import time
import smtplib
import pandas as pd
import Adafruit_SSD1306
from email.mime.text import MIMEText
from flask import Flask, render_template, jsonify
import requests

DHT_PIN = 4
RELAY_PIN = 17
BUZZER_PIN = 27

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"

TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

OLED_WIDTH = 128
OLED_HEIGHT = 64
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()

app = Flask(__name__)
LOG_FILE = "temperature_log.csv"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def send_email_alert(temperature):
    subject = "🔥 High Temperature Alert!"
    body = f"Warning! The current temperature is {temperature}°C. Take immediate action."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("📧 Email sent successfully!")
    except Exception as e:
        print(f"❌ Email Error: {e}")

def send_telegram_alert(temperature):
    message = f"⚠️ High Temperature Alert: {temperature}°C!"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("📩 Telegram alert sent!")
        else:
            print("❌ Telegram Error:", response.text)
    except Exception as e:
        print("❌ Telegram Connection Error:", e)

def read_dht11():
    GPIO.setup(DHT_PIN, GPIO.OUT)
    GPIO.output(DHT_PIN, GPIO.LOW)
    time.sleep(0.018)
    GPIO.output(DHT_PIN, GPIO.HIGH)
    time.sleep(0.00002)
    GPIO.setup(DHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    temperature = 35
    humidity = 55
    return temperature, humidity

def update_display(temperature, humidity):
    disp.clear()
    disp.display()
    time.sleep(0.1)
    message = f"T: {temperature}°C\nH: {humidity}%"
    print("📟 OLED Display:", message)
    disp.text(message, 10, 10, 1)
    disp.display()

def log_data(temperature, humidity):
    data = {"Temperature": [temperature], "Humidity": [humidity], "Time": [time.strftime("%Y-%m-%d %H:%M:%S")]}
    df = pd.DataFrame(data)

    try:
        df.to_csv(LOG_FILE, mode='a', header=not pd.io.common.file_exists(LOG_FILE), index=False)
        print("📊 Data Logged Successfully!")
    except Exception as e:
        print(f"❌ Logging Error: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def get_data():
    temp, hum = read_dht11()
    return jsonify({"temperature": temp, "humidity": hum})

try:
    while True:
        temperature, humidity = read_dht11()

        if temperature is not None and humidity is not None:
            print(f"🌡 Temperature: {temperature}°C, 💧 Humidity: {humidity}%")
            update_display(temperature, humidity)
            log_data(temperature, humidity)

            GPIO.output(RELAY_PIN, GPIO.HIGH if temperature > 40 else GPIO.LOW)
            if temperature > 200:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                print("🔊 Buzzer Alert!")
                time.sleep(0.5)
                GPIO.output(BUZZER_PIN, GPIO.LOW)

            if temperature > 100:
                send_email_alert(temperature)
                send_telegram_alert(temperature)

        else:
            print("⚠️ Sensor Read Error.")

        time.sleep(2)

finally:
    GPIO.cleanup()
