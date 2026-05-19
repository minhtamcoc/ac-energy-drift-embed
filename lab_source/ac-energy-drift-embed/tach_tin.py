import cv2
import os

# =============================
# CONFIG
# =============================
VIDEO = "output.avi"

MAGIC = b"STEGOVID"
HEADER_SIZE = len(MAGIC) + 4  # MAGIC 8 bytes + LENGTH 4 bytes


# =============================
# BITS -> BYTES
# =============================
def bits_to_bytes(bits: str) -> bytes:
    out = bytearray()

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]

        if len(byte) == 8:
            out.append(int(byte, 2))

    return bytes(out)


# =============================
# Bit stream generator
# Đọc bit liên tục, không bị nhảy frame
# =============================
def bit_stream_from_video(cap):
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        h, w, _ = frame.shape

        for y in range(h):
            for x in range(w):
                # Lấy LSB kênh Blue
                bit = frame[y, x, 0] & 1
                yield str(bit)


# =============================
# Đọc n bit từ generator
# =============================
def read_n_bits(bit_gen, n_bits: int) -> str:
    bits = ""

    for _ in range(n_bits):
        try:
            bits += next(bit_gen)
        except StopIteration:
            break

    return bits


# =============================
# MAIN EXTRACT
# =============================
def main():
    if not os.path.exists(VIDEO):
        print(f"[!] Không thấy video: {VIDEO}")
        return

    cap = cv2.VideoCapture(VIDEO)

    if not cap.isOpened():
        print("[!] Không mở được video")
        return

    bit_gen = bit_stream_from_video(cap)

    # Bước 1: đọc header
    # Header = MAGIC + LENGTH
    header_bits_needed = HEADER_SIZE * 8
    header_bits = read_n_bits(bit_gen, header_bits_needed)

    if len(header_bits) < header_bits_needed:
        print("[!] Không đọc đủ header")
        cap.release()
        return

    header = bits_to_bytes(header_bits)

    magic = header[:len(MAGIC)]
    msg_len_bytes = header[len(MAGIC):len(MAGIC) + 4]

    if magic != MAGIC:
        print("[!] Video này không có magic hợp lệ")
        print("[!] Có thể video bị nén lại hoặc không phải output từ tao_tin.py")
        cap.release()
        return

    msg_len = int.from_bytes(msg_len_bytes, "big")
    msg_bits_needed = msg_len * 8

    # Bước 2: đọc tiếp message ngay sau header
    # Quan trọng: dùng cùng bit_gen nên không bị nhảy frame
    msg_bits = read_n_bits(bit_gen, msg_bits_needed)

    cap.release()

    if len(msg_bits) < msg_bits_needed:
        print("[!] Không đọc đủ message")
        return

    secret_data = bits_to_bytes(msg_bits)

    try:
        secret_text = secret_data.decode("utf-8")
    except UnicodeDecodeError:
        secret_text = secret_data.decode("utf-8", errors="replace")

    print("===== SECRET MESSAGE =====")
    print(secret_text)
    print("==========================")


if __name__ == "__main__":
    main()