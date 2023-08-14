# labber-wrapper
A library of software utilities and experimental procedures built on Labber. The library provides the following features on top of the Labber python API.

1) Ease of use. Labber's data model exposes all of its instrument configurations as key, value dictionaries with setters and getters. The objects have keys that are irregular and hard to predict. Therefore we have written utilities that allow code complletion to fill in the blanks for you.

2) Validation. We have written JSON Schemas for all of the configuration dictionaries relevant to devices in the QSTL lab that specify acceptable value types and ranges. Any experiment script can be validated in real-time or before-hand by either enabling continuous validation or a precursory call to `validate()`. This way we won't fry any devices.

3) Compatibility. We initialize our objects with the appropriate JSON Schemas and use the Labber API to populate them so that they match whatever configuration you have setup on your instrument at startup. We can then validate any changes that your script makes to the configuration with no effort.

4) Experiments. We have provided a number of out-of-the-box experiments such as voltage sweeps and piecewise voltage ramps.

# Testing

To run the tests associated with a particular driver run the correpsonding test suite like `python -m unittest tests/devices/test_Keithley_2400.py`. To run the entire test suite use `python -m unittest discover`.
