#!/bin/sh
# Nhắc ngắn mỗi lượt để Claude không "quên" giải thích khi cuộc trò chuyện dài.
[ -f "$HOME/.claude/learn-while-vibe-coding.off" ] || echo "[LearnWhileVibeCoding] Nhớ: mỗi bước làm kèm giải thích 2–3 dòng, dễ hiểu, theo định dạng 📘 Đang làm / 💡 Vì sao / 🔑 Thuật ngữ."
[ -f "$HOME/.claude/learn-while-vibe-coding.adhd" ] && echo "[ADHD] Câu ngắn, in đậm từ khoá, cập nhật 🗺️ tiến độ, chỉ 1 việc tiếp theo, chỉ 1 câu hỏi."
exit 0
