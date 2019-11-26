## WebPageTest
At its core, WebPagetest is used for measuring and analyzing the performance of web pages.
There are a lot of options that may seem intimidating at first but doing quick testing is pretty simple.
This guide will walk you through submitting a test and interpreting the results. you can find compete dicumentation [here](https://sites.google.com/a/webpagetest.org/docs/using-webpagetest).
### How to Setup
Follow the instructions in given [webpage](https://linuxhowtoguide.blogspot.com/2017/01/how-to-setup-web-page-test-private.html).

Add this to www/settings/locations.ini:
``` sript
        [locations]
        1=Stamford_Office
        default=Stamford_Office

        [Stamford_Office]
        1=LUMS-Desktop
        2=Samsung-S6
        3=Nokia-1
        label=LUMS
        connectivity=LAN

        [LUMS-Desktop]
        browser=Chrome,Firefox
        label="Abdul's Laptop"
        connectivity=LAN

        [Samsung-S6]
        browser=Chrome
        label="Samsung-S6"
        type=nodejs,mobile
        connectivity="WiFi"

        [Nokia-1]
        browser=Nokia1 - Chrome,Nokia1 - Chrome Beta
        label="Nokia-1"
        type=nodejs,mobile
        connectivity="WiFi"
```

if location.ini is not present rename locations.ini.sample to locations.ini and replace the above lines 

Download wptagent from the link:
        https://codeload.github.com/WPO-Foundation/wptagent/zip/master

Run following command inside wptagent:
``` terminal
$ python wptagent.py -vvvv --server "http://localhost/work/" --android --location Samsung-S6
```
