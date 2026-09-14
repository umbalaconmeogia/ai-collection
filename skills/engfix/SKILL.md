---
name: engfix
description: Thực hiện yêu cầu của user như bình thường, rồi cuối câu trả lời bổ sung một mục ngắn sửa lỗi tiếng Anh trong chính câu yêu cầu đó — sửa tối thiểu, chỉ chạm vào lỗi thật (ngữ pháp, chia động từ, giới từ, mạo từ, dùng từ sai nghĩa), không viết lại cho hoa mỹ. Dùng skill này BẤT CỨ KHI NÀO chuỗi "/engfix" xuất hiện trong tin nhắn của user — ở ĐẦU tin nhắn (dạng slash command "/engfix <yêu cầu>") hoặc ở CUỐI tin nhắn sau phần yêu cầu ("<yêu cầu> /engfix"), hoặc ở giữa. User là người Việt đang tự bổ túc tiếng Anh cơ bản, nên mục sửa lỗi này là phần bắt buộc của câu trả lời, không phải tùy chọn — kể cả khi yêu cầu chính rất dài, phức tạp, hay khi câu tiếng Anh trông đã ổn.
---

# /engfix — làm việc, rồi bổ túc tiếng Anh

User là người Việt, đang chủ động luyện viết tiếng Anh bằng cách viết yêu cầu công việc
bằng tiếng Anh thay vì tiếng Việt. Họ tự nhận tiếng Anh "còn hổng rất nhiều" và muốn
**bổ túc phần nền**, không phải học viết văn hay.

Skill này có hai phần, theo đúng thứ tự:

1. **Thực hiện yêu cầu.** Đây vẫn là việc chính. Làm đầy đủ, đúng chất lượng như mọi khi.
   Sự có mặt của `/engfix` không được làm phần này bị rút ngắn hay xao nhãng.
2. **Sửa tiếng Anh của chính câu yêu cầu đó**, trong một mục ngắn ở cuối câu trả lời.

Bỏ `/engfix` ra khỏi nội dung yêu cầu khi diễn giải — nó là cờ điều khiển, không phải một phần
của việc cần làm. Cũng đừng sửa lỗi ở giữa chừng: user cần câu trả lời cho công việc trước,
phần tiếng Anh là hậu cảnh.

## Nguyên tắc sửa: tối thiểu

Đây là điều dễ làm sai nhất, nên cần hiểu rõ *vì sao*.

Một mô hình ngôn ngữ được yêu cầu "sửa văn bản" sẽ có phản xạ viết lại cho mượt: đổi từ
thường sang từ sang hơn, gộp câu, thêm liên từ, chỉnh nhịp điệu. Với người đang học ở mức
nền, phản xạ đó **phản tác dụng** — bản sửa trả về không còn là câu của họ, họ không nhận ra
mình sai chỗ nào, và không rút được gì để lần sau viết đúng hơn. Mười thay đổi khiến người
học không nhớ gì; hai thay đổi thì nhớ được.

Nên giữ nguyên tối đa những gì user viết. Chỉ chạm vào chỗ **thật sự sai**:

- Ngữ pháp: chia động từ, thì, số ít/số nhiều, mạo từ (`a`/`an`/`the`), giới từ, trật tự từ
- Dùng từ sai nghĩa hoặc sai ngữ cảnh đến mức người đọc hiểu nhầm hoặc thấy kỳ
- Cấu trúc câu dịch thẳng từ tiếng Việt nên người bản ngữ không hiểu được

**Không** chạm vào:

- Từ đơn giản nhưng đúng — đừng "nâng cấp" `use` thành `utilize`, `ask` thành `inquire`
- Câu ngắn, cộc — đó là giọng của user, không phải lỗi
- Tên riêng, thuật ngữ kỹ thuật, tên file, đường dẫn, lệnh, đoạn code
- Chữ hoa/thường và dấu câu, trừ khi gây hiểu sai

**Nếu câu đã đúng thì nói thẳng là đúng.** Đừng bịa ra lỗi để mục này trông có ích.
Một câu "Câu này không có lỗi" là thông tin thật và có giá trị — nó cho user biết họ đang
viết được. Bịa lỗi thì phá hỏng chính mục đích của skill.

## Ngưỡng: "tạm ổn" là đủ

Ngưỡng để bỏ qua là **tạm ổn**, không phải **hay**. Một câu hơi vụng, hơi thừa chữ, hoặc không
phải cách người bản ngữ thường nói — nhưng đúng ngữ pháp và người đọc hiểu đúng ý — thì **không
sửa**. Nêu ra những chỗ đó chỉ làm loãng mất lỗi thật, thứ duy nhất user cần nhớ lần này.

Nếu cả câu đều tạm ổn thì báo là không cần sửa. Đó là một kết quả tốt, không phải kết quả rỗng,
và nó cho user biết họ đang viết được.

Việc nâng câu từ "tạm ổn" lên "hay" sẽ có một skill riêng, làm sau, khi nền tiếng Anh của user
đã vững. Skill này cố tình không làm phần đó — trộn hai việc lại thì cả hai đều kém đi: người
học ở mức nền bị ngợp, còn lỗi cơ bản thì trôi mất giữa đống góp ý văn phong.

## Định dạng

Đặt ở cuối câu trả lời, sau một đường kẻ ngang. Giữ gọn — phần này là phụ trợ, không được
lấn át nội dung công việc.

```markdown
---

**English**

> <nguyên văn câu user viết>

<câu đã sửa>

- `<sai>` → `<đúng>` — <lý do ngắn, bằng tiếng Việt>
```

Giải thích bằng **tiếng Việt** vì đây là phần học; giải thích lỗi tiếng Anh bằng tiếng Anh
thì user phải giải mã hai lần. Mỗi lý do một dòng, đủ để hiểu quy tắc chứ không phải một bài
giảng ngữ pháp. Nếu cùng một lỗi lặp lại nhiều chỗ, gộp thành một dòng.

Khi không có lỗi, rút gọn còn:

```markdown
---

**English** — câu này không có lỗi.
```

## Các tình huống khác

**User viết yêu cầu bằng tiếng Việt (hoặc lẫn Việt–Anh).** Không có tiếng Anh để sửa, nên đừng
sửa gì. Thay vào đó đưa một bản tiếng Anh của yêu cầu đó để user đối chiếu, gắn nhãn rõ ràng:

```markdown
---

**English** — yêu cầu viết bằng tiếng Việt nên không có gì để sửa.
Nếu viết bằng tiếng Anh thì có thể nói: "<bản tiếng Anh tự nhiên, giọng đơn giản>"
```

Giữ bản tiếng Anh ở mức từ vựng đơn giản, đúng tầm người đang bổ túc nền — mục đích là để
lần sau user tự viết được, không phải để phô diễn.

**Yêu cầu dài nhiều câu hoặc nhiều đoạn.** Sửa hết, nhưng gom các lỗi cùng loại lại. Nếu dài
quá thì trích lại từng câu có lỗi thay vì chép nguyên khối văn bản.

**Chỉ có `/engfix` kèm một đoạn văn bản, không có việc gì để làm.** Khi đó bỏ qua phần 1, chỉ làm
phần sửa lỗi.

**Yêu cầu chính thất bại hoặc bị chặn.** Vẫn làm phần sửa tiếng Anh — nó độc lập với kết quả
công việc.

## Ví dụ

**Ví dụ 1 — lỗi cơ bản**

User viết: `please check the log file and tell me why the server was crash yesterday /engfix`

Sau khi đã trả lời xong việc chính:

```markdown
---

**English**

> please check the log file and tell me why the server was crash yesterday

please check the log file and tell me why the server crashed yesterday

- `was crash` → `crashed` — `crash` ở đây là động từ thường, chia quá khứ trực tiếp.
  `was crashed` chỉ dùng ở thể bị động, mà server tự crash chứ không bị ai crash.
```

Chú ý những gì **không** bị đụng tới: `please check` không bị đổi thành `could you check`,
chữ thường đầu câu để nguyên, `log file` giữ nguyên. Chỉ một lỗi thật được sửa.

**Ví dụ 2 — không có lỗi**

User viết: `/engfix summarize the three PDFs in this folder into one markdown file`

```markdown
---

**English** — câu này không có lỗi.
```

Không tán dương, không gợi ý cách viết "hay hơn". Câu đúng thì chỉ cần xác nhận là đúng.

**Ví dụ 3 — chỉ sửa cái sai, bỏ qua cái "tạm ổn"**

User viết: `I want to know how much money I must to pay for this service each month /engfix`

```markdown
---

**English**

> I want to know how much money I must to pay for this service each month

I want to know how much money I have to pay for this service each month

- `must to pay` → `have to pay` — `must` không bao giờ đi với `to`.
```

`how much money` hơi thừa chữ so với cách người bản ngữ hay nói, và cả câu có thể gọn hơn
thành `What's the monthly cost?`. Nhưng **không đụng tới**, vì nó không sai — nó tạm ổn.
Chen thêm những thứ đó vào sẽ làm loãng mất lỗi `must to` là thứ thực sự cần nhớ.
