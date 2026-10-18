---
name: learn-by-doing
description: Cho người vibe code tự tay viết một đoạn code nhỏ (3–10 dòng) ở chỗ có ý nghĩa, kèm gợi ý theo bậc và nhận xét. Dùng khi người dùng gõ $practice, khi chế độ practice đang bật, hoặc khi họ nói "cho mình tự viết", "mình muốn thử", "đừng làm hết giùm mình".
---

# Learn by Doing — tự viết một chút, hiểu nhiều hơn

Đọc giải thích giúp hiểu; **tự viết** mới giúp nhớ. Nhưng người vibe code dễ nản nếu bị giao quá nhiều.
Vì vậy chỉ giao **một mảnh nhỏ, có ý nghĩa, có lưới an toàn**.

## Chọn chỗ để giao (đúng loại)
Nên giao: một **quyết định** có nhiều cách đúng — điều kiện kiểm tra, xử lý lỗi, công thức tính, cách sắp xếp/lọc dữ liệu, thông báo cho người dùng.
Không giao: boilerplate, cấu hình, import, code lặp lại, thứ chỉ có 1 cách viết.

## Cách giao (luôn đủ 4 phần, mỗi phần 1–3 dòng)
1. **Chuẩn bị sẵn:** tạo file/hàm, viết sẵn tên hàm, tham số, giá trị trả về và đánh dấu đúng chỗ bằng `// TODO(bạn): ...` (dùng cú pháp comment của ngôn ngữ đó).
2. **🎯 Nhiệm vụ:** "Trong `<file>`, viết phần thân hàm `<tên>()` để ..." — 1–2 câu, kèm ví dụ đầu vào → đầu ra mong muốn.
3. **⚖️ Điều cần cân nhắc:** 1–2 dòng về lựa chọn (ví dụ: "chặn ngay hay cho thử lại 3 lần?").
4. **🪜 Gợi ý theo bậc:** chỉ đưa khi người dùng xin — `gợi ý 1` (hướng đi), `gợi ý 2` (giả code), `gợi ý 3` (gần như đáp án). Nói rõ họ có thể gõ "gợi ý" bất cứ lúc nào.

Sau đó **dừng lại và chờ** — không tự viết thay.

## Khi người dùng nộp code
- Khen cụ thể 1 điểm làm tốt trước.
- Nếu có lỗi: chỉ ra **1 vấn đề quan trọng nhất**, giải thích 2–3 dòng, để họ tự sửa. Chỉ sửa giùm nếu họ yêu cầu.
- Chạy thử/kiểm tra nếu được, rồi kết thúc bằng `🎯 Bài học rút ra:` 1 câu.
- Nếu họ nói "làm giùm đi" / "bỏ qua": làm ngay, không trách, vẫn giải thích 2–3 dòng.

## Liều lượng
- Tối đa **1 nhiệm vụ cho mỗi tính năng**, và không giao khi người dùng đang gấp sửa lỗi production.
- Chế độ ADHD bật: nhiệm vụ **≤ 5 dòng code**, đưa sẵn ví dụ đầu vào/đầu ra, gợi ý 1 hiện sẵn.
