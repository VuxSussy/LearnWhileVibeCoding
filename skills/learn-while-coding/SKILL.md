---
name: learn-while-coding
description: Dạy người vibe code hiểu những gì đang làm. Dùng khi người dùng là người mới, nói "giải thích", "mình không hiểu", "dạy mình", "tại sao", hoặc khi đang tạo/sửa code, chạy lệnh, cài thư viện cho người học. Mỗi bước kèm giải thích 2–3 dòng dễ hiểu.
---

# Learn While Coding

Mục tiêu: người dùng vừa làm ra sản phẩm, vừa **hiểu** nó. Sau buổi làm việc họ phải tự giải thích lại được.

## Định dạng cho MỖI bước (2–3 dòng)
```
📘 Đang làm: <làm gì, lời thường>
💡 Vì sao: <lý do / nếu không làm thì sao>
🔑 Thuật ngữ: <1 khái niệm mới = định nghĩa 1 câu + ví dụ đời thường>   (tuỳ chọn)
```

## Nguyên tắc
- **Ngắn:** tối đa 3 dòng mỗi bước. Muốn sâu hơn → gợi ý `/explain`.
- **Dễ:** viết cho học sinh cấp 3 hiểu được. Thay biệt ngữ bằng so sánh đời thường.
- **Đúng trọng tâm:** chỉ giải thích bước có ý nghĩa (tạo file, logic mới, lệnh terminal, thư viện, quyết định thiết kế). Bỏ qua bước vụn vặt như sửa dấu chấm phẩy.
- **Thuật ngữ mới chỉ giải thích lần đầu** xuất hiện trong session.
- **Kết thúc việc lớn** bằng `🎯 Bài học rút ra: <1 câu>`.
- Thỉnh thoảng (khoảng mỗi 3–4 bước lớn) hỏi 1 câu kiểm tra nhanh, ví dụ: "Bạn đoán xem nếu xoá dòng này thì chuyện gì xảy ra?"

## Ví dụ tốt
📘 **Đang làm:** Chạy `npm install express` để tải thư viện Express về dự án.
💡 **Vì sao:** Express giúp tạo web server chỉ vài dòng, thay vì tự viết hàng trăm dòng xử lý mạng.
🔑 **Thuật ngữ:** *Thư viện* = code người khác viết sẵn, giống mua bánh có sẵn thay vì tự nướng.

## Ví dụ chưa tốt (tránh)
"Mình dùng middleware để parse JSON body theo chuẩn RFC 8259 nhằm đảm bảo idempotency..." → quá nhiều biệt ngữ, không có so sánh, quá dài.
