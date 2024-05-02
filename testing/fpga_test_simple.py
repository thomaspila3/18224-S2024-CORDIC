from machine import Pin

# initiate IN gpio pins
gpio_0 = Pin(0, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_1 = Pin(1, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_2 = Pin(2, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_3 = Pin(3, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_4 = Pin(4, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_5 = Pin(5, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_6 = Pin(6, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_7 = Pin(7, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_8 = Pin(8, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_9 = Pin(9, mode=Pin.IN, pull=Pin.PULL_DOWN)
gpio_10 = Pin(10, mode=Pin.IN, pull=Pin.PULL_DOWN)


# initiate OUT gpio pins
gpio_11 = Pin(11, mode=Pin.OUT)
gpio_12 = Pin(12, mode=Pin.OUT)
gpio_13 = Pin(13, mode=Pin.OUT)
gpio_14 = Pin(14, mode=Pin.OUT)
gpio_15 = Pin(15, mode=Pin.OUT)
gpio_16 = Pin(16, mode=Pin.OUT)
gpio_17 = Pin(17, mode=Pin.OUT)
gpio_18 = Pin(18, mode=Pin.OUT)
gpio_19 = Pin(19, mode=Pin.OUT)
gpio_20 = Pin(20, mode=Pin.OUT)
# out toggle, mode toggle
gpio_21 = Pin(21, mode=Pin.OUT)
gpio_22 = Pin(22, mode=Pin.OUT)

# sample input 
in_list = [1,1,1,1,1,1,0,1,0,1]
in_string = ""
for i in range(len(in_list)):
    in_string += str(in_list[i])

# for some reason, using in_string here doesn't work
mode_tog = 1
out_tog = 1

gpio_11.value(in_list[9])
gpio_12.value(in_list[8])
gpio_13.value(in_list[7])
gpio_14.value(in_list[6])
gpio_15.value(in_list[5])
gpio_16.value(in_list[4])
gpio_17.value(in_list[3])
gpio_18.value(in_list[2])
gpio_19.value(in_list[1])
gpio_20.value(in_list[0])
    
gpio_21.value(out_tog)
gpio_22.value(mode_tog)

print(f"inputs:")
print(f"in_val: {in_string} out_toggle: {out_tog} mode_toggle: {mode_tog}")
print(f"output:")
print(f"done: assume 1 val: {gpio_10.value()}{gpio_9.value()}\
{gpio_8.value()}{gpio_7.value()}{gpio_6.value()}{gpio_5.value()}{gpio_4.value()}\
{gpio_3.value()}{gpio_2.value()}{gpio_1.value()}{gpio_0.value()}")