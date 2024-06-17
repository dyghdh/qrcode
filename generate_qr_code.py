import qrcode

# QR 코드 생성
data = "출석체크: 유저 고유 ID 또는 이벤트 ID"
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

# QR 코드 이미지 생성
img = qr.make_image(fill='black', back_color='white')
img.save("attendance_qr.png")
