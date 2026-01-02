import qrcode
from PIL import Image

url = input("Digite a URL: ").strip()

file_path = "qrcode.png"  # salva na mesma pasta do arquivo

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)

qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save(file_path)

img.show()  # 👈 abre o QR Code na tela

print("QR Code gerado com sucesso!")
