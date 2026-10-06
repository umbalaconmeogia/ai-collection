# rinri-kaikin — thống kê 皆勤賞 / もう少し賞 モーニングセミナー

Thống kê hàng tháng những người 自単会 được 皆勤賞 (dự đủ mọi buổi) và もう少し賞 (vắng đúng 1 buổi)
của モーニングセミナー 倫理法人会.

## Quy trình

1. Vào **RinriApp**, download 参加者情報 (file CSV) của tháng cần thống kê.
   Lưu vào thư mục tháng, ví dụ:
   `my-ai-brain-files/associations/rinri-houjinkai/minurin/202609.モーニングセミナー/参加履歴情報_202609.csv`
2. Chạy skill: trong Claude Code gõ `/rinri-kaikin` kèm đường dẫn file và tháng, hoặc chạy trực tiếp:

   ```bash
   python ~/.claude/skills/rinri-kaikin/scripts/kaikin.py "<đường dẫn csv>" 202609
   ```

   Tháng nhận `202609`, `2026/09` hoặc `2026-09`.

## Kết quả

Đúng 2 dòng, tên = 姓 + " " + 名, cách nhau bởi " , ":

```
皆勤賞（x人）：姓 名 , 姓 名
もう少し賞（y人）：姓 名 , 姓 名
```

## Quy tắc tính

- Buổi = các ngày distinct trong cột `開催日` thuộc tháng chỉ định, tính trên mọi dòng (kể cả 他単会, 非会員).
- Chỉ xét dòng có `区分` chứa `自単会`.
- Nhận diện người theo 姓 + 名 (bỏ khoảng trắng), không dùng `法人会員番号` vì số này dùng chung cho cả công ty.
- Mỗi người mỗi ngày đếm 1 lần.

## Cấu trúc

- `SKILL.md` — hướng dẫn cho Claude khi skill được kích hoạt
- `scripts/kaikin.py` — script thống kê
- `README.md` — file này
