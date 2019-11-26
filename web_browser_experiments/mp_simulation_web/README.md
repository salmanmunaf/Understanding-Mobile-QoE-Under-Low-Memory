## Memory Pressure Simulator
We have developed andoid application using NDK and SDK on android studio which creates artificial memory presure to the device.
We have uplaoded apk released version [here](https://github.com/ehsanlatif/Understanding-Mobile-QoE-Under-Low-Memory/tree/master/web_browser_experiments/mp_simulation_web/mp_simulator).

### Root Requirement
MPSimulator requires root permission to restrict memory, for which the target device must be rooted.
We also have provide root images [here](https://github.com/ehsanlatif/Understanding-Mobile-QoE-Under-Low-Memory/tree/master/web_browser_experiments/mp_simulation_web/root_images).

### Experiment
We create memory pressure to the device using our application and then run telemetry to getits impact on webpage's page load time.

### Geting system state
You can check system state after creating memroy pressure using folloing command:
``` terminal
$ adb shell dumpsys meminfo
```
this will give you a clear picture of mobile memory state.

### Core Binding
we restrict cpu cores and then analyzed its impact on webpage loading time.
we bind cpu cores by using **taskset** commands.


```terminal
su
taskset -p (cpumask) (pid)
cat /proc/pid/status --> To check if binded
```
Cpus_allowed:	2 --> 0010 --> Binded to CPU 1 only

Cpus_allowed_list:	1 --> ^
```terminal
su
 Without stopping this service, the following approach will fail
# You can run it after. This will increase battery life. So, I suggest to run it.
stop mpdecision

# Make the file writable
chmod 664 /sys/devices/system/cpu/cpu0/online

# Make the core always offline
echo 0 > /sys/devices/system/cpu/cpu0/online

# Make the file read-only. 
# Now "online" status will not be changed by external apps
chmod 444 /sys/devices/system/cpu/cpu0/online

# Run the service again
start mpdecision
```
