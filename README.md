# GFDM USRP PHY-Reference

This repository contains a simplified reference model of GFDM/filtered OFDM signal processing layer, which is roughly aligned to the [GFDM hardware implementation from the eWine Project](https://github.com/ewine-project/Flexible-GFDM-PHY). Some parts are not yet implemented (e.g. channel coding)


## How to run
- Clone repository and submodules

```
git clone
git submodule init
git submodule update
```

- Requirements
    - The project was created and tested with python 3.6.5
    - required packages are listed in reqirements.txt. You can install them using pip:  ```pip install -r reqirements.txt  ```

- Run example: ```python /path/to/repository/simulation/example_waveform_test.py```
