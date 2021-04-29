# BirdNET Backend

Continuously running BirdNET on a VM

## Installation

Clone the [BirdNET repository](https://github.com/mitwelten/BirdNET) and follow the [installation insturctions](https://github.com/mitwelten/BirdNET#installation)



### Requirements

Tested versions on Ubuntu 20.04 *CPU*:

Python version: 3.8.5


Package|Version
-|-
future|0.18.2 
Lasagne|0.2.dev1
librosa|0.8.0
llvmlite|0.36.0
numpy| 1.20.2
scipy| 1.6.2
Theano|1.0.5+unknown

### Continuous operation of BirdNET

Download the file [analyze-continuous.py](analyze-continuous.py) next to the `analyze.py` file in the cloned [BirdNET repository](https://github.com/mitwelten/BirdNET).

Create the folders `input` and `output` in the BirdNET directory.

Start the application
```sh
python3 analyze-continuous.py
```

Or use the [service script](birdnet.service)
