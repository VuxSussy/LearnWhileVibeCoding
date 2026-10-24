# 🔁 VibeLearning được làm ra như thế nào

Tài liệu này dạy bạn **tự làm lại một bản nhỏ của VibeLearning** từ một thư mục trống. Nó được viết đúng theo khuôn mà lệnh `/rebuild` tạo ra,
nên bạn vừa học cách làm plugin, vừa thấy một bản "Tự làm lại" mẫu trông như thế nào.

## 🧠 Ý tưởng cốt lõi

Claude Code tự nó không biết bạn là người mới học. Plugin này **chen thêm chữ vào ngữ cảnh của AI đúng lúc**:
lúc mở phiên (luật dạy), lúc bạn gửi tin nhắn (lời khuyên dạy câu này thế nào), và lúc AI trả lời xong (ghi nhớ bạn đã học gì).
Giống như một trợ giảng đứng sau thầy giáo, thì thầm "bạn này hỏi khái niệm đấy, nhớ cho ví dụ" trước mỗi câu trả lời.

Toàn bộ "trí thông minh" nằm ở hai chỗ:
- **Chữ** (file `.md`): luật dạy và các skill. AI đọc rồi làm theo.
- **Script nhỏ** (`.sh`, `.py`): hook. Claude Code tự chạy chúng ở những thời điểm cố định. Thứ gì script **in ra** sẽ được đưa cho AI đọc.

## 🧱 Bản thiết kế

```
plugin.json ─► session-start.sh ─► (AI đọc luật dạy)
                     │
 bạn gõ tin nhắn ─► context.py ─► (AI biết nên dạy câu này kiểu gì)
                     │
 AI trả lời xong ─► learner.py ─► learner.json ─► (phiên sau session-start.sh đọc lại)
```

Thứ tự làm: **manifest → luật dạy lúc mở phiên → đọc tin nhắn → bộ nhớ → test**.
Mốc nào cũng chạy được ngay, nên bạn luôn có một plugin hoạt động, rồi thêm từng mũi tên một.

## 🪜 Các mốc

### Mốc 1/5: Một plugin trống mà Claude Code nhận ra
🎯 **Mục tiêu:** `claude --plugin-dir ./my-learning` chạy được, không báo lỗi.
✍️ **Viết:** `my-learning/.claude-plugin/plugin.json`
```json
{ "name": "my-learning", "version": "0.1.0", "description": "Dạy tôi khi tôi code" }
```
🛠️ **Tự tìm ra thế nào:** Tìm "Claude Code plugins reference" trên docs.claude.com. Hoặc mở một plugin có sẵn (thư mục `.claude-plugin/` của repo này) và bắt chước.
✅ **Kiểm tra:** Chạy `claude --plugin-dir ./my-learning`, gõ `/plugin`, và thấy `my-learning` trong danh sách.
🔑 *Manifest* = tờ "chứng minh thư" của plugin: tên, phiên bản, mô tả.

### Mốc 2/5: Luật dạy được nạp mỗi khi mở phiên
🎯 **Mục tiêu:** Mở phiên mới, AI tự giải thích từng bước mà bạn không cần nhắc.
✍️ **Viết:** `hooks/hooks.json` để đăng ký hook, `hooks/session-start.sh` để in luật ra.
```json
{ "hooks": { "SessionStart": [ { "hooks": [
  { "type": "command", "command": "sh \"${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh\"" } ] } ] } }
```
```sh
#!/bin/sh
cat "$(dirname "$0")/teaching-rules.md"
```
Rồi viết `hooks/teaching-rules.md`, chừng 10 dòng: "Mỗi bước: 📘 Đang làm / 💡 Vì sao / 🛠️ Tự làm thế nào".
🛠️ **Tự tìm ra thế nào:** Đọc trang "Hooks reference" của Claude Code, mục `SessionStart`: những gì hook in ra (stdout) sẽ được thêm vào ngữ cảnh.
Muốn biết `${CLAUDE_PLUGIN_ROOT}` là gì thì tìm đúng cụm đó trong docs.
✅ **Kiểm tra:** Mở phiên mới và nhờ AI tạo một file bất kỳ. Câu trả lời phải có dòng 📘 và 💡.
⚠️ **Bẫy hay gặp:** Quên `exit 0` hoặc script bị lỗi thì luật không được nạp mà không có thông báo nào. Hãy chạy thử `sh hooks/session-start.sh` trong terminal trước.

### Mốc 3/5: Đọc tin nhắn của người học
🎯 **Mục tiêu:** Gõ "middleware là gì" thì AI nhận được dòng `[VibeLearning] Reading this message → concept question`.
✍️ **Viết:** `hooks/context.py`, đăng ký ở sự kiện `UserPromptSubmit`. Phần lõi chỉ khoảng 15 dòng:
```python
import json, re, sys
INTENTS = [
    ("bug", [r"\blỗi\b", r"\berror\b"], "Bug: dò lỗi thành tiếng với các dòng 🔦."),
    ("concept question", [r"là gì", r"what is"], "Hỏi khái niệm: trả lời thẳng, ví dụ đời thường, chỉ chỗ trong code."),
    ("how to make it", [r"làm sao", r"how do i"], "Muốn biết cách làm: 🧱 bản thiết kế trước, 🛠️ từng bước."),
]
prompt = json.load(sys.stdin).get("prompt", "").lower()
found = [(name, advice) for name, patterns, advice in INTENTS if any(re.search(p, prompt) for p in patterns)]
if found:
    print("[VibeLearning] Reading this message → " + ", ".join(n for n, _ in found))
    for _, advice in found:
        print("→ " + advice)
```
🧮 **Thuật toán:** *So khớp từ khoá (regex)*. Dò từng cụm từ trong câu, giống như phân loại thư theo chữ ghi ngoài phong bì. Câu dài gấp đôi thì mất khoảng gấp đôi thời gian, và vẫn chỉ tốn vài phần nghìn giây.
🛠️ **Tự tìm ra thế nào:** Docs của `UserPromptSubmit` cho biết hook nhận JSON qua stdin, trong đó có trường `prompt`. Để thử regex, dùng regex101.com.
✅ **Kiểm tra:** `echo '{"prompt":"middleware là gì"}' | python3 hooks/context.py` phải in ra `concept question`.
⚠️ **Bẫy hay gặp:** Người Việt hay gõ không dấu. Bản thật bỏ dấu cả câu lẫn mẫu (`learner.plain()`) khi người dùng gõ không dấu. Còn khi có dấu, nó so **có dấu**, để "lời" không bị nhầm thành "lỗi".

### Mốc 4/5: Bộ nhớ người học
🎯 **Mục tiêu:** Sau khi AI dạy `🔑 Thuật ngữ: *Hook* = ...`, phiên sau AI biết bạn đã học "Hook".
✍️ **Viết:** `hooks/learner.py`, đăng ký ở sự kiện `Stop`. Nó làm 3 việc:
1. Đọc `last_assistant_message`, tức tin nhắn cuối của AI, từ JSON đầu vào.
2. Dùng regex lấy các dòng `🔑 ...: *tên* = nghĩa` và `📚 Thuật ngữ mới: *a*, *b*`.
3. Ghi vào `~/.claude/vibe-learning/learner.json`. `session-start.sh` gọi `python3 learner.py summary` để in phần "đã biết" vào luật dạy.

🛠️ **Tự tìm ra thế nào:** Muốn biết Stop hook nhận được những trường nào, cách nhanh nhất là viết một hook chỉ làm `cat > /tmp/stop.json` rồi mở file đó ra xem.
✅ **Kiểm tra:** `echo '{"last_assistant_message":"🔑 Term: *Hook* = chuông báo"}' | python3 hooks/learner.py`, rồi `cat ~/.claude/vibe-learning/learner.json`.

🧩 **Ca khó: "Bộ nhớ không ghi được gì"**
   🤒 **Triệu chứng:** Ở phiên thật, AI viết 🔑 rất nhiều lần mà `learner.json` vẫn trống.
   🔦 **Dò ra thế nào:** Mở thẳng file transcript của phiên. Thấy app desktop chỉ lưu **1 đoạn chữ** của AI trong cả phiên. Tiếp đó đọc mô tả trường `last_assistant_message`: trường này chỉ chứa **tin nhắn cuối cùng**.
   🔎 **Nguyên nhân gốc:** Các dòng 🔑 nằm ở giữa lượt, xen giữa các lệnh, nên không tới được hook.
   🛠️ **Cách sửa & vì sao đúng:** Luật dạy yêu cầu AI kết thúc lượt bằng dòng `📚 Thuật ngữ mới: ...`. Dòng này luôn nằm trong tin nhắn cuối, nên hook luôn đọc được.
   🧠 **Lần sau nhận ra:** Test với dữ liệu giả thì xanh, chạy thật lại trống, nghĩa là **dữ liệu thật có hình dạng khác**. Hãy đi xem dữ liệu thật trước khi sửa code.

### Mốc 5/5: Test tự động
🎯 **Mục tiêu:** `python3 -m unittest discover -s tests` báo `OK`.
✍️ **Viết:** Mỗi test chạy hook bằng `subprocess` với một thư mục `HOME` tạm. Nhờ vậy bạn thử thoải mái mà không đụng tới `~/.claude` thật.
```python
out = subprocess.run([sys.executable, "hooks/context.py"], input='{"prompt":"middleware là gì"}',
                     capture_output=True, text=True, env={**os.environ, "HOME": tmp}).stdout
assert "concept question" in out
```
🛠️ **Tự tìm ra thế nào:** Mỗi lần thêm một cụm từ vào `INTENTS`, thêm luôn câu ví dụ đó vào `test_detects_what_kind_of_help_is_wanted`.
Regex rất dễ "sửa chỗ này hỏng chỗ kia", và test là lưới an toàn cho chuyện đó.
✅ **Kiểm tra:** Cố tình xoá `r"là gì"` khỏi `INTENTS` thì test phải đỏ. Thêm lại thì test xanh.

## 🧭 Khuôn dùng lại được

Mọi plugin "làm AI cư xử khác đi" đều theo một khuôn: **chọn thời điểm (hook) → in ra đúng chữ AI cần đọc lúc đó → lưu lại những gì cần nhớ vào file**.
Bạn có thể dùng khuôn này để làm plugin nhắc viết test, plugin kiểm tra bảo mật, hay plugin bắt AI trả lời ngắn.

## 🏋️ Tự thử

1. **Dễ:** Thêm ý định "so sánh" (`so với`, `nên dùng cái nào`, `vs`) vào `INTENTS`, kèm lời khuyên "lập bảng so sánh 3 dòng". Nhớ thêm test.
2. **Khó hơn:** Cho `/progress` đánh dấu một thuật ngữ là "đã vững" khi bạn trả lời đúng câu `/quiz` về nó. Gợi ý: thêm trường `"solid": true` trong `learner.json`.

## 📁 Bản đồ file của bản thật

| File | Làm gì |
|---|---|
| `.claude-plugin/plugin.json` | Manifest: tên, phiên bản |
| `hooks/hooks.json` | Đăng ký hook nào chạy lúc nào |
| `hooks/session-start.sh` | Mở phiên: in luật dạy + chế độ đang bật + phần "đã biết" |
| `hooks/teaching-rules.md` | Luật dạy cốt lõi (📘/💡/🛠️, 🧱, 🔁, 🧩, 🧾...) |
| `hooks/context.py` | Đọc từng tin nhắn, chọn cách dạy |
| `hooks/learner.py` | Bộ nhớ người học |
| `hooks/log-activity.py` | Ghi mỗi lệnh AI chạy, phục vụ `/activity` |
| `hooks/type-it-guard.py` | Chế độ tự gõ: chặn AI chạy `git`/`npm` thay bạn |
| `skills/*/SKILL.md` | Kỹ năng AI tự dùng khi phù hợp (`rebuild`, `hard-case`...) |
| `commands/*.md` | Lệnh gạch chéo (`/progress`, `/quiz`...) |
| `scripts/build-codex.py` | Sinh bản cho OpenAI Codex từ các file trên |
| `tests/test_hooks.py` | Test tự động |
