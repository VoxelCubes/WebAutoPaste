import clipboard
from default_selenium import SeleniumDefault


class SeleniumPaste(SeleniumDefault):
    """ Using Selenium to paste clipboard data into a website."""

    def __init__(self, **kwargs):

        super(SeleniumPaste, self).__init__(**kwargs)
        self.sleep(2, 'Opening browser.')
        self.display_sleep_time = True

    def paste_in_site(self, text, anchor):
        input_area = self.driver.find_element_by_css_selector(anchor)
        clipboard.copy(text)
        self.paste_clipboard(input_area)

    def clear_input(self, anchor):
        input_area = self.driver.find_element_by_css_selector(anchor)
        input_area.clear()
