"""
Automatically translate all text files given in the text-input folder.
Optionally, a term dictionary may be applied before translation begins.

21.01.2021
"""

import json
import logging
import time
import sys
import clipboard
import logzero
from logzero import logger
from pynput.keyboard import Listener

import paste_selenium

def on_press_show_key(key):
    """
    For showing the user what the key code is.
    :param key: given by pynput
    """
    print(f"{key} pressed")

def on_press(key):
    """
    Execute given function if the key matches the required key
    """
    try:
        if key.char.upper() == (cfg_cb_key_c.upper()):
            logger.info("Clearing clipboard memory.")
            global browser
            browser.clear_input(cfg_web_anchor)
    except AttributeError:
        pass

def clipboard_get_new(delay):
    """
    Wait indefinitely until clipboard updates.
    :param delay: sleep time in s before next check
    :return: string clipboard data
    """
    old_value = clipboard.paste()
    while True:
        time.sleep(delay)
        if old_value != clipboard.paste():
            return clipboard.paste()


def set_loglevel(level):
    """
    :param level: string in level_table
    """
    level_table = {
        'debug': logging.DEBUG,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'error': logging.ERROR
    }
    log_level = level_table[level.lower()]
    logzero.loglevel(log_level)


if __name__ == "__main__":
    # Load config, restore if necessary
    config = {}
    try:
        with open("..\\config.json") as config_file:
            config = json.load(config_file)
            print("Loading config.json")

    except (OSError, ValueError):
        logger.warning("WARNING: config.json missing or corrupted. Restoring defaults.")
        config = {
            "website_url": "https://www.deepl.com/en/translator",
            "website_anchor": "div.lmt__inner_textarea_container textarea",
            "clipboard_accumulate": True,
            "clipboard_key_clear": "q",
            "clipboard_wait_time_s": 0.5,
            "suppress_errors": False,
            "logging": "info",
            "help_show_key_code": False
        }
        try:
            with open("..\\config.json", 'w', encoding="utf-8") as outfile:
                json.dump(config, outfile, indent=4, ensure_ascii=False)
        except OSError:
            logger.error("Could not restore config!")
    # End try

    # Load config
    cfg_web_url     = config["website_url"]
    cfg_web_anchor  = config["website_anchor"]
    cfg_cb_acc      = config["clipboard_accumulate"]
    cfg_cb_key_c    = config["clipboard_key_clear"]
    cfg_cb_wait     = config["clipboard_wait_time_s"]
    cfg_suppress    = config["suppress_errors"]
    cfg_loglevel    = config["logging"]
    cfg_help_key    = config["help_show_key_code"]
    set_loglevel(cfg_loglevel)

    logger.info("Starting...")

    if cfg_help_key:
        listener = Listener(on_press=on_press_show_key)
    else:
        listener = Listener(on_press=on_press)
    listener.start()

    # Open browser
    browser = paste_selenium.SeleniumPaste(driver_path='../chromedriver', loglevel=cfg_loglevel)
    browser.connect_to_url(cfg_web_url)

    # Continuously read the clipboard and paste it into website
    while True:
        logger.info("Waiting for clipboard update...")
        clipboard_text = clipboard_get_new(cfg_cb_wait)

        # Stop if word copied is "stop"
        if clipboard_text[0].upper() == "STOP":
            print("Halting...")
            browser.close_driver()
            sys.exit()

        if not cfg_cb_acc:
            browser.clear_input()
            browser.sleep(0.5)

        browser.paste_in_site(clipboard_text, cfg_web_anchor)

