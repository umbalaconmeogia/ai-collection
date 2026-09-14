# engfix

Skill cá nhân cho Claude Code. Làm việc bạn yêu cầu **rồi** sửa lỗi tiếng Anh trong chính
câu yêu cầu đó, ở một mục ngắn cuối câu trả lời.

Tạo ngày 2026-09-13.

> **Phân biệt hai file:** `SKILL.md` là chỉ thị cho Claude đọc và thi hành.
> `README.md` (file này) là ghi chú cho bạn — thiết kế, lý do, cách điều chỉnh.
> Sửa hành vi của skill thì sửa `SKILL.md`, không phải file này.

## Cách gọi

```
/engfix please check the log file and tell me why the server was crash yesterday
```

hoặc đặt ở cuối, sau khi viết xong yêu cầu:

```
please check the log file and tell me why the server was crash yesterday /engfix
```

Dạng đứng đầu chắc chắn chạy vì đó là slash command thật. Dạng đứng cuối phụ thuộc vào việc
Claude có để ý chuỗi `/engfix` trong tin nhắn — thường là có, nhưng nếu thấy nó im lặng không
sửa gì thì chuyển lên đầu câu.

## Mục đích

Bạn đang tự bổ túc **nền** tiếng Anh bằng cách viết yêu cầu công việc bằng tiếng Anh thay vì
tiếng Việt. Skill này bám đúng mục tiêu đó: chữa chỗ hỏng, không dạy viết văn hay.

Việc chính vẫn là thực hiện yêu cầu. Phần tiếng Anh là hậu cảnh, đặt cuối, giữ ngắn.

## Ngưỡng sửa

Ngưỡng là **tạm ổn**, không phải **hay**.

| Sửa | Để yên |
|---|---|
| Ngữ pháp: chia động từ, thì, số ít/nhiều, mạo từ, giới từ, trật tự từ | Từ đơn giản nhưng đúng (`use` không bị đổi thành `utilize`) |
| Dùng từ sai nghĩa (`relative` khi muốn nói `related`) | Câu ngắn, cộc — đó là giọng của bạn |
| Lỗi kết hợp từ (`make an explanation` → `explain`) | Câu đúng nhưng dài dòng (`the reason why`, `how much money`) |
| Câu dịch thẳng từ tiếng Việt nên người bản ngữ không hiểu | Tên riêng, thuật ngữ, tên file, đường dẫn, code |

Câu đã tạm ổn thì nó báo `**English** — câu này không có lỗi.` và dừng. **Không bịa lỗi** để
mục đó trông có ích — đây là quy tắc được viết rõ trong `SKILL.md` và đã được kiểm chứng.

Lý do đặt ngưỡng thấp: mười thay đổi thì không nhớ gì, hai thay đổi thì nhớ được. Nêu cả những
chỗ chỉ hơi vụng sẽ làm loãng mất lỗi thật — thứ duy nhất cần nhớ lần đó.

## Cố tình không làm

**Không nâng câu từ "tạm ổn" lên "hay".** Phần đó sẽ là một skill riêng, làm sau, khi nền tiếng
Anh đã vững. Trộn hai việc lại thì cả hai đều kém: người học ở mức nền bị ngợp, còn lỗi cơ bản
thì trôi mất giữa đống góp ý văn phong.

Nếu sau này làm skill bậc hai, đừng nhồi vào file này — tạo skill mới.

## Yêu cầu viết bằng tiếng Việt

Không có tiếng Anh để sửa nên nó không sửa gì, chỉ đưa một bản tiếng Anh của yêu cầu để bạn
đối chiếu, có gắn nhãn rõ là không phải sửa lỗi.

## Đã kiểm chứng

Chạy 5 ca qua subagent trước khi dùng thật, tất cả đạt:

| Ca | Kiểm tra | Kết quả |
|---|---|---|
| 1 | `all the markdown file` — lỗi số nhiều | Sửa đúng 1 chỗ, không đụng gì khác |
| 2 | Câu tiếng Anh hoàn toàn đúng | Báo không có lỗi, không bịa |
| 3 | Yêu cầu viết bằng tiếng Việt | Không bịa, đưa bản tiếng Anh đơn giản |
| 4 | `make a explanation` — lỗi mạo từ + kết hợp từ | Sửa cả hai, giải thích quy tắc |
| 5 | Câu đúng ngữ pháp nhưng dài dòng ba chỗ | Để yên hoàn toàn |

Ca 2 và ca 5 là hai ca quan trọng nhất — chúng kiểm tra việc **không** làm gì, thứ mà một mô
hình được yêu cầu "sửa văn bản" rất dễ làm quá tay.

Các ca test không kiểm tra được việc skill có **tự kích hoạt** hay không, vì subagent được chỉ
định đọc file skill sẵn. Việc đó chỉ biết qua dùng thật.

## Muốn điều chỉnh

Chỗ dễ phải chỉnh nhất là ranh giới "từ dùng quá chuối" — nó nằm giữa lỗi thật và chuyện văn phong.

- Thấy nó **sửa nhiều quá** những thứ bạn cho là chấp nhận được → siết mục
  `## Ngưỡng: "tạm ổn" là đủ`, và thêm ví dụ về thứ cần để yên.
- Thấy nó **bỏ sót** lỗi bạn muốn được nhắc → nới danh sách trong mục
  `## Nguyên tắc sửa: tối thiểu`.
- Muốn đổi cách trình bày → mục `## Định dạng`.

Cách sửa hiệu quả nhất là **thêm hoặc đổi ví dụ** ở mục `## Ví dụ`, không phải thêm chữ "đừng".
Ví dụ 3 hiện đang dạy bằng cách chỉ ra thứ không được đụng tới — đó là khuôn mẫu nên theo.

## File trong folder

```
engfix/
├── SKILL.md    <- chỉ thị cho Claude (sửa file này để đổi hành vi)
└── README.md   <- ghi chú cho bạn (file này)
```
