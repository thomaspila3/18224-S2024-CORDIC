import copy
import cocotb
import logging
import random
import math
from cocotb.triggers import *
from cocotb.clock import Clock

ERROR = 0
PARTIAL_ERROR = 0

# resets the design
async def reset_design(dut):
    dut.rst.value = True
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = False

# gets the magnitude of a binary value
def twos_comp(val, bits):
    is_negative = False
    if (val & (1 << (bits-1))) != 0: # sign bit is a 1
        val = val - (1 << bits)
        is_negative = True
    return (val, is_negative)

def bin_to_int(val):
    int_val = 0
    mask = 1
    for i in range(11):
        int_val += mask & val
        mask = mask << 1
    return int_val

# changes the binary output of the module into floats
def bin_to_float(bin_val):
    (twos_comp_val, is_negative) = twos_comp(bin_val, 11)
    return (bin_to_int(twos_comp_val) / 512, is_negative)


# changes a radian value to binary string
def rad_to_binary(rad):
    rad_copy = int(rad * 128)
    out_bin = ""
    for i in range(10):
        curr_bit = rad_copy & 1
        out_bin = out_bin + str(curr_bit)
        rad_copy = rad_copy >> 1
    return "0b" + out_bin[::-1]

def int_to_binary_mode1(in_val):
    int_val = int(in_val * 32)
    bin_val = 0
    mask = 1
    for i in range(5):
        bin_val += mask & int_val
        mask = mask << 1
    return bin_val

# run test
async def input_test_mode0(dut, in_rad):
    global ERROR

    await reset_design(dut)
    dut.mode_toggle.value = 0
    dut.out_toggle.value = 0
    dut.in_val.value = int(rad_to_binary(in_rad), 2)

    while (dut.done.value != 1):
        await FallingEdge(dut.clk)
    fin_val, fin_val_neg = bin_to_float(dut.val.value)
    dut.out_toggle.value = 1
    await FallingEdge(dut.clk)
    fin_val_1, fin_val_neg = bin_to_float(dut.val.value)
    print(f"Testing Rotation mode CORDIC. Input: {in_rad} radians")
    # print(f"my cos: {fin_val} real cos: {math.cos(in_rad)}")
    # print(f"my sin: {fin_val_1} real sin: {math.sin(in_rad)}")
    if (abs(fin_val - math.cos(in_rad)) < 0.01 and abs(fin_val_1 - math.sin(in_rad)) < 0.01):
        print(fin_val)
        print(f"pass! error within 0.01 \n\n")
    else:
        print(f"fail! error larger than 0.01\n\n")
        ERROR += 1

# run test
async def input_test_mode1(dut, in_x, in_y):
    global ERROR, PARTIAL_ERROR

    await reset_design(dut)
    dut.mode_toggle.value = 1
    dut.out_toggle.value = 0
    dut.in_val.value = ((int_to_binary_mode1(in_x)) << 5) + int_to_binary_mode1(in_y)

    while (dut.done.value != 1):
        await FallingEdge(dut.clk)

    print(dut.val.value)
    fin_val, fin_val_neg = bin_to_float(dut.val.value)
    dut.out_toggle.value = 1
    await FallingEdge(dut.clk)
    print(dut.val.value)
    fin_val_1, fin_val_neg = bin_to_float(dut.val.value)
    print(f"Testing vectoring mode CORDIC. In_x: {in_x} In_y: {in_y}")
    print(f"{fin_val} {fin_val_1} {math.atan(in_y/in_x)} {1.646760 * math.dist([0,0], [in_x, in_y])}")

    if (abs(fin_val_1 - math.atan(in_y/in_x)) < 0.01 and abs(fin_val - 1.646760 * math.dist([0,0], [in_x, in_y]) < 0.01)):
       print(f"pass! error within 0.01 \n\n")
    elif (abs(fin_val_1 - math.atan(in_y/in_x)) < 0.1 and abs(fin_val - 1.646760 * math.dist([0,0], [in_x, in_y]) < 0.1)):
       print(f"partial pass! error within 0.1 \n\n")
       PARTIAL_ERROR += 1
    else:
        print(f"fail! error larger than 0.01\n\n")
        ERROR += 1



@cocotb.test()
async def test(dut):
    global ERROR, PARTIAL_ERROR

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await FallingEdge(dut.clk)
    await reset_design(dut)

    for i in range(150):
        await input_test_mode0(dut, i * 0.01)
    for i in range(1,32):
        for j in range(1,32):
            await input_test_mode1(dut, i/32, j/32)

    print(f"Total testcases: 1050. There are {ERROR} large margin errors in the design, {PARTIAL_ERROR} smaller margin errors")

