from urllib.parse import quote

pay_url = "https://qr.alipay.com/fkx17629ee8clivc1hn8kc8"
# 如果想要赞助我，可以扫码上方链接
if not pay_url.endswith('?noT=ntagtqp'):
    pay_url += '?noT=ntagtqp'

# 定义固定的页面数据
fixed_pages = {
    'Page 0': '1D 6E 74 8F',
    'Page 1': '9A 95 00 00',
    'Page 2': '0F A3 FF FF',
    'Page 3': 'E1 10 3E 00',
    'Page 4': '03 FF 00 FF',
    'Page 5': '91 01 CE 55',
    # Page 130 - Page 134
    'Page 130': 'FF FF FF BD',
    'Page 131': '00 00 00 04',
    'Page 132': '00 00 00 00',
    'Page 133': '00 00 00 00',
    'Page 134': '00 00 00 00',
}

# 定义要插入的URL，从Page 6开始
scheme = f"alipay://nfc/app?id=10000007&actionType=route&codeContent={quote(pay_url, 'utf-8')}"
url = f"render.alipay.com/p/s/ulink/?scene=nfc&scheme={quote(scheme, 'utf-8')}"

print(url)


# 将URL转换为字节数组，按照NFC NDEF格式进行编码
def encode_ndef_uri(uri):
    uri_bytes = uri.encode('utf-8')
    ndef_message = [0x04] + list(uri_bytes)
    return ndef_message


# 插入的二进制数据
binary_data_hex = (
    "54 0F 1B 61 6E 64 72 6F 69 64 2E 63 6F 6D 3A 70 6B 67 63 6F 6D 2E 65 67 2E "
    "61 6E 64 72 6F 69 64 2E 41 6C 69 70 61 79 47 70 68 6F 6E 65 FE"
)
binary_data = [int(byte, 16) for byte in binary_data_hex.split()]

# 将NDEF消息和二进制数据合并
ndef_message = encode_ndef_uri(url) + binary_data

# 将数据分割成每页4个字节
pages = {}
page_number = 6  # 从Page 6开始
for i in range(0, len(ndef_message), 4):
    page_data = ndef_message[i:i + 4]
    # 如果不足4字节，用0x00填充
    while len(page_data) < 4:
        page_data.append(0x00)
    page_hex = ' '.join(f"{byte:02X}" for byte in page_data)
    pages[f"Page {page_number}"] = page_hex
    page_number += 1

# 合并所有页面数据
all_pages = {}
# 添加固定的页面数据
for page in range(0, 6):
    key = f"Page {page}"
    all_pages[key] = fixed_pages.get(key, '00 00 00 00')
# 添加生成的页面数据
all_pages.update(pages)
# 添加尾部固定页面数据
for page in range(130, 135):
    key = f"Page {page}"
    all_pages[key] = fixed_pages.get(key, '00 00 00 00')


# 生成最终的数据文件内容
def generate_data_file():
    lines = []
    lines.append("Filetype: Flipper NFC device")
    lines.append("Version: 4")
    lines.append(
        "# Device type can be ISO14443-3A, ISO14443-3B, ISO14443-4A, ISO14443-4B, ISO15693-3, FeliCa, NTAG/Ultralight, Mifare Classic, Mifare Plus, Mifare DESFire, SLIX, ST25TB, EMV")
    lines.append("Device type: NTAG/Ultralight")
    lines.append("# UID is common for all formats")
    lines.append("UID: 1D 6E 74 9A 95 00 00")
    lines.append("# ISO14443-3A specific data")
    lines.append("ATQA: 00 44")
    lines.append("SAK: 00")
    lines.append("# NTAG/Ultralight specific data")
    lines.append("Data format version: 2")
    lines.append("NTAG/Ultralight type: NTAG215")
    lines.append(
        "Signature: 1D 6E 74 8F 9A 95 00 00 1D 6E 74 8F 9A 95 00 00 1D 6E 74 8F 9A 95 00 00 1D 6E 74 8F 9A 95 00 00")
    lines.append("Mifare version: 00 04 04 02 01 00 11 03")
    lines.append("Counter 0: 0")
    lines.append("Tearing 0: 00")
    lines.append("Counter 1: 0")
    lines.append("Tearing 1: 00")
    lines.append("Counter 2: 0")
    lines.append("Tearing 2: 00")
    lines.append("Pages total: 135")
    pages_read = max(int(page.split()[1]) for page in all_pages.keys()) + 1
    lines.append(f"Pages read: 133")
    # 添加页面数据
    for page_num in range(0, pages_read):
        key = f"Page {page_num}"
        page_data = all_pages.get(key, '00 00 00 00')
        lines.append(f"{key}: {page_data}")
    lines.append("Failed authentication attempts: 0")
    return '\n'.join(lines)


# 将数据写入文件
with open('Alipay-nfcPay.flipper0.nfc', 'w', encoding='utf-8') as f:
    data_file_content = generate_data_file()
    f.write(data_file_content)
    print("数据文件已生成：Alipay-nfcPay.flipper0.nfc")

# 打印生成的部分数据用于验证
print("\n生成的部分页面数据：")
for page_num in range(6, 10):
    key = f"Page {page_num}"
    print(f"{key}: {all_pages.get(key)}")
