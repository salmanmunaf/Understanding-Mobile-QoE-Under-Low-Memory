# DASH Experiments
This folder contains all the scripts related to the DASH experiments presented in the paper.

### Prerequisites
- Install prerequisites (tested with Ubuntu 16.04, Tensorflow v1.1.0, TFLearn v0.3.1 and Selenium v2.39.0)
```
python setup.py
```
- Install apache server using the following link: https://vitux.com/how-to-install-and-configure-apache-web-server-on-ubuntu/

- Make sure the device is rooted in order to extract device metrics using the file device_data.js

### Guidlines about Experiments

- Run the file called `server3.sh` to start the apache server. Make sure that video and manifest files are stored in the appropriate folder in the machine accessible through the server.

- `simple_server.py` launches an ABR server on the machine.

- `device_data.js` gathers device metrics from an Android device.

- Use the memory pressure application to restrict memory on the Android device.

- Assign the appropriate variable values in the following files: `ABRController.js`, `simple_server.py`.