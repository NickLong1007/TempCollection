import board
import busio
import adafruit_mcp9600
import time
import datetime
import adafruit_ahtx0
import digitalio
import adafruit_max31855
import random
import urllib.request
import requests
import threading
from adafruit_htu21d import HTU21D

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
spi = board.SPI()

#Water Inlet Temperature
cs_inlet = digitalio.DigitalInOut(board.D5)
water_inlet = adafruit_max31855.MAX31855(spi, cs_inlet)

#Water Outlet Temperature
cs_outlet = digitalio.DigitalInOut(board.D6)
water_outlet = adafruit_max31855.MAX31855(spi, cs_outlet)

#Temperature and Humidity Sensor 
air_inlet = adafruit_ahtx0.AHTx0(i2c,address= 0X38)
air_outlet = HTU21D(i2c,address = 0X40)

#UnderGround
mcp_0 = adafruit_mcp9600.MCP9600(i2c, address= 0X60)
mcp_2 = adafruit_mcp9600.MCP9600(i2c, address= 0X62)
mcp_3 = adafruit_mcp9600.MCP9600(i2c, address= 0X63)
mcp_5 = adafruit_mcp9600.MCP9600(i2c, address= 0X65)
mcp_6 = adafruit_mcp9600.MCP9600(i2c, address= 0X66)
mcp_7 = adafruit_mcp9600.MCP9600(i2c, address= 0X67)

#Begin Variable Averege For Underground
five = 0
six = 0
seven = 0 
eight = 0
nine = 0
ten = 0

#Begin Varible For Averege Above Ground 
enter_temp = 0
enter_humid = 0
exit_temp = 0
exit_humid = 0
fluid_enter = 0
fluid_exit = 0
while True:
    for x in range(5):
        time.sleep(1)
        now = datetime.datetime.now()
        five_ft= round(((mcp_0.temperature*.668)+5.84),2)
        six_ft= round(((mcp_2.temperature*.666)+6.666),2)
        seven_ft= round(((mcp_3.temperature*.682)+5.5),2)
        eight_ft= round(((mcp_5.temperature*.663)+7.2),2)
        nine_ft= round(((mcp_6.temperature*.663)+7.2),2)
        ten_ft= round(((mcp_7.temperature*.684)+4.875),2)
        
        five += five_ft
        six += six_ft
        seven += seven_ft
        eight += eight_ft
        nine += nine_ft
        ten += ten_ft
        enter_temp += air_inlet.temperature
        enter_humid += air_inlet.relative_humidity
        exit_temp += air_outlet.temperature
        exit_humid += air_outlet.relative_humidity
        fluid_enter += water_inlet.temperature
        fluid_exit += water_inlet.temperature
    
        date_time = (now.strftime("Date:%Y/%m/%d Time:%H:%M:%S"))
        print("Data Collection Succesfull, Collected at:"+date_time)
        print("")
        print("Run Number", x+1)
        print("UnderGround Temperature: \n  5Ft:{} C \n  6Ft:{} C \n  7Ft:{} C \n  8Ft:{} C \n  9Ft:{} C\n  10Ft:{} C ".format(five_ft,six_ft,seven_ft,eight_ft,nine_ft,ten_ft))
        print("")
        print("Inlet Temperature and Humidity:")
        print("  Temperature: %0.1f C" % air_inlet.temperature)
        print("  Humidity: %0.1f %%" % air_inlet.relative_humidity)
        print("")
        print("Outlet Temperature and Humidity:")
        print("  Temperature: %0.1f C" % air_outlet.temperature)
        print("  Humidity: %0.1f %%" % air_outlet.relative_humidity)
        print("")
        print("Inlet and Outlet Water Temperature:")
        print("  Inlet:{} C \n  Outlet:{} C".format(water_inlet.temperature,water_outlet.temperature))
        
    #The 3 is the Number of Data point and needs to be accurate
    five_avg=round((five/(x+1)),2)
    six_avg=round((six/(x+1)),2)
    seven_avg=round((seven/(x+1)),2)
    eight_avg=round((eight/(x+1)),2)
    nine_avg=round((nine/(x+1)),2)
    ten_avg=round((ten/(x+1)),2)
    
    enter_temp_avg=round((enter_temp/(x+1)),2)
    enter_humid_avg=round((enter_humid/(x+1)),2)
    exit_temp_avg=round((exit_temp/(x+1)),2)
    exit_humid_avg=round((exit_humid/(x+1)),2)
    fluid_enter_avg=round((fluid_enter/(x+1)),2)
    fluid_exit_avg=round((fluid_exit/(x+1)),2)
    
        #Below Ground
    def thingspeak():
        #timerbelow is how often to upload in seconds
        URL='https://api.thingspeak.com/update?api_key='
        KEY='KY192MJQ1J9101BS'
        #field 1 and 2 are created on thing speak and the values come
        #from val 1 and val 2
        HEADER='&field1={}&field2={}&field3={}&field4={}&field5={}&field6={}'.format(five_avg,six_avg,seven_avg,eight_avg,nine_avg,ten_avg)
        new_URL=URL+KEY+HEADER
        v=urllib.request.urlopen(new_URL)
        print(v)
    if __name__== '__main__':
        thingspeak()
        
        #Above Ground 
    def thingspeak():
        #timerbelow is how often to upload in seconds
        URL='https://api.thingspeak.com/update?api_key='
        KEY='V1KQU9V58WSZ8WKZ'
        #field 1 and 2 are created on thing speak and the values come
        #from val 1 and val 2
        HEADER='&field1={}&field2={}&field3={}&field4={}&field5={}&field6={}'.format(enter_temp_avg,enter_humid_avg,exit_temp_avg,exit_humid_avg,fluid_enter_avg,fluid_exit_avg)
        new_URL=URL+KEY+HEADER
        v=urllib.request.urlopen(new_URL)
        print(v)
        print("Average Data has been sent\n",(x+1)," Runs Were Averaged")
        print("For Reference The Five Foot Average was: ", five_avg)
    if __name__== '__main__':
        thingspeak()
    five = 0
    six = 0
    seven = 0 
    eight = 0
    nine = 0
    ten = 0
