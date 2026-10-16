---
description: Mổ xẻ case khó mà AI vừa giải — nguyên nhân gốc, vì sao cách sửa đúng, và cách tự nhận ra lần sau
argument-hint: [mô tả case - mặc định là bug khó gần nhất]
---
Dùng skill `hard-case-explainer` để mổ xẻ kỹ case sau (nếu trống: case khó nhất vừa giải trong cuộc trò chuyện): $ARGUMENTS

Trình bày theo thứ tự, mỗi phần 2–3 dòng, lời thường:
1. **Khối 🧩** đầy đủ (triệu chứng, nguyên nhân gốc, cách sửa & vì sao đúng, lần sau nhận ra).
2. **🎬 Luồng chạy trước và sau khi sửa** — 2 dòng mũi tên, ví dụ: `Bấm nút → gửi request → (chưa xong) → bấm lại → gửi request lần 2 ❌`.
3. **❌ Các cách đã thử chưa được** (nếu có) và vì sao.
4. **🧪 Tự tái hiện:** 1 cách đơn giản để người dùng tự làm lỗi xuất hiện lại, để thấy tận mắt.
5. **🔁 Những chỗ khác có thể dính lỗi tương tự** trong dự án (nếu có, tối đa 2).
6. **❓ 1 câu hỏi kiểm tra** để người dùng tự trả lời; chờ họ trả lời rồi mới nhận xét.

Nếu tham số có chữ "lưu" hoặc "save": nối khối 🧩 vào `LEARNING_NOTES.md` dưới mục `## 🧩 Case khó` (tạo nếu chưa có).
