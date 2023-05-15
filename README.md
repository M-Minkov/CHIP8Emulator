# CHIP8Emulator

An emulator (or more like interpreter) for the Chip8 language. This was a very nice introduction for me to learn about how emulators generally work.

I had an okay-ish understanding of memory busses, assembly, and CPU architecture before. This project helped further solidify it.

I'd recommend people to do a project like this, if they would like to further solidify that knowledge.

Though, I recommend C++ over Python, as bit-masking is actually much more straight-forward and makes more sense in C++.
Doing an AND operation on an 8-bit signed number, that you know will always be 8-bit no matter what, has a great feeling to it in C++.

Where-as Python has an affair with the CPU behind your back, and you just never know what it's upto.

I did modularize the code with classes a bit though. A GUI class, and a Chip8 class.
GUI is always displayed, and the Chip8 sends write requests to it. I tried to make the code as readable as possible.
