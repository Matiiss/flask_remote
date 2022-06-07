from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk
from gui.settings import info_about, font, win_w_h
from getaddr import get_hostname_ip
from app import app, ServerThread
from getaddr.generate_qr import save_code
import secrets
import os
import logging as log


class MainWindow(Tk):
    def __init__(self):
        log.info('Started initialising MainWindow')
        Tk.__init__(self)

        self.title('Remote Control')
        self.iconphoto(True, ImageTk.PhotoImage(Image.open(os.getcwd() + '/gui/icon.ico')))
        log.info('Inherited, set title and icon')

        self.width, self.height = win_w_h
        self.screen_middle_x = self.winfo_screenwidth() // 2
        self.screen_middle_y = self.winfo_screenheight() // 2
        self.geometry(f'{self.width}x{self.height}'
                      f'+{self.screen_middle_x - self.width // 2}'
                      f'+{self.screen_middle_y - self.height // 2}')
        self.resizable(False, False)
        log.info('Window geomtery set')
        self.protocol('WM_DELETE_WINDOW', self.close)
        log.info('Assigned a protocol')

        self.info_frame = Frame(self, bd=2, relief='solid', padx=5, pady=5)
        self.info_frame.pack(padx=10, pady=10)
        self.pack_info(self.info_frame)
        log.info('Created info frame for main info')
        self.btn = Button(self, text='Start Session', command=self.start_session, font=font, bd=5)
        self.btn.pack(expand=True, ipadx=10, ipady=10)

        self.server = None
        log.info('Added main button and set self.server to None')

    @staticmethod
    def pack_info(parent):
        for index, info in enumerate(info_about):
            Label(parent, text=info, font=font).grid(row=index, column=0, sticky='w', pady=5)
        log.info('Placed info in the info frame')

    def start_session(self):
        log.info('Session method called')
        _, ip = get_hostname_ip()
        port = 5000
        pin = secrets.token_hex(8)
        address = f'http://{ip}:{port}/start_session/{pin}'
        filename = save_code(address)
        log.info(f'Generated address ({address}) and QR code')
        with open(os.getcwd() + '/app/static/' + 'checker_file.txt', 'w') as file:
            file.write(pin)
        log.info(f'PIN written to file, PIN: {pin}')
        self.server = ServerThread(app, ip, port, daemon=True)
        self.server.start()
        log.info('ServerThread started...')
        self.show_session_info(filename)
        self.btn.config(text='Stop Session', command=self.stop_session)
        log.info('Done starting the server')

    def show_session_info(self, filename):
        log.info('Called show_session_info()')
        info_frame = Frame(self)
        info_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='c')

        info_frame.image = ImageTk.PhotoImage(Image.open(filename))
        Label(info_frame, image=info_frame.image).pack()
        Button(info_frame, text='Close', command=info_frame.destroy, font=font).pack()
        log.info('Info placed after show_session_info()')

    def stop_session(self):
        log.info('Called stop_session()')
        info_frame = Frame(self)
        info_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='c')
        self.server.shutdown()
        Label(info_frame, text='Session Stopped', font=font).pack(expand=True)
        self.btn.config(text='Start Session', command=self.start_session)
        self.after(2000, info_frame.destroy)
        log.info('session shutdown')

    def close(self):
        if self.server:
            self.server.shutdown()
            log.info('Server shut down')
        self.destroy()
        log.info('MainWindow closed')


if __name__ == '__main__':
    root = MainWindow()
    root.mainloop()
