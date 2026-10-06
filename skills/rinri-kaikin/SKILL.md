---
name: rinri-kaikin
description: Thống kê 皆勤 (dự đủ mọi buổi) và もう少し賞 (vắng đúng 1 buổi) của モーニングセミナー 倫理法人会 trong một tháng chỉ định, từ file CSV 参加履歴情報 tải về từ hệ thống. Chỉ xét người có 区分 chứa 自単会. Dùng skill này khi user đưa file CSV 参加履歴情報 / lịch sử tham gia モーニングセミナー và muốn biết ai 皆勤, ai もう少し賞, ai đi đủ, thống kê chuyên cần theo tháng, hoặc gõ /rinri-kaikin.
---

# /rinri-kaikin — thống kê 皆勤 / もう少し賞 モーニングセミナー

## Tham số

1. **Đường dẫn file CSV** 参加履歴情報 (UTF-8 BOM hoặc cp932, header tiếng Nhật).
2. **Tháng**: `202609`, `2026/09` hoặc `2026-09`.

Nếu user chỉ đưa file mà không nói tháng, suy ra từ tên file (vd `参加履歴情報_202609.csv`)
hoặc từ dữ liệu; nếu file chứa nhiều tháng và không rõ, hỏi lại.

## Cách chạy

```bash
python ~/.claude/skills/rinri-kaikin/scripts/kaikin.py "<csv_path>" <month>
```

Script in ra đúng 2 dòng, tên người = 姓 + " " + 名, các tên cách nhau bởi " , ":

```
皆勤賞（x人）：姓 名 , 姓 名
もう少し賞（y人）：姓 名 , 姓 名
```

Trả cho user **nguyên văn 2 dòng đó**, không thêm bảng hay giải thích, trừ khi user hỏi thêm.

## Quy tắc nghiệp vụ (đã cài trong script, đừng làm khác)

- **Buổi** = các ngày distinct trong cột `開催日` (fallback `開始日`) thuộc tháng chỉ định,
  tính trên toàn bộ dòng kể cả 他単会/非会員 — để không bỏ sót buổi mà không ai 自単会 dự.
- **Đối tượng**: chỉ dòng có `区分` chứa `自単会` (vd `会員（自単会）`).
- **Nhận diện người theo 姓+名** sau khi bỏ mọi khoảng trắng half/full-width.
  **Không** dùng `法人会員番号`: số này là mức 法人, nhiều người cùng công ty dùng chung
  (vd 須賀/野口, 清水俊佑/清水良朗 tại ミヌリン) và đôi khi để trống.
- Mỗi người mỗi ngày đếm 1 lần (hệ thống có thể xuất trùng dòng).
- 皆勤 = số ngày dự == số buổi; もう少し賞 = số buổi − 1.

## Lưu ý khi báo cáo

- Nêu rõ số buổi và ngày các buổi, vì tháng có ngày lễ (vd 秋分の日) sẽ ít buổi hơn.
- Nếu thấy tên gần giống nhau nhưng khác khoảng trắng/ký tự (script đã chuẩn hoá khoảng
  trắng, nhưng không chuẩn hoá chữ khác), nhắc user kiểm tra.
- Kết quả là thống kê tra cứu; không tự ghi vào vault trừ khi user yêu cầu.
