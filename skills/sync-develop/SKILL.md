---
name: sync-develop
description: >-
  Đồng bộ nhánh làm việc hiện tại với nhánh đích (mặc định develop) trong repo đang làm việc: merge
  origin/<đích> vào nhánh hiện tại, commit toàn bộ thay đổi (kể cả file mới chưa add), push nhánh,
  rồi merge nhánh vào <đích> và push <đích>. Dùng khi người dùng gọi /sync-develop,
  /sync-develop <branch> (vd /sync-develop main), hoặc bảo "merge develop, commit, push, merge vào
  develop". Các skill khác (vd /debt-complete) gọi lại quy trình này.
argument-hint: "[branch] [commit message]"
---

# /sync-develop — merge nhánh đích ↔ nhánh hiện tại + push

Gọi skill này **là** cho phép commit toàn bộ, merge vào nhánh đích và push hai nhánh. Không hỏi lại
những việc đó; chỉ dừng ở các điểm dừng ghi bên dưới. **Không bao giờ** force push, `reset --hard`,
hay tự giải conflict.

Skill là global, không gắn với repo nào: mỗi lần gọi phải xác định `<repo>` và `<đích>` ở bước 0.
Mọi lệnh git bên dưới chạy trong `<repo>` (`git -C <repo> …` nếu thư mục hiện hành không nằm trong nó).

## Bước 0 — Xác định repo và nhánh đích

**`<repo>`** — theo thứ tự:

1. Người dùng (hoặc skill gọi tới) nêu rõ repo → dùng repo đó.
2. Thư mục hiện hành nằm trong một git repo (`git rev-parse --show-toplevel` thành công) → repo đó.
3. Thư mục hiện hành chỉ là thư mục cha chứa nhiều repo → lấy repo mà phiên này đang làm việc
   (repo chứa các file vừa đọc/sửa, nơi vừa chạy lệnh). Xác nhận bằng
   `git -C <repo> rev-parse --show-toplevel`.
4. Không rõ, hoặc phiên này đã sửa file ở **nhiều hơn một** repo → **dừng**, hỏi repo nào.
   Mỗi lần gọi chỉ xử lý **một** repo.

**`<đích>`** và commit message — tách từ `$ARGUMENTS` (sau `git fetch origin`):

- Rỗng → `<đích>` = `develop`, không có message.
- Token đầu tiên là tên nhánh có trên remote
  (`git show-ref --verify --quiet refs/remotes/origin/<token>`) → `<đích>` = token đó; phần còn lại
  (nếu có) là commit message.
- Ngược lại → `<đích>` = `develop`, toàn bộ `$ARGUMENTS` là commit message. Ngoại lệ: tham số chỉ
  có **một từ** mà không khớp nhánh nào → nhiều khả năng gõ sai tên nhánh → **dừng**, hỏi.
- Skill khác gọi tới thì dùng nhánh/message nó đưa.

`origin/<đích>` không tồn tại → **dừng**, báo (liệt kê `git branch -r`).

## Bước 1 — Kiểm tra

1. `git branch --show-current` → `<nhánh>`.
   - Detached HEAD, hoặc `<nhánh>` = `<đích>` → **dừng**, hỏi.
   - `<nhánh>` là nhánh dài hạn khác (`develop`/`main`/`master`) → **dừng**, xác nhận người dùng
     thật sự muốn merge `<nhánh>` ↔ `<đích>`.
2. `git status --short` — ghi lại danh sách thay đổi hiện có.
3. `git fetch origin` (nếu bước 0 chưa chạy).

## Bước 2 — Merge nhánh đích vào nhánh hiện tại

1. `git rev-list --count HEAD..origin/<đích>` = 0 → bỏ qua bước này (ghi "`<đích>` không có gì mới").
2. `git merge --no-edit origin/<đích>`.
   - Git từ chối vì thay đổi chưa commit sẽ bị ghi đè → làm **bước 3 trước**, rồi merge lại.
   - **Conflict → dừng**: liệt kê file conflict, hỏi người dùng muốn tự giải hay `git merge --abort`.

## Bước 3 — Commit toàn bộ

1. Không có thay đổi (`git status --short` rỗng) → bỏ qua.
2. `git add -A`, rồi `git status --short`.
3. Có file trông như bí mật (`.env`, credential, key, dump DB), file lớn bất thường, hoặc file mà
   repo vốn không track (vd lock file, thư mục build/vendor lọt `.gitignore`) → **dừng**, hỏi.
4. Commit message:
   - Có message từ tham số → dùng nguyên văn (thêm dòng attribution nếu thiếu).
   - Không có → tự soạn từ `git diff --cached`, theo kiểu lịch sử của chính repo đó
     (`git log --oneline -10`); repo chưa có quy ước rõ thì dùng
     `<type>(<scope>): <tóm tắt tiếng Việt>` + 1–3 dòng thân nói thay đổi gì, vì sao.
   - Kết thúc bằng dòng `Co-Authored-By` theo system reminder hiện hành.

## Bước 4 — Push nhánh hiện tại

`git push origin <nhánh>` (chưa có upstream → `git push -u origin <nhánh>`).
Bị từ chối (non-fast-forward) → **không** force; `git fetch`, `git merge --no-edit origin/<nhánh>`
(conflict → dừng), push lại.

## Bước 5 — Merge nhánh vào nhánh đích, push nhánh đích

1. `git checkout <đích>` (chưa có local thì git tự tạo nhánh theo dõi `origin/<đích>`).
2. `git merge --ff-only origin/<đích>` (đưa `<đích>` local về bằng remote). Không ff được — `<đích>`
   local có commit chưa push → **dừng**, báo, quay lại `<nhánh>`.
3. `git merge --no-edit <nhánh>`. Conflict (hiếm, vì bước 2 đã merge `<đích>`) → `git merge --abort`,
   quay lại `<nhánh>`, báo.
4. `git push origin <đích>`. Bị từ chối → **không** force; `git checkout <nhánh>`, quay lại bước 1.
   Bị chặn vì nhánh được bảo vệ (protected branch, cần PR) → **dừng**, quay lại `<nhánh>`, báo.
5. `git checkout <nhánh>` — luôn kết thúc ở nhánh làm việc.

## Báo cáo cuối (tiếng Việt, ngắn)

- Repo và cặp nhánh đã xử lý: `<repo>`, `<nhánh>` ↔ `<đích>`.
- Merge `<đích>`: số commit kéo về (hoặc không có gì mới).
- Commit: hash + tiêu đề; danh sách file đã commit (gom theo thư mục nếu dài).
- Push: `<nhánh>` và `<đích>` — hash cuối của mỗi nhánh.
- Điểm đã dừng (nếu có) và việc người dùng cần làm tiếp.
