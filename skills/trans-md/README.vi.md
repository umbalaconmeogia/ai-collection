[English](README.md) | [Tiếng Việt](README.vi.md) | [日本語](README.ja.md)

# /trans-md Skill

Skill này giúp bạn dịch các tài liệu Markdown đa ngôn ngữ một cách tự động và chuyên nghiệp, hỗ trợ cả dịch thuận và dịch ngược (về file gốc).

## Cách sử dụng

Bạn có thể gọi skill này bằng cách sử dụng slash command hoặc yêu cầu trực tiếp:

### Cú pháp
`/trans-md <source-lang> <target-1> [<target-2>] [<file-path>]`

### 1. Dịch thuận (Tạo file vệ tinh có suffix)
Dịch từ một file sang các ngôn ngữ khác với hậu tố `.[lang].md`.
- `/trans-md vi en ja` (Dịch README.md từ Việt sang Anh và Nhật)
- `/trans-md en vi docs/api-guide.md` (Dịch file api-guide.md từ Anh sang Việt)

### 2. Dịch ngược (về file Base)
Sử dụng từ khóa **`base`** để dịch một file có suffix về file gốc không có suffix.
- `/trans-md vi base mydoc.vi.md`
  - Đầu vào: `mydoc.vi.md`
  - Đầu ra: `mydoc.md` (Nội dung tiếng Anh/Mặc định)

### 3. Kết hợp cả hai
Bạn có thể cập nhật file gốc và tạo file vệ tinh cùng lúc:
- `/trans-md vi base ja mydoc.vi.md`
  - Cập nhật đồng thời: `mydoc.md` và `mydoc.ja.md`.

## Tính năng nổi bật
- **Smart Naming**: Tự động nhận diện và xử lý hậu tố file (`.vi.md`, `.ja.md`, ...).
- **Language Switcher**: Tự động chèn/cập nhật thanh chuyển đổi ngôn ngữ ở đầu trang.
- **Code Integrity**: Bảo toàn tuyệt đối nội dung trong các khối code.
- **Deep Linking**: Cập nhật liên kết giữa các tài liệu nếu có bản dịch tương ứng.
