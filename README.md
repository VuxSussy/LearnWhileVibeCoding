# 🎓 LearnWhileVibeCoding

Plugin cho **Claude Code** giúp người vibe code **vừa làm vừa học** — không còn cảnh app chạy được mà mình không hiểu gì.
Mỗi bước Claude làm đều kèm giải thích **2–3 dòng, dễ hiểu như nói chuyện**.

## ✨ Trông như thế nào?

> 📘 **Đang làm:** Tạo file `.env` để lưu khoá API thay vì viết thẳng vào code.
> 💡 **Vì sao:** Nếu khoá nằm trong code và bạn đẩy lên GitHub, người lạ có thể lấy dùng.
> 🔑 **Thuật ngữ:** *Biến môi trường* = "tờ ghi chú bí mật" chương trình đọc lúc chạy.

## 📦 Cài đặt

Trong Claude Code, gõ lần lượt:

```
/plugin marketplace add VuxSussy/LearnWhileVibeCoding
/plugin install learn-while-vibe-coding@learn-while-vibe-coding-marketplace
```

Hoặc từ terminal:

```bash
claude plugin marketplace add VuxSussy/LearnWhileVibeCoding
```

```bash
claude plugin install learn-while-vibe-coding@learn-while-vibe-coding-marketplace
```

Sau đó mở session mới — chế độ học sẽ tự bật. Cập nhật bản mới: `claude plugin update learn-while-vibe-coding`.

## 🧰 Plugin gồm những gì?

| Thành phần | Tác dụng (giải thích ngắn) |
|---|---|
| **Hook `SessionStart`** | Mỗi khi mở session, "dặn" Claude luật dạy học: mỗi bước kèm 2–3 dòng giải thích. |
| **Hook `UserPromptSubmit`** | Nhắc khẽ mỗi lượt để Claude không quên giải thích khi trò chuyện dài. |
| **Skill `learn-while-coding`** | Bộ quy tắc chi tiết: định dạng 📘/💡/🔑, dùng so sánh đời thường, tránh biệt ngữ. |
| `/explain [thứ cần hiểu]` | Giải thích một file, đoạn code, lệnh hoặc khái niệm từng phần một. |
| `/why [quyết định]` | Vì sao chọn cách này? So với cách khác thì sao? |
| `/quiz [chủ đề]` | Đố nhanh 3 câu dựa trên code của bạn để kiểm tra đã hiểu chưa. |
| `/recap [lưu]` | Tóm tắt những gì đã học; thêm `lưu` để ghi vào `LEARNING_NOTES.md`. |
| `/glossary [từ]` | Bảng thuật ngữ đã gặp, mỗi từ giải nghĩa 1 câu + ví dụ đời thường. |
| `/learn-off` · `/learn-on` | Tắt / bật chế độ giải thích tự động khi bạn đã quen. |
| **Skill `i-have-adhd`** | Cho người ADHD / khó tập trung: chia nhỏ việc, câu ngắn, in đậm từ khoá, mỗi lần chỉ 1 việc. |
| `/adhd-on` · `/adhd-off` | Bật / tắt chế độ ADHD (được nhớ cho các session sau). |
| `/where` | "Mình đang ở đâu?" — định vị nhanh khi bị lạc hoặc vừa nghỉ quay lại. |

> Lệnh plugin có thể hiện dưới dạng `/learn-while-vibe-coding:explain` nếu trùng tên với lệnh khác.

## 🧠 Chế độ ADHD (`/adhd-on`)

Dành cho người **khó giữ tập trung** hoặc **dễ ngợp khi đọc chữ dài**. Vẫn giải thích 2–3 dòng, nhưng:

| Kỹ thuật | Giúp gì? |
|---|---|
| 🗺️ Thanh tiến độ `✅ → 👉 → ⬜` | Luôn thấy mình đang ở bước nào, còn bao nhiêu bước. |
| Câu ≤ 15 từ, **in đậm từ khoá** | Lướt mắt là bắt được ý chính, không phải đọc hết. |
| `👉 Việc của bạn:` — chỉ 1 việc | Không bị tê liệt vì quá nhiều lựa chọn. |
| `🅿️ Để sau:` | Ý lạc đề được "đỗ" lại, không làm đứt mạch. |
| ✅ Ăn mừng nhỏ, ☕ gợi ý nghỉ | Giữ động lực, tránh kiệt sức. |
| `/where` → khối 📍 định vị | Quay lại sau khi xao nhãng mà không phải đọc lại cả cuộc trò chuyện. |

Ví dụ:

> 🗺️ `✅ Cài Express → 👉 Tạo server → ⬜ Chạy thử`
>
> 📘 **Đang làm:** Tạo file `server.js` — **cửa chính** của web.
> 💡 **Vì sao:** Mọi yêu cầu từ trình duyệt đều **đi qua đây** trước.
>
> 👉 **Việc của bạn:** Gõ `node server.js` rồi mở `localhost:3000`.

Không cần bật lệnh cũng được: chỉ cần nói *"mình bị ADHD"* hoặc *"đọc dài không nổi"*, Claude sẽ tự dùng skill này.

## 🗺️ Gợi ý quy trình học

1. Ra yêu cầu như bình thường → đọc các khối 📘💡🔑 khi Claude làm.
2. Chỗ nào chưa hiểu → `/explain` hoặc `/why`.
3. Xong một tính năng → `/quiz` để tự kiểm tra.
4. Cuối buổi → `/recap lưu` để có sổ tay ôn tập.

## 📁 Cấu trúc

```
LearnWhileVibeCoding/
├── .claude-plugin/
│   ├── plugin.json          # thông tin plugin
│   └── marketplace.json     # để cài bằng `claude plugin`
├── hooks/
│   ├── hooks.json           # đăng ký hook
│   ├── session-start.sh     # bơm luật dạy học vào session
│   ├── reminder.sh          # nhắc mỗi lượt
│   ├── teaching-rules.md    # nội dung luật dạy học
│   └── adhd-rules.md        # luật thêm khi bật /adhd-on
├── skills/
│   ├── learn-while-coding/SKILL.md
│   └── i-have-adhd/SKILL.md
└── commands/                # các slash command
```

Muốn chỉnh giọng văn/định dạng giải thích? Sửa `hooks/teaching-rules.md` và `skills/learn-while-coding/SKILL.md`.
