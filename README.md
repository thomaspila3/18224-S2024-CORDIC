# CORDIC

Thomas Kang
18-224 Spring 2024 Final Tapeout Project

## Overview

CORDIC is a module that computes non-linear functions like cosine, sine, arctan, and distance formula without the usage of multipliers or dividers. There are two modes: vectoring and rotation mode. Vectoring mode returns arctan and length of a vector while rotation mode returns cosine and sine. 

## How it Works

In order to save space but also get a faster clock, I will be divide this into 16 stages, and 4 stages will be merged to one large stage. Total of 4 large stages are pipelined. 
Each stage will perform a single iteration, which consists of couple of subtractors and comparators, and uses a singular pre-coded LUT value. Depending on the mode_toggle value that chooses between rotation mode and vectoring mode, in_x, in_y, and in_z into the stages differ. Each stage simply computes the addition or subtraction of in_x/shifted in_y, in_y/shifted in_x, and in_z/z_coefficient. Whether it subtracts or adds depends on the mode_toggle as well as the sign of in_y and in_z. 
After going through 16 stages in total, depending on the out_toggle and mode_toggle, one can choose which value to generate. Rotation mode generates cosine and sine of the input radian value. Vectoring generates arctan(y_in/x_in) or K(x_in^2 + y_in^2)^1/2 where K is a pre-defined value of 1.646760. 


![](docs/CORDIC_diagram.pdf)

## Inputs/Outputs

### INPUTS:
**Clk**: simple clock\
**rst**: resets the design. Each time one wants to change the mode or change the input value, you would need to assert this after changing the inputs accordingly.\
**10-bit in_val**: A 3-bit decimal, 7-bit fraction radian value for rotation mode, while it is 2 5-bit fraction x and y coordinate values concatenated for vectoring mode.\
**1-bit out_toggle**: toggles between different outputs. Cosine vs sine OR arctan(y_in/x_in) vs K(x_in^2 + y_in^2)^1/2\
**1-bit mode_toggle**: 0 means rotation mode, 1 means vectoring mode

### OUTPUTS:
**1-bit done**: Denotes when the calculation is done.\ 
**11-bit val**: Output of the design that can be changed by out_toggle or mode_toggle. 2-bit decimal and 9-bit fraction weighted two’s complement value. 

## Design Testing / Bringup

One can test the design using the provided cocotb testbench in testing/cordic_tb.py and testing/testbench.mk. Simply by running “make -Bf testbench.mk,” it will output the input and output of each testcase. The cocotb testbench sweeps the entire input range, which is 0~1.50 radians by 0.01 steps for rotation mode, and 1/32 ~ 31/32 x/y coordinate values for vectoring mode. Due to the limited number of input bits, vectoring mode saw some output values that weren’t as accurate. Those that are within 0.01 are full pass, within 0.1 are partial pass, and anything exceeding that was a fail. There are 30x30 = 900 total test cases, and there were 9 partial passes and 27 fails. For rotation mode, everything was within 0.01 error rate, giving them all a pass. For more information, take a look at testing/cordic_tb.py and testing/testbench.mk. Input_test_mode0 tests rotation mode, and input_test_mode1 tests vectoring mode.

One can also test the design using a microcontroller and an FPGA. The sample micropython code is testing/fpga_test_simple.py, and the constraints.lpf file was used to load the design on a ulx3s FPGA board. Simply hook up the Pi Pico(or any microcontroller) with the FPGA and initiate the output and input gpio pins. Once that’s done, set the input to whatever you want, reset the design, and you should see the output of the design being loaded. Every time you want to change the input value or mode, you will have to reset the design in between.

## Future Work
In case there are more pins accessible, it would be great to try increasing the x and y input width to get a better precision on the vectoring mode output. 
Without an increase in pins, one could try these to improve the design:
1) Make the design take in x and y input over multiple cycles to get a wider input value
2) Have internal processing that enables the rotation mode to take in multiple quadrant radian values. 
And others as well.

## References
web.cs.ucla.edu/digital_arithmetic/files/ch11.pdf

