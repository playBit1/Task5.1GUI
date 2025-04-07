import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                           QRadioButton, QPushButton, QLabel, QButtonGroup, 
                           QLineEdit)
from PyQt5.QtCore import Qt
import RPi.GPIO as GPIO

class LEDControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.red_pin = 11
        self.green_pin = 13
        self.blue_pin = 15
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        
        self.turn_off_all_leds()
        self.init_ui()
    
    def init_ui(self):
        #Set window
        self.setWindowTitle('LED Control GUI')
        self.setFixedSize(350, 250)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addSpacing(10)
        
        
        #title label
        title_label = QLabel('Raspberry Pi LED Control GUI')
        title_label.setStyleSheet("font-weight: bold;")
        title_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title_label)
        
        
        #radio buttons
        radio_layout = QVBoxLayout()
        radio_layout.setSpacing(5)
        self.led_group = QButtonGroup(self)
        
        self.red_radio = QRadioButton('Red')
        self.green_radio = QRadioButton('Green')
        self.blue_radio = QRadioButton('Blue')
        
        self.red_radio.setStyleSheet("font-size: 14px; margin-left: 5px;")
        self.green_radio.setStyleSheet("font-size: 14px; margin-left: 5px;")
        self.blue_radio.setStyleSheet("font-size: 14px; margin-left: 5px;")
        
        self.led_group.addButton(self.red_radio, 1)
        self.led_group.addButton(self.green_radio, 2)
        self.led_group.addButton(self.blue_radio, 3)

        radio_layout.addWidget(self.red_radio)
        radio_layout.addWidget(self.green_radio)
        radio_layout.addWidget(self.blue_radio)
        
        
        main_layout.addLayout(radio_layout)
        
        self.led_group.buttonClicked.connect(self.update_leds)
        
        
        #text input box and submit button
        input_label = QLabel('Enter Color Name (Red, Green or Blue)')
        input_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(input_label)
        
        input_layout = QHBoxLayout()
        
        self.color_input = QLineEdit()
        submit_button = QPushButton('Submit')
        submit_button.setFixedWidth(70)
        submit_button.clicked.connect(self.process_text_input)
        
        input_layout.addWidget(self.color_input)
        input_layout.addWidget(submit_button)
        
        main_layout.addLayout(input_layout)
        
        
        #exit button
        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.closeEvent)
        main_layout.addWidget(exit_button)
        
        
        self.setLayout(main_layout)
        
    def update_leds(self, button):
        self.turn_off_all_leds()
        
        if button == self.red_radio:
            GPIO.output(self.red_pin, GPIO.HIGH)
        elif button == self.green_radio:
            GPIO.output(self.green_pin, GPIO.HIGH)
        elif button == self.blue_radio:
            GPIO.output(self.blue_pin, GPIO.HIGH)
    
    def process_text_input(self):
        color_text = self.color_input.text().lower().strip()
        self.turn_off_all_leds()
        
        if color_text == "red":
            self.red_radio.setChecked(True)
            GPIO.output(self.red_pin, GPIO.HIGH)
        elif color_text == "green":
            self.green_radio.setChecked(True)
            GPIO.output(self.green_pin, GPIO.HIGH)
        elif color_text == "blue":
            self.blue_radio.setChecked(True)
            GPIO.output(self.blue_pin, GPIO.HIGH)
        
        self.color_input.clear()
    
    def turn_off_all_leds(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)
    
    def closeEvent(self, event):
        GPIO.cleanup()
        event.accept()

# Initialize the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LEDControlGUI()
    window.show()
    sys.exit(app.exec_())
