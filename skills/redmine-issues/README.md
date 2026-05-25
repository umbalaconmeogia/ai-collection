# Skill `redmine-issues`

Thư mục này chứa skill Cursor dùng [REST API của Redmine](https://www.redmine.org/projects/redmine/wiki/Rest_api) để tạo/cập nhật issue (kể cả issue con gắn `parent_issue_id`).

| File | Vai trò |
|------|--------|
| `SKILL.md` | Hướng dẫn cho agent (có YAML `description` để Cursor gợi ý khi nào dùng skill). |
| `README.md` | Hướng dẫn cho bạn (cách gắn skill, biến môi trường, lưu ý bảo mật). |
| `.env.example` | Mẫu biến; sao chép thành `.env` rồi điền giá trị thật. |
| `.env` | **Bạn tự tạo** — chứa URL và API key; không commit (đã có `.gitignore`). |

## Cách dùng trong Cursor

1. **Gắn skill vào chat** (Attach skill / Skills) và chọn `redmine-issues`, hoặc nhắc rõ: *tạo issue Redmine*, *parent task #123*, v.v.
2. **Cung cấp thông tin** mà agent cần: project (id hoặc identifier), tracker, tiêu đề/mô tả, id issue cha nếu có. Assignee (担当者) có thể để mặc định trong `.env` (xem mục dưới).
3. Cấu hình URL và API key theo thứ tự ưu tiên trong mục dưới (môi trường process → file `.env` trong thư mục skill → hoặc bạn dán trong chat nếu chấp nhận rủi ro lộ key trong lịch sử).

Agent làm theo `SKILL.md`: **ưu tiên biến môi trường**; nếu thiếu thì **đọc `.env` cùng thư mục với `SKILL.md`** (thường là `~/.cursor/skills/redmine-issues/.env`).

## `REDMINE_BASE_URL` và `REDMINE_API_KEY` đặt ở đâu?

Tên đúng là **`REDMINE_API_KEY`** (không phải `REDMIENE_...`).

### 0. File `.env` trong thư mục skill (fallback khi process chưa có biến)

Thư mục skill (cùng chỗ với `SKILL.md`):

- Windows: `%USERPROFILE%\.cursor\skills\redmine-issues\.env`
- macOS/Linux: `~/.cursor/skills/redmine-issues/.env`

Cách tạo nhanh:

1. Sao chép [`.env.example`](.env.example) thành tên file `.env`.
2. Sửa `REDMINE_BASE_URL` (không `/` cuối), `REDMINE_API_KEY`, và (tuỳ chọn) assignee mặc định.

Nếu trong **môi trường process** đã có biến, giá trị env **ghi đè** cùng key trong `.env` (xem `SKILL.md`).

## Assignee mặc định (owner / 担当者)

Redmine lưu người phụ trách trong trường **`assigned_to_id`** (số). Skill gửi id sau khi resolve (nếu cần) từ login.

| Biến | Bắt buộc | Gợi ý |
|------|----------|--------|
| `REDMINE_DEFAULT_ASSIGNED_TO_LOGIN` | Không | **Nên dùng** — login Redmine, ví dụ `thanh_tt` (dễ đọc, ổn khi copy `.env`) |
| `REDMINE_DEFAULT_ASSIGNED_TO_ID` | Không | Ví dụ `7` — gửi thẳng API, **không** tra login; nếu **cả hai** có trong config thì **id thắng** |

**Thứ tự khi agent tạo/sửa issue:** (1) bạn chỉ định trong prompt → (2) `REDMINE_DEFAULT_ASSIGNED_TO_ID` → (3) `REDMINE_DEFAULT_ASSIGNED_TO_LOGIN` → resolve → (4) không gán (Redmine default).

Ví dụ trong `.env`:

```env
REDMINE_DEFAULT_ASSIGNED_TO_LOGIN=thanh_tt
```

### API key khác assignee

- **`REDMINE_API_KEY`**: xác thực API; user của key thường là **người tạo** issue và **người ghi** khi cập nhật (journal).
- **Assignee**: người **được giao** (`assigned_to`) — cấu hình bằng biến trên hoặc nói rõ trong prompt.

Có thể biết user của API key bằng `GET /users/current.json`, nhưng **không cần** gọi mỗi lần nếu assignee đã cố định trong `.env`.

### Login hay numeric id?

| | Login (`thanh_tt`) | Id (`7`) |
|---|-------------------|----------|
| Trong `.env` | Khuyến nghị | Khi muốn bỏ bước lookup |
| Nhược | Một lần tra id (memberships / users API) | Id có thể khác giữa staging/production |

Chi tiết resolve login → id: **`SKILL.md` → Assignee (owner / 担当者)**.

### 1. Windows — biến môi trường người dùng (khuyến nghị cho dùng lâu dài)

1. Mở **Settings** → **System** → **About** → **Advanced system settings** → **Environment Variables**.
2. Trong **User variables** (hoặc System nếu cần chung máy), **New**:
   - `REDMINE_BASE_URL` = ví dụ `https://redmine.congty.com` (không có `/` cuối).
   - `REDMINE_API_KEY` = key lấy trong Redmine: **My account** → **API access key**.

Đóng mở lại **terminal** (và nếu cần, khởi động lại Cursor) để process mới nhận biến.

### 2. PowerShell — chỉ phiên hiện tại

```powershell
$env:REDMINE_BASE_URL = "https://redmine.example.com"
$env:REDMINE_API_KEY  = "your_api_key_here"
```

Hết cửa sổ terminal là mất (trừ khi bạn thêm vào profile — mục 3).

### 3. PowerShell — tự nạp mỗi khi mở shell (tiện nhưng key nằm trong file profile)

Thêm hai dòng `$env:...` vào profile, ví dụ:

```powershell
notepad $PROFILE
```

**Cảnh báo:** API key lưu dạng plain text trong profile; chỉ nên dùng trên máy cá nhân đã bảo vệ.

### 4. File `.env` của project (không liên quan skill này)

**Cursor không tự** nạp `.env` của repo vào mọi lệnh terminal. Skill chỉ đọc `.env` trong **thư mục `redmine-issues`** (mục 0). Nếu bạn chỉ có `.env` trong project, hãy export biến vào shell hoặc dùng mục 0 / 1.

## Lấy API key trên Redmine

Đăng nhập Redmine → **My account** → mục **API access key** → tạo/copy key. User phải có quyền trên project/tracker cần tạo issue.

## Kiểm tra nhanh (PowerShell)

```powershell
Invoke-RestMethod -Uri "$env:REDMINE_BASE_URL/issues.json?limit=1" -Headers @{ "X-Redmine-API-Key" = $env:REDMINE_API_KEY }
```

Nếu trả về JSON (hoặc 200) là URL và key hợp lệ trong phiên hiện tại.

## Tiếng Nhật / Tiếng Việt bị mojibake (文字化け)

Nguyên nhân thường gặp: body JSON **không được gửi dưới dạng octet UTF-8** (đặc biệt **PowerShell 5.1** + `-Body` là chuỗi), hoặc **chỉ terminal/cmd** hiển thị sai trong khi Redmine trên trình duyệt vẫn đúng.

**Gửi API (bắt buộc khi có chữ Nhật/Việt):**

- Header: `Content-Type: application/json; charset=utf-8`
- **PowerShell:** sau `ConvertTo-Json`, dùng `-Body ([System.Text.Encoding]::UTF8.GetBytes($json))` và `-ContentType 'application/json; charset=utf-8'`. **Cập nhật issue (`PUT`)** cũng áp dụng y hệt.
- **Không** nhét script dài vào `powershell -Command "..."` từ shell khác (dễ mất `$`, sai quote, lệch encoding) — nên lưu **`script.ps1` mã hóa UTF-8** rồi `powershell -NoProfile -File script.ps1`.
- **`curl.exe`:** ghi `payload.json` **UTF-8** (nên **không BOM**), rồi `--data-binary "@payload.json"`.
- Đọc `.env` có Unicode: `Get-Content -Encoding UTF8`.

**Kiểm tra:** sau khi tạo/sửa, mở issue trên web; nếu vẫn nghi ngờ, agent có thể `GET /issues/{id}.json` và đối chiếu `subject` với nội dung mong muốn (xem checklist trong `SKILL.md`).

**Chỉ output terminal bị lỗi:** nếu trên **Redmine web** vẫn đúng → xử lý hiển thị console (`chcp 65001`, Windows Terminal UTF-8, `[Console]::OutputEncoding`), không phải sửa payload API.

**Khuyến nghị:** **PowerShell 7** (`pwsh`) + vẫn nên gửi **byte UTF-8** cho payload lớn có đa ngôn ngữ.

Chi tiết đầy đủ (mẫu code, anti-pattern): **`SKILL.md` → mục UTF-8 / mojibake**.

## Bảo mật

- Không commit file `.env` (thư mục skill có `.gitignore` cho `.env` nếu bạn đưa cả folder vào git).
- Không đưa key vào `SKILL.md` / `README.md` / issue công khai.
- Nếu đã lộ key: vào Redmine tạo lại **API access key** (xoá/rotate key cũ nếu Redmine hỗ trợ).

## Chi tiết kỹ thuật

Xem `SKILL.md` (endpoint, `parent_issue_id`, `assigned_to_id`, assignee mặc định, ví dụ `curl`).
