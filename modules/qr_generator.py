import qrcode
import time

from PIL import Image, ImageOps

def create_qr(dirname, link, config):
    inpic_s = 100
    robonomics = Image.open(dirname + '/media/robonomics.jpg').resize((inpic_s,inpic_s))
    qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr_big.add_data('https://' + link)
    qr_big.make()
    img_qr_big = qr_big.make_image().convert('RGB')

    pos = ((img_qr_big.size[0] - robonomics.size[0]) // 2, (img_qr_big.size[1] - robonomics.size[1]) // 2)

    qr_s = 200
    border_s = int((696 - qr_s)/2)
    img_qr_big.paste(robonomics, pos)
    img_qr_big = img_qr_big.resize((qr_s, qr_s))
    img_qr_big = ImageOps.expand(img_qr_big,border=border_s,fill='white')
    left, top, right, bottom = 0, border_s-2, qr_s+border_s*2, border_s+qr_s+2
    img_qr_big = img_qr_big.crop((left, top, right, bottom))

    if config['print_qr']['logos']:
        left_pic = Image.open(dirname + '/media/left_pic.jpg').resize((qr_s,qr_s))
        posl = (24, 2)
        img_qr_big.paste(left_pic, posl)

        right_pic = Image.open(dirname + '/media/right_pic.jpg').resize((qr_s,qr_s))
        posr = (696-qr_s-24, 2)
        img_qr_big.paste(right_pic, posr)

    qrpic = dirname + "/output/" + time.ctime(time.time()).replace(" ", "_") + 'qr.png'
    img_qr_big.save(qrpic)

    return qrpic