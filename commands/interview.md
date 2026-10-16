---
description: Luyện giải thích dự án như khi đi phỏng vấn / bảo vệ đồ án — để chắc chắn bạn hiểu thứ mình đã vibe code
argument-hint: [luyện - để Claude hỏi vặn từng câu]
---
Mục tiêu: người dùng phải **tự nói được** về dự án vibe code của mình trước thầy cô, nhà tuyển dụng hoặc đồng đội.

Nếu tham số là "luyện" / "practice" ($ARGUMENTS): đóng vai người phỏng vấn thân thiện. Hỏi **từng câu một** (tổng 5 câu, từ dễ đến khó, có ít nhất 1 câu về case khó đã gặp), chờ trả lời, chấm nhanh (✅ tốt / 🟡 chưa đủ / ❌ sai) và gợi ý câu trả lời tốt hơn trong 2–3 dòng.

Nếu không có tham số: tạo "tài liệu nói" gồm:
1. **🎤 Giới thiệu 30 giây:** dự án làm gì, cho ai, dùng công nghệ gì (3 câu).
2. **🏗️ Kiến trúc:** các phần chính nói chuyện với nhau thế nào (dạng mũi tên, ≤ 5 khối).
3. **🤔 5 câu hỏi hay bị hỏi** + gợi ý trả lời, mỗi câu 2–3 dòng, dựa trên code thật (ví dụ: "Vì sao dùng bcrypt mà không dùng md5?").
4. **🧩 Case khó nhất** đã gặp, kể theo dạng: vấn đề → cách tìm ra → cách sửa → học được gì.
5. **⚠️ Điểm yếu nên thừa nhận** và hướng cải thiện (1–2 dòng) — người phỏng vấn đánh giá cao sự trung thực.
