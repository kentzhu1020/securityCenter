
# Overview

This script is used to load, view, remove the assets into(from) security center via REST API.

Script runs based on Python. In order to use the script please install python above 2.7 but lower than 3.0

The script also used third-party open source libary pycurl, please you download pyurl on [Github](https://github.com/pycurl/pycurl) and install.

## Usage

####Please follow bellow illustrate to run the job.

Right now this is the version 1 which support:

```
 -h,print help message.
 -v,view all the asset.
 -d,view asset by id.
 -l,load all the asset into security center.
 -r,remove all the asset.
 -s,remove the asset by id.
```

You could follow command to use the script.

```
cd /path/to/your/script
python sc_asset.py -option

```

This script is an interactive batch job. User need to input your valid username and password. login as the valid login credential. the job would run and give you a correspond response.

```
Enter SecurityCenter username: 
Enter SecurityCenter password: 
```





