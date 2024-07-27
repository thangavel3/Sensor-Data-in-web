from flask import Flask, render_template
import serial
import time

app = Flask(__name__)

# Initialize serial connection with Arduino
ser = serial.Serial('COM8', 9600, timeout=2)  # Change 'COM8' to your correct COM port

def read_serial_data():
    ser.write(b'r')  # Send a request to Arduino to send data
    time.sleep(2)
     data = ser.readline().decode().strip()
    return data

def parse_data(data):
    try:
        print("Received data from Arduino:", data)
        humidity, temperature = data.split(',')
        humidity = float(humidity)
        temperature = float(temperature)
        if 0 <= humidity <= 100 and -40 <= temperature <= 125:  # Valid ranges for DHT11 sensor
            return humidity, temperature
        else:
            raise ValueError("Invalid humidity or temperature value")
    except ValueError as e:
        print("Error parsing data:", e)
        raise

@app.route('/')
def index():
    try:
        data = read_serial_data()
        humidity, temperature = parse_data(data)
        return render_template('index.html', humidity=humidity, temperature=temperature)
    except Exception as e:
        print("An error occurred:", e)
        return "Error: Failed to read sensor data"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
