import sys
from PyQt6.QtWidgets import QApplication
from Screenshot import Screenshot
from AI import AI
from Screen import Screen
import ctypes
import logging
import configparser


logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

if __name__ == '__main__':

    logging.info("--- START APLIKACJI ---")

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception as e:
        logging.error(f"--- ctype ERROR --- \n\t{e}")
        pass

    app = QApplication(sys.argv)

    try:
        cfg = configparser.ConfigParser()
        cfg.read("config.conf", encoding="utf-8")
        dots_opacity = cfg.getint('Screen', 'dots_opacity')
        dot_radius = cfg.getint('Screen', 'dot_radius')
        hot_key = cfg.get('HotKeys', 'hot_key')
        clear_key = cfg.get('HotKeys', 'clear_key')
        file_name = cfg.get('Screenshot', 'file_name')
        logging.info("configparser readed")

    except Exception as e:
        logging.error(f"--- configparser ERROR --- \n\t{e}")
        dots_opacity = 122
        dot_radius = 5
        hot_key = "shift"
        clear_key = "f4"
        file_name = "test"

    sc = Screen(dots_opacity, dot_radius)
    sc.show()

    def handle_ai_response(response):
        sc.ai_signal.emit(response.text)

    def on_screenshot_taken(file_path):
        sc.clear_signal.emit()
        gem.received_last_photo(file_path)

    def manual_clear():
        sc.clear_signal.emit()

    gem = AI("gemini-3.6-flash", "ss", handle_ai_response)
    ss = Screenshot("ss",
                    hot_key,
                    clear_key,
                    file_name,
                    on_screenshot_taken=on_screenshot_taken,
                    on_clear_requested=manual_clear)

    ss.start(blocking=False)

    sys.exit(app.exec())