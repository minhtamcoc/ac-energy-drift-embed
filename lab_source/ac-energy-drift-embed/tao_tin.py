import cv2
import os

# =============================
# CONFIG
# =============================
VIDEO_IN = "input.mp4"
VIDEO_OUT = "output.avi"
SECRET_FILE = "secret.txt"

# Magic để extractor biết đúng video có giấu tin
MAGIC = b"STEGOVID"

# =============================
# BYTES -> BITS
# =============================
def bytes_to_bits(data: bytes) -> str:
    bits = ""
    for byte in data:
        bits += format(byte, "08b")
    return bits


def bits_to_bytes(bits: str) -> bytes:
    out = bytearray()

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) == 8:
            out.append(int(byte, 2))

    return bytes(out)


# =============================
# MAIN EMBED
# =============================
def main():
    if not os.path.exists(VIDEO_IN):
        print(f"[!] Không thấy video input: {VIDEO_IN}")
        return

    if not os.path.exists(SECRET_FILE):
        print(f"[!] Không thấy file secret: {SECRET_FILE}")
        return

    with open(SECRET_FILE, "rb") as f:
        secret_data = f.read()

    # Payload format:
    # MAGIC 8 bytes + LENGTH 4 bytes + SECRET DATA
    #
    # LENGTH là độ dài secret theo byte, lưu dạng big-endian 4 bytes
    payload = MAGIC + len(secret_data).to_bytes(4, "big") + secret_data
    payload_bits = bytes_to_bits(payload)

    cap = cv2.VideoCapture(VIDEO_IN)

    if not cap.isOpened():
        print("[!] Không mở được video input")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Mỗi pixel giấu 1 bit vào LSB kênh Blue
    capacity_bits = w * h * total_frames

    print(f"[*] Video: {w}x{h}, frames={total_frames}, fps={fps}")
    print(f"[*] Capacity: {capacity_bits} bits / {capacity_bits // 8} bytes")
    print(f"[*] Payload: {len(payload_bits)} bits / {len(payload)} bytes")

    if len(payload_bits) > capacity_bits:
        print("[!] Secret quá dài, video không đủ chỗ để giấu")
        cap.release()
        return

    # Dùng FFV1 lossless để không làm hỏng LSB
    fourcc = cv2.VideoWriter_fourcc(*"FFV1")
    out = cv2.VideoWriter(VIDEO_OUT, fourcc, fps, (w, h), True)

    if not out.isOpened():
        print("[!] Không tạo được video output với codec FFV1")
        print("[!] Thử đổi VIDEO_OUT = 'output.mkv' rồi chạy lại")
        cap.release()
        return

    bit_idx = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # frame dạng BGR
        for y in range(h):
            for x in range(w):
                if bit_idx >= len(payload_bits):
                    break

                bit = int(payload_bits[bit_idx])

                # Nhúng vào LSB kênh Blue
                frame[y, x, 0] = (frame[y, x, 0] & 0b11111110) | bit

                bit_idx += 1

            if bit_idx >= len(payload_bits):
                break

        out.write(frame)

    cap.release()
    out.release()

    print("[+] DONE EMBED")
    print(f"[+] Đã nhúng {bit_idx} bits")
    print(f"[+] Output: {VIDEO_OUT}")


if __name__ == "__main__":
    main()