import logging
import random
import time

import logzero
from logzero import logger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SeleniumDefault:
    """ Skeleton for apps using Selenium. Frequently needed shortcuts are available in here.
    """

    def __init__(self, driver_path='chromedriver', loglevel='error'):
        """Instanciate the class needs to feed a selenium driver.
           (Development realized on macOS Catalina + Chrome)
        
        PARAMETERS:
            - driver_path : str - path to the selenium driver (mandatory)
            - loglevel    : str - [debug/info/warning/error] (default is error). Adapt the level of information displayed in terminal.
        """

        self.url = None
        self.original_window = None
        self.display_sleep_time = False

        self.driver_path = driver_path
        self.create_driver()
        self.set_loglevel(loglevel)

    def create_driver(self):
        """Instanciate 
        """

        logger.info(self.driver_path)
        self.driver = webdriver.Chrome(self.driver_path)  # TODO:check path

    def connect_to_url(self, url):
        """ Redirect the webpage to a new url.
        PARAMETERS:
            - url : str - webpage to visit with webdriver.
        """
        self.url = url
        self.load_url()

    def load_url(self, sleep=3):
        """Instantiate a new driver instance.

        PARAMETERS:
            - sleep : int - number of waiting seconds after instantiating driver. Default is 3.
        """

        self.driver.get(self.url)
        self.original_window = self.driver.window_handles[0]
        self.sleep(sleep, 'Load url : {}'.format(self.url))

    def paste_clipboard(self, element):
        """
        Copy clipboard content into the selected element
        :param element: string
        """
        element.send_keys(Keys.SHIFT, Keys.INSERT)

    def scroll_to_element(self, elmt, sleep=1):
        """Scroll to any defined element on the webpage (essentially to make it clickcable).
        
        PARAMETERS:
            - elmt : selenium element - element to scroll to
            - sleep : int - number of waiting seconds after scrolling. Default is 1.
        """

        y = elmt.location['y']
        logger.debug('scrolling to y={}'.format(y))
        y = y - 150
        self.driver.execute_script("window.scrollTo(0, {})".format(y))
        self.sleep(sleep)

    def sleep(self, sleep=1, message='Wait', exact=False):
        """ Sleeping function : as web pages might take time to react, it is interesting to wait for their responses.
            To introduce noise the time value is slightly modified around the desired value.
        PARAMETERS:
            - sleep   : int - number of waiting seconds. Default is 1.
            - message : message to display in terminal (in addition to the waiting time). Displayed only when loglevel is debug or info.
            - exact   : boolean - To use the exact waiting value. Default is False: random noise of max 0.5s and minimum waiting time is 1s.
        """

        if self.display_sleep_time:
            logger.debug('({} s.) - {}'.format(sleep, message))

        if not exact:
            noise = random.random() - 0.5
            sleep = max(sleep + noise, 1)
        time.sleep(sleep)

    def close_driver(self):
        """ Close the driver instance and the window associated.
            Might be useful in case of bug or wrong instanciation.
        """

        logger.info('Exit navigation.')
        self.driver.quit()

    def set_loglevel(self, level):
        """ Adapting the loglevel for information display through process.

        PARAMETERS:
            - loglevel : str - [debug/info/warning/error]
        """
        level_table = {
            'debug': logging.DEBUG,
            'warn': logging.WARNING,
            'warning': logging.WARNING,
            'info': logging.INFO,
            'error': logging.ERROR
        }
        loglevel = level_table[level.lower()]
        logzero.loglevel(loglevel)
