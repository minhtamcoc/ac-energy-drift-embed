# Giau tin video bang AC energy drift

## Muc dich

Bai thuc hanh giup sinh vien hieu cach giau va tach tin trong video khi can bao toan du lieu an. Sinh vien se xem thong so video bang `ffmpeg`, chay chuong trinh Python de nhung thong diep vao video, sau do tach lai thong diep tu video da duoc tao.

Trong bai nay, thong diep duoc chuyen thanh chuoi bit va nhung lien tuc vao dong pixel cua video. Chuong trinh ghi video dau ra bang codec lossless FFV1 de han che viec codec nen lam hong bit an.

## Yeu cau doi voi sinh vien

De lam bai lab, sinh vien can nam cac noi dung sau:

(1) Khai niem co ban ve giau tin trong video.

(2) Ly do nen dung video lossless khi tach tin phu thuoc vao bit/he so anh.

(3) Cach doc va chay chuong trinh Python su dung OpenCV.

(4) Cach dung `ffmpeg` de xem thong so video.

## Cau hinh bai lab

Bai lab gom 1 container. Trong container co cac file chinh:

- `input.mp4`: video goc dung de giau tin.
- `secret.txt`: thong diep bi mat can nhung.
- `tao_tin.py`: chuong trinh tao video co tin an.
- `tach_tin.py`: chuong trinh tach lai thong diep tu video da nhung.

Moi truong da cai san:

- Python 3.
- OpenCV.
- NumPy.
- ffmpeg.
- nano.

## Chuan bi moi truong

Tren terminal cua may Labtainer, vao thu muc:

```bash
cd /home/student/labtainer/labtainer-student
```

Tai bai lab:

```bash
imodule https://github.com/minhtamcoc/ac-energy-drift-embed/raw/main/ac-energy-drift-embed.tar.gz
```

Khoi tao bai lab:

```bash
labtainer ac-energy-drift-embed
```

Khi duoc hoi e-mail, sinh vien nhap ma sinh vien cua minh.

## Cac nhiem vu can thuc hien

### Task 1: Xem thong so ky thuat cua video

Muc tieu: xac dinh dinh dang, do phan giai, fps, bitrate va thoi luong cua file `input.mp4`.

Thuc hien lenh:

```bash
ffmpeg -hide_banner -i input.mp4
```

Ghi lai cac thong so quan trong:

- Do phan giai cua video.
- Frame rate.
- Thoi luong video.
- Codec cua video.

### Task 2: Doc va chay chuong trinh giau tin

Mo file `secret.txt` de xem thong diep can giau:

```bash
cat secret.txt
```

Mo file `tao_tin.py` de quan sat cac tham so:

```bash
nano tao_tin.py
```

Trong file nay can chu y:

- `VIDEO_IN = "input.mp4"`: video dau vao.
- `VIDEO_OUT = "output.avi"`: video dau ra.
- `SECRET_FILE = "secret.txt"`: file chua thong diep bi mat.
- `MAGIC = b"STEGOVID"`: dau hieu de chuong trinh tach tin nhan dien video co tin an.

Chay chuong trinh giau tin:

```bash
python3 tao_tin.py
```

Neu thanh cong, man hinh se hien:

```text
DONE EMBED
Output: output.avi
```

Sau buoc nay, file `output.avi` se duoc tao trong thu muc hien tai.

### Task 3: Kiem tra video da nhung tin

Kiem tra file video dau ra:

```bash
ls -lh output.avi
```

Xem thong so cua video vua tao:

```bash
ffmpeg -hide_banner -i output.avi
```

Chu y: khong nen doi `output.avi` sang mp4 bang codec nen thong thuong, vi viec nen lai co the lam hong cac bit da nhung.

### Task 4: Tach lai thong diep bi mat

Mo file `tach_tin.py` de quan sat cach doc lai bit tu video:

```bash
nano tach_tin.py
```

Chay chuong trinh tach tin:

```bash
python3 tach_tin.py
```

Neu thanh cong, chuong trinh se in ra thong diep trong `secret.txt`.

## Kiem tra bai lam

Tu terminal Labtainer, chay:

```bash
checkwork
```

Bai lab co 4 muc cham:

- `cw1`: da chay lenh xem thong so video bang `ffmpeg`.
- `cw2`: da chay `python3 tao_tin.py` va chuong trinh bao `DONE EMBED`.
- `cw3`: chuong trinh giau tin da tao `output.avi`.
- `cw4`: da chay `python3 tach_tin.py` va tach duoc thong diep bi mat.

Ket qua `Y` nghia la muc do da hoan thanh, `N` nghia la muc do chua duoc ghi nhan.

## Ket thuc bai lab

Sau khi lam xong, dung lenh:

```bash
stoplab ac-energy-drift-embed
```

Ket qua bai lam se duoc luu trong thu muc `labtainer_xfer`.

## Khoi dong lai bai lab

Neu can lam lai bai lab tu dau:

```bash
labtainer -r ac-energy-drift-embed
```
