## Telemetry?
Telemetry is an open source performance benchmarking tool provided by google developers, which provides multiple utilities to record/reply benchmarks on available browsers whether desktop or android.

### How to run telemetry benchmarks locally
To [run telemetry locally](https://github.com/catapult-project/catapult/blob/master/telemetry/docs/run_benchmarks_locally.md), you must clone [latest chromium checkout](https://chromium.googlesource.com/chromium/src/+/master/docs/android_build_instructions.md#install-depot_tools) and install [depot tools](https://chromium.googlesource.com/chromium/src/+/master/docs/android_build_instructions.md#install-depot_tools)  to run benchmarks properly.

Clonning and checking out chromium is time taking and data consuming task, for replicator's convinience we have uploaded archive to chromium and depot tools. you should only download it and extract to the local directory.

### Setup Telemetry
Even if one download chromium from available archives, one must have to fulfill basic requirements to run telemetry.
a mentioned [here](https://github.com/catapult-project/catapult/blob/master/telemetry/docs/run_benchmarks_locally.md).
#### Windows
Some benchmarks require you to have pywin32. Be sure to install a version that matches the version and bitness of the Python you have installed.

#### Linux
Telemetry on Linux tries to scan for attached Android devices with adb. The included adb binary is 32-bit. On 64-bit machines, you need to install the libstdc++6:i386 package.

#### Android
Running on Android is supported with a Linux or Mac OS X host. Windows is not yet supported. There are also a few additional steps to set up:

Telemetry requires adb. If you're running from the zip archive, adb is already included. But if you're running with a Chromium checkout, ensure your .gclient file contains target_os = ['android'], then resync your code.
If running from an OS X host, you need to run ADB as root. First, you need to install a "userdebug" build of Android on your device. Then run adb root. Sometimes you may also need to run adb remount.

userdebug builds for android devices are also available [here](https://github.com/ehsanlatif/Understanding-Mobile-QoE-Under-Low-Memory/tree/master/web_browser_experiments/am_footprint_web/user_debug_build_images).

Enable debugging over USB on your device.
You can get the name of your device with adb devices and use it with Telemetry via --device=<device_name>.



We have built chromium for android device Nexus 5 (OS 6.0), if you want to run it on the different device then you should follow [these instructions](https://chromium.googlesource.com/chromium/src/+/master/docs/android_build_instructions.md#setting-up-the-build) up to [updating your checkout](https://chromium.googlesource.com/chromium/src/+/master/docs/android_build_instructions.md#updating-your-checkout).

### Test chromium before runnig benchmarks
Before running benchmarks, you have to [Install and Run Chromium on your device](https://chromium.googlesource.com/chromium/src/+/master/docs/android_build_instructions.md#installing-and-running-chromium-on-a-device).
If all goes well, then you need to run ADB as root by running this command on the terminal:(ensure that your device is connected to adb)
``` terminal
$ adb root
```

### Run Benchmarks
##### Testing available browser
First you have to change your current directory to /chromium/src/tools/perf/
then you have to run following command to check for available browsers:
``` terminal
$ ./run_benchmark --browser=list
```
If it shows android-chromium as browser then you can run any benchmark on it. if not then you first check your device connctivity and browser version compatibility.

##### Running benchmark for memory footprint 
To get memory footprints of websites, you first have to set website's URLs in the file of /chromium/src/tools/perf/page_sets/memory_top_10_mobile.py as a list of (link, title) tuple.

URLs to [Alexa top 100 webistes](https://github.com/ehsanlatif/Understanding-Mobile-QoE-Under-Low-Memory/tree/master/web_browser_experiments/am_footprint_web/samples/top_100_pages) are also provided.

To run memory benchmark, you first have to record it as a binary file using record script of telemetry by runnig:
```terminal
$ ./record_wpr --browser=android-chromium  memory_top_10_mobile
```
then you have to reply these files to get real picture of memory footprint as:
```terminal
$ ./run_benchmark --browser=android-chromium --pageset-repeat=15 memory.top10.mobile --output-format=csv
```
you can repeat benchmark as many times as you want by changing value of **--pageset-repeat** in the command.

The above command will create a results.csv file.

To parse this csv file you can use our script availble [here](https://github.com/ehsanlatif/Understanding-Mobile-QoE-Under-Low-Memory/tree/master/web_browser_experiments/am_footprint_web/csv_parsers/mem_process_files.py).


##### Running benchmark for loading times
o get memory footprints of websites, you first have to set website's URLs in the file of /chromium/src/tools/perf/page_sets/loading_mobile.py as a list of (link, title) tuple.

To run loading time benchmark, you first have to record it as a binary file using record script of telemetry by runnig:
```terminal
$ ./record_wpr --browser=android-chromium  loading_mobile
```
then you have to reply these files to get real picture of memory footprint as:
```terminal
$ ./run_benchmark --browser=android-chromium --pageset-repeat=15 loading.mobile --output-format=csv
```
you can repeat benchmark as many times as you want by changing value of **--pageset-repeat** in the command.

The above command will create a results.csv file.

To parse this csv file you can use our script availble [here](https://github.com/ehsanlatif/Understanding-Mobile-QoE-Under-Low-Memory/tree/master/web_browser_experiments/am_footprint_web/csv_parsers/plt_process_files.py).
