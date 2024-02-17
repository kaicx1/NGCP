# NGCP
Flight scripts using Ardupilot and PyMavLink on Ubuntu20.0

**Install Ardupilot**

```
cd ~
sudo apt install git
git clone https://github.com/ArduPilot/ardupilot.git
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
. ~/.profile
```

**Install pymavlink**
```
pip install pymavlink
```


**To run**
```
cd NGCP/pymavlink
mkdir ArduPlane
cd ArduPlane
sim_vechile --map --console
```

**IN A DIFFERENT TERMINAL**
```
python3 {any_sript.py}
```
