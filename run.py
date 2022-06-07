from gui import MainWindow
import logging


if __name__ == '__main__':
    logging.basicConfig(filename='latest_log.log', filemode='w', level=logging.INFO)
    MainWindow().mainloop()
