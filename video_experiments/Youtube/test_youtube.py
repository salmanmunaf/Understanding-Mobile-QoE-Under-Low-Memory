import unittest
import time
from datetime import datetime
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException


VIDEO_SEARCH = ''
RESULT_FILE = './results/log_youtube.txt'

class YoutubeAndroidTest(unittest.TestCase):
    def __init__(self):
        constant_quality = True
        
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '' # Android version
        desired_caps['deviceName'] = '' # Device Name
        # desired_caps['noReset'] = 'true'
        desired_caps['appPackage'] = 'com.google.android.youtube'
        desired_caps['appActivity'] = 'com.google.android.apps.youtube.app.WatchWhileActivity'

        self.driver = webdriver.Remote('', desired_caps) #Device IP

    def tearDown(self):
        self.driver.quit()

    def existsById(self, id):
        try:
            self.driver.find_element_by_id(id)
        except NoSuchElementException:
            return False
        return True

    def existsByXpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def existsByXpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def existsByAccessibilityId(self, accessibility_id):
        try:
            self.driver.find_element_by_accessibility_id(accessibility_id)
        except NoSuchElementException:
            return False
        return True

    def testGetStats(self):
        # search_button = self.driver.find_element_by_xpath('//android.widget.ImageView[@content-desc="Search"]')
        # while not (self.existsByAccessibilityId('Account')):
        #     pass
        time.sleep(7)
        account_button = self.driver.find_element_by_accessibility_id('Account')
        account_button.click()

        while not (self.existsByXpath('/hierarchy/android.widget.FrameLayout/\
            android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
            android.support.v7.widget.RecyclerView/android.widget.LinearLayout[6]')):
            pass
        settings_button = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/\
            android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
            android.support.v7.widget.RecyclerView/android.widget.LinearLayout[6]')
        settings_button.click()

        while not (self.existsByXpath('/hierarchy/android.widget.FrameLayout/\
            android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/\
            android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
            android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ListView/\
            android.widget.LinearLayout[1]/android.widget.RelativeLayout')):
            pass
        general_settings_button = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/\
            android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/\
            android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
            android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ListView/\
            android.widget.LinearLayout[1]/android.widget.RelativeLayout')
        general_settings_button.click()

        while not (self.existsByXpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/\
            android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
            android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/\
            android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
            android.widget.ListView/android.widget.LinearLayout[7]/android.widget.LinearLayout/\
            android.widget.Switch')):
            pass
        enable_stats_switch = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/\
            android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/\
            android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
            android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/\
            android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[7]/\
            android.widget.LinearLayout/android.widget.Switch')
        enable_stats_switch.click()

        navigate_up = self.driver.find_element_by_accessibility_id('Navigate up')
        navigate_up.click()
        navigate_up.click()

        search_button = self.driver.find_element_by_accessibility_id('Search')
        search_button.click()

        search_box = self.driver.find_element_by_id('com.google.android.youtube:id/search_edit_text')
        search_box.send_keys(VIDEO_SEARCH)
        self.driver.press_keycode(66)

        # time.sleep(5)

        while not (self.existsByXpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/\
            android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
            android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/\
            android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/\
            android.widget.FrameLayout[2]/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/\
            android.widget.FrameLayout[1]/android.widget.LinearLayout')):
            pass

        video = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/\
            android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
            android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/\
            android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/\
            android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout')
        video.click()

        time.sleep(1)
        # more_options = self.driver.find_element_by_xpath('//android.widget.ImageView[@content-desc="More options"]')
        # tap_video = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout\
        # /android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout\
        # /android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup\
        # /android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup\
        # /android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout\
        # /android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.View')
        # tap_video.click()
        # more_options.click()

        

        if (self.constant_quality):

            action1 = TouchAction(self.driver)
            action1.tap(None, 1365, 175)
            action1.perform()

            action2 = TouchAction(self.driver)
            action2.tap(None, 1365, 175)
            action2.perform()

            while not (self.existsByXpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/\
            android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/\
            android.widget.RelativeLayout[2]')):
                pass

            quality_button = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/\
                android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
                android.widget.ListView/android.widget.RelativeLayout[2]')
            quality_button.click()

            while not (self.existsByXpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/\
                android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/\
                android.widget.RelativeLayout[2]')):
                pass

            quality = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/\
                android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/\
                android.widget.ListView/android.widget.RelativeLayout[2]')
            quality.click()


        action1 = TouchAction(self.driver)
        action1.tap(None, 1365, 175)
        action1.perform()

        action2 = TouchAction(self.driver)
        action2.tap(None, 1365, 175)
        action2.perform()

        while not (self.existsByXpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/\
            android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/\
            android.widget.RelativeLayout[4]')):
            pass

        stats_button = self.driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/\
            android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/\
            android.widget.RelativeLayout[4]')
        stats_button.click()

        # copy_info_button = self.driver.find_element_by_id('com.google.android.youtube:id/copy_debug_info_button')
        # copy_info_button.click()

        # text = self.driver.get_clipboard_text()

        # with open(RESULT_FILE, 'w') as f:
        #     f.write("TimeStamp" + '\t' + "VideoFormat" + '\t' + "AudioFormat" + '\t' + "ReadAhead" + '\t' + "Viewport" + '\t' + "BandwidthEstimate" + \
        #     '\t' + "DroppedFrames" + '\n')
        with open(RESULT_FILE, 'w') as f:
            f.write("TimeStamp" + '\t' + "VideoFormat" + '\t' + "BandwidthEstimate" + '\t' + "DroppedFrames" + '\n')

        # readahead_num = -1
        output_list = []
        # current_time_obj = 0
        # total_time_obj = 1
        while True:
            try:
                video_format = self.driver.find_element_by_id('com.google.android.youtube:id/video_format').text
                audio_format = self.driver.find_element_by_id('com.google.android.youtube:id/audio_format').text
                readahead = self.driver.find_element_by_id('com.google.android.youtube:id/readahead').text
                viewport = self.driver.find_element_by_id('com.google.android.youtube:id/viewport').text
                bandwidth_estimate = self.driver.find_element_by_id('com.google.android.youtube:id/bandwidth_estimate').text
                dropped_frames = self.driver.find_element_by_id('com.google.android.youtube:id/dropped_frames').text

                # if not (self.existsById('com.google.android.youtube:id/time_bar_current_time')):
                    # action3 = TouchAction(self.driver)
                    # action3.tap(None, 565, 175)
                    # action3.perform()

                # current_time = self.driver.find_element_by_id('com.google.android.youtube:id/time_bar_current_time').text
                # total_time = self.driver.find_element_by_id('com.google.android.youtube:id/time_bar_total_time').text

                # current_time_obj = datetime.strptime(current_time, '%M:%S')
                # total_time_obj = datetime.strptime(total_time, '%M:%S')

                # readahead_num = float(readahead[:-2])
                # print datetime.now().strftime("%M:%S")
                # output_list.append(str(current_time_obj.time()) + '\t' + video_format + '\t' + audio_format + '\t' + readahead + '\t' + viewport + '\t' + \
                 # bandwidth_estimate + '\t' + dropped_frames)
                output_list.append(str(datetime.now().strftime("%M:%S")) + '\t' + video_format + '\t' + audio_format + '\t' + readahead + '\t' + viewport + '\t' + \
                 bandwidth_estimate + '\t' + dropped_frames)
                # output_list.append(str(datetime.now().strftime("%M:%S")) + '\t' + video_format + '\t' + dropped_frames)

                if (self.existsById('com.google.android.youtube:id/countdown')):
                    break

            except NoSuchElementException:
                # with open(RESULT_FILE, 'a') as f:
                #     for row in output_list:
                #         f.write(row + '\n')
                continue

        with open(RESULT_FILE, 'a') as f:
            for row in output_list:
                f.write(row + '\n')

            # if ((total_time_obj - current_time_obj).total_seconds() <= 3):
                # break


        # print output_list
        # with open('results.txt', 'a') as f:
        #     for row in output_list:
        #         f.write(row + '\n')

            # time.sleep(1)


        # time.sleep(10)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(YoutubeAndroidTest)
    unittest.TextTestRunner(verbosity=1).run(suite)
