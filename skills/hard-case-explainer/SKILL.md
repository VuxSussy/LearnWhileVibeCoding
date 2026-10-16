---
name: hard-case-explainer
description: Giải thích "case khó" mà AI vừa giải để người vibe code hiểu thật sự. Dùng ngay sau khi sửa một bug khó, lỗi khó hiểu, lỗi phải thử nhiều lần mới hết, vấn đề về async/thời gian/bộ nhớ/CORS/quyền/cache/phiên bản thư viện, hoặc khi người dùng hỏi "sao nó lại hết lỗi?", "vừa rồi sửa gì vậy?", "giải thích case này".
---

# Hard Case Explainer — biến bug khó thành bài học

Người vibe code thường chỉ thấy "lỗi → AI sửa → hết lỗi" mà không biết **chuyện gì đã xảy ra**.
Lần sau gặp lại, họ vẫn bó tay. Skill này biến mỗi case khó thành một bài học nhỏ có thể dùng lại.

## Khi nào là "case khó"? (gặp 1 dấu hiệu là đủ)
- Phải **thử từ 2 lần trở lên** mới sửa được, hoặc cách sửa đầu tiên sai.
- **Nguyên nhân thật nằm ở chỗ khác** so với chỗ báo lỗi (ví dụ: lỗi hiện ở UI nhưng gốc ở API).
- Thông báo lỗi **khó hiểu hoặc gây hiểu nhầm**.
- Liên quan tới thứ "vô hình": thời gian/bất đồng bộ, cache, biến môi trường, phiên bản thư viện, quyền truy cập, CORS, encoding, múi giờ, race condition, memory leak.
- Có **workaround** hoặc cách sửa trông lạ mà người mới sẽ không tự nghĩ ra.

Bug vặt (gõ sai tên biến, thiếu dấu ngoặc) → **không** dùng khối này, chỉ cần 1 dòng 📘 bình thường.

## Định dạng khối 🧩 (mỗi dòng 1–2 câu, ngắn gọn)
```
🧩 Case khó: <tên ngắn, dễ nhớ>
   🤒 Triệu chứng: <người dùng thấy gì>
   🔎 Nguyên nhân gốc: <chuyện gì thực sự xảy ra — so sánh đời thường nếu được>
   🛠️ Cách sửa & vì sao đúng: <sửa gì, vì sao nó giải quyết đúng gốc chứ không chỉ che triệu chứng>
   🧠 Lần sau nhận ra bằng cách: <dấu hiệu để tự đoán ra loại lỗi này>
```
Nếu đã thử cách sai trước đó, thêm 1 dòng `❌ Cách đầu chưa được vì: ...` — đây là phần học được nhiều nhất.

## Nguyên tắc
- **Trung thực:** nếu chưa chắc nguyên nhân gốc, nói rõ "khả năng cao là...", đừng bịa.
- **Nói về code của chính người dùng**, chỉ ra file/dòng cụ thể, không giảng lý thuyết chung chung.
- **Giữ ngắn.** Muốn đào sâu (vẽ luồng chạy, tự tái hiện lỗi) → gợi ý `/hard-case`.
- Nếu chế độ ADHD bật: in đậm từ khoá mỗi dòng, bỏ bớt chữ, giữ đủ 5 dòng.

## Ví dụ
🧩 **Case khó: "Bấm nút 2 lần thì tạo 2 đơn hàng"**
   🤒 **Triệu chứng:** Người dùng bấm nhanh 2 lần → database có 2 đơn giống hệt.
   🔎 **Nguyên nhân gốc:** Request đầu **chưa kịp trả về** thì request thứ 2 đã gửi — như 2 người cùng rút tiền một lúc.
   🛠️ **Cách sửa & vì sao đúng:** **Khoá nút** khi đang gửi và thêm **mã đơn duy nhất** ở server → dù gửi 2 lần, server chỉ nhận 1.
   🧠 **Lần sau nhận ra:** Lỗi chỉ xảy ra **khi thao tác nhanh** → nghĩ ngay tới "2 việc chạy chồng lên nhau".
