import qrcode
import os


def generate_qr_code(url):
    img = qrcode.make(url)
    return img


def save_code(url):
    img = generate_qr_code(url)
    filename = os.getcwd() + '/app/static/temp_qr' + '.png'
    img.save(filename)
    return filename


# if __name__ == '__main__':
#     show_code('random_stuff.com')
