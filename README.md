# Understanding-Mobile-QoE-Under-Low-Memory
https://github.com/ehsanlatif/Understanding-Mobile-QoE-Under-Low-Memory
## About Repository
  In our paper we analyze application performance under low memory regime, for which we have performed different experiments on mobile devices. In this repository, we have provided all the tools, images, files, scripts and also mentioned required dependencies along with the commands to install them, which we have used to perform experiments described in the paper. 
  
  In our work there are three common applications were under our observation: Web Browsing, Email and Video Streaming. In each application, we have performed different experiments to analyze the QoE (Quality of Experience). We have examined application memory footprint, application behaviour under high memory pressure regime and also performed experiments as the base of our suggested optimizations for each application. For almost all the experiments, we have used a 2GB RAM device Nexus 5 with a quad-core processor as a mid-range device mostly used in developing countries.
  
  To perform the experiments of tracking memory footprint, we have flashed User Debug Build (built from Google repository) to the device. Furthermore, for creating artificial memory pressure using third party application (memory pressure simulator), we have rooted the device. We have tracked memory footprints by using telemetry, and for getting webpage size and more details about web page requests we have used WebPageTest an open-source tool available by Google. For simulating memory Pressure we have designed and developed our native android application using SDK and NDK on the tool of android studio. For tracking PSS of applications, we also have developed an android application.

