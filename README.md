# 🌡️ Temperature and Humidity Monitoring System

## 📚 Project Overview
This project is a **temperature and humidity monitoring system** built on a **Raspberry Pi**. It reads data from a **DHT11 sensor**, logs it, displays it on an **OLED screen**, and triggers a **relay** and **buzzer** for certain temperature thresholds. In case of high temperature, the system sends **alerts via email** 📧 and **Telegram** 📲.

### 🔧 Features:
- **Temperature & Humidity Monitoring**: Reads real-time data from a DHT11 sensor.
- **OLED Display**: Displays temperature and humidity values on a connected OLED screen 🖥️.
- **Relay & Buzzer Control**: Controls a relay and triggers a buzzer 🔊 when the temperature crosses certain thresholds.
- **Email Alerts**: Sends email alerts 📧 when the temperature exceeds a certain limit.
- **Telegram Alerts**: Sends Telegram notifications for temperature-related alerts 📲.
- **Data Logging**: Logs temperature and humidity data to a CSV file 📊 for record-keeping.
- **Flask Web Interface**: Provides an API to get real-time temperature and humidity data 🌍.

## 🛠️ Requirements
Before running the system, make sure you have the following:

1. **Hardware Requirements**:
   - Raspberry Pi (any model with GPIO support) 🖥️
   - DHT11 Temperature and Humidity Sensor 🌡️
   - 128x64 OLED Display (SSD1306) 🖥️
   - Buzzer 🔊
   - Relay (for controlling an external device) 🔌

2. **Software Requirements**:
   - Python 3.x 🐍
   - Libraries:
     - `RPi.GPIO`
     - `time`
     - `smtplib`
     - `pandas`
     - `Adafruit_SSD1306`
     - `flask`
     - `requests`
   
   To install the required libraries, you can use pip:
   ```bash
   pip install -r requirements.txt
   sudo apt-get install libssl-dev
   sudo apt-get install libjpeg-dev
   sudo apt-get install python3-pip
   sudo pip3 install Adafruit_SSD1306
   ```

## 🛠️ Setup Instructions

1. **Hardware Connections**:

| **Component**       | **Pin on Raspberry Pi**  | **Description**                             |
|---------------------|--------------------------|---------------------------------------------|
| **DHT11 Sensor**     | GPIO Pin 4 (BCM)          | Used for reading temperature and humidity   |
| **Relay Module**     | GPIO Pin 17 (BCM)         | Controls external devices based on temperature thresholds |
| **Buzzer**           | GPIO Pin 27 (BCM)         | Emits a sound when the temperature exceeds a threshold |
| **OLED Display (SDA)**| GPIO Pin 2 (BCM, SDA)     | Used for data communication (I2C SDA)      |
| **OLED Display (SCL)**| GPIO Pin 3 (BCM, SCL)     | Used for clock communication (I2C SCL)     |
| **Ground (GND)**     | Any Ground Pin (e.g., Pin 6) | Connect to the ground of all components     |
| **5V Power**         | Pin 2 (5V)                | Power the components (DHT11, Relay, Buzzer, OLED) |

2. **Email Configuration**:
   - Set up an email account (Gmail recommended) 📧.
   - Generate an **App Password** for your Gmail account (for security reasons).
   - Replace `your_email@gmail.com` and `your_app_password` in the code with your Gmail credentials.

3. **Telegram Configuration**:
   - Create a Telegram bot using [BotFather](https://core.telegram.org/bots#botfather) 📲.
   - Get your **Telegram Bot Token** and **Chat ID**.
   - Replace `your_telegram_bot_token` and `your_chat_id` in the code with these values.

4. **Run the System**:
   - Once everything is connected and configured, run the system:
   ```bash
   python3 app.py
   ```

   The system will start reading temperature and humidity from the DHT11 sensor 🌡️, log the data to a CSV file 📊, display the readings on the OLED screen 🖥️, and send alerts if needed ⚠️.

## 🌐 Web Interface
- Open the web interface by navigating to `http://<raspberry_pi_ip>:5000/` in your web browser 🌍.
- The homepage will show basic details 🏠.
- The `/data` endpoint will provide real-time temperature and humidity data in JSON format 📊.


## 🛠️ Code Walkthrough

- **Temperature and Humidity Reading**: The `read_dht11()` function simulates reading from a DHT11 sensor 🌡️. It returns hardcoded values for temperature and humidity.
- **Display**: The `update_display()` function clears and updates the OLED display with the current temperature and humidity 🖥️.
- **Data Logging**: The `log_data()` function saves the temperature and humidity readings into a CSV file 📊, appending each new entry.
- **Alerting**: The system sends an email 📧 and Telegram alert 📲 if the temperature exceeds a set threshold (100°C in this case).
- **Relay and Buzzer Control**: If the temperature exceeds 40°C 🔥, the relay is activated. If it exceeds 200°C 🔥, a buzzer sounds 🔊.

## 🛠️ Troubleshooting
- If the **DHT11 sensor** is not working, check the wiring and ensure the sensor is functioning correctly ⚠️.
- Ensure your Raspberry Pi has internet access 🌐 for email and Telegram notifications.
- Verify the **email credentials** 📧 and **Telegram bot settings** 📲 if alerts are not working.
