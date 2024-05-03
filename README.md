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

OR you can go to this google drive link: https://drive.google.com/file/d/1buy2GcVNB3jInE9abCZTOaj97sAnSFyX/view 

**Install pymavlink**
```
pip install pymavlink
```


**To run**
```
cd NGCP/pymavlink
mkdir ArduPlane
cd ArduPlane
sim_vehicle --map --console
```

**IN A DIFFERENT TERMINAL**
```
python3 {any_script.py}
```
