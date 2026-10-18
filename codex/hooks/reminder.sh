#!/bin/sh
# Nhắc ngắn mỗi lượt để Claude không "quên" giải thích khi cuộc trò chuyện dài.
FLAG="$HOME/.codex/vibe-learning"
[ -f "$FLAG.off" ] || echo "[VibeLearning] Mỗi bước kèm 📘/💡/🔑 (2–3 dòng, dễ hiểu). Vừa giải xong case khó → thêm khối 🧩 (triệu chứng, nguyên nhân gốc, cách sửa & vì sao, lần sau nhận ra)."
[ -f "$FLAG.adhd" ] && echo "[ADHD] Câu ngắn, in đậm từ khoá, cập nhật 🗺️ tiến độ, chỉ 1 việc tiếp theo, chỉ 1 câu hỏi."
[ -f "$FLAG.practice" ] && echo "[Practice] Tính năng mới → cân nhắc chừa 1 chỗ 3–10 dòng có ý nghĩa với TODO(bạn) cho người dùng tự viết."
exit 0
