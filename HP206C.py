# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HP206C
# This code is designed to work with the HP206C_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=HP206C_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)


# I2C address of the device
HP206C_DEFAULT_ADDRESS				= 0x76

# HP206C Command Set
HP206C_SOFT_RST						= 0x06 # Soft reset the device
HP206C_ADC_CVT						= 0x40 # Perform ADC conversion
HP206C_READ_PT						= 0x10 # Read the temperature and pressure values
HP206C_READ_AT						= 0x11 # Read the temperature and altitude values
HP206C_READ_P						= 0x30 # Read the pressure value only
HP206C_READ_A						= 0x31 # Read the altitude value only
HP206C_READ_T						= 0x32 # Read the temperature value only
HP206C_ANA_CAL						= 0x28 # Re-calibrate the internal analog blocks
HP206C_READ_REG						= 0x80 # Read out the control registers
HP206C_WRITE_REG					= 0xC0 # Write in the control registers

# OSR and Channel Configuration
HP206C_OSR_4096						= 0x00 # Conversion time: 4.1ms
HP206C_OSR_2048						= 0x04 # Conversion time: 8.2ms
HP206C_OSR_1024						= 0x08 # Conversion time: 16.4ms
HP206C_OSR_512						= 0xC0 # Conversion time: 32.8ms
HP206C_OSR_256						= 0x10 # Conversion time: 65.6ms
HP206C_OSR_128						= 0x14 # Conversion time: 131.1ms
HP206C_CH_PRESSTEMP					= 0x00 # Sensor Pressure and Temperature Channel 
HP206C_CH_TEMP						= 0x02 # Temperature Channel

class HP206C():
	def p_cnvrsn_config(self):
		"""Select the OSR and Channel Configuration Command from the given provided value"""
		CNVRSN_CONFIG = (HP206C_ADC_CVT | HP206C_OSR_2048 | HP206C_CH_PRESSTEMP)
		bus.write_byte(HP206C_DEFAULT_ADDRESS, CNVRSN_CONFIG)
	
	def read_pres(self):
		"""Read back data from HP206C_READ_P(0x30), 3 bytes
		pressure MSB, pressure CSB, pressure LSB"""
		data = bus.read_i2c_block_data(HP206C_DEFAULT_ADDRESS, HP206C_READ_P, 3)
		
		pressure = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
		
		return {'p' : pressure}
	
	def read_temp(self):
		"""Read back data from HP206C_READ_T(0x32), 3 bytes
		pressure MSB, pressure CSB, pressure LSB"""
		data = bus.read_i2c_block_data(HP206C_DEFAULT_ADDRESS, HP206C_READ_T, 3)
		
		cTemp = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
		fTemp = (cTemp * 1.8) + 32
		
		return {'c' : cTemp, 'f' : fTemp}
	
	def read_altitude(self):
		"""Read back data from HP206C_READ_A(0x31), 3 bytes
		altitude MSB, altitude CSB, altitude LSB"""
		data = bus.read_i2c_block_data(HP206C_DEFAULT_ADDRESS, 0x11, 6)
		cTemp = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
		fTemp = (cTemp * 1.8) + 32
		altitude = (((data[3] & 0x0F) * 65536) + (data[4] * 256) + data[5]) / 100.00
		
		return {'a' : altitude}

from HP206C import HP206C
hp206c = HP206C()

while True :
	hp206c.p_cnvrsn_config()
	alt = hp206c.read_altitude()
	print "Altitude : %.2f m"%(alt['a'])
	pres = hp206c.read_pres()
	print "Pressure : %.2f hPa"%(pres['p'])
	temp = hp206c.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************** "
	time.sleep(1)
