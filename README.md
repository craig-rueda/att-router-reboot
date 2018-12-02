# att-router-reboot
Simple python script that logs into and then reboots `BGW210` routers provided by AT&T.

## Usage
 0. Optionally setup a virtual env
 ```Bash
 virtualenv venv
 source ./venv/bin/activate
 ```

 1. Install dependencies:
 ```Bash
 pip install -r requirements.txt
 ```
 2. Run main.py
 ```Bash
 ROUTER_BASE_URL='http://192.168.1.254'
 ACCESS_CODE='sdf#$%SD'
 
 python main.py -u ${ROUTER_BASE_URL} -a ${ACCESS_CODE}
 ```
 
 After running the script, your router should have restarted...