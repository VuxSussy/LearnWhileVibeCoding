---
description: A plain-language map of the project — what each folder and key file is for, and how a request flows through it
argument-hint: [folder - optional]
---
Build a beginner-friendly map of the project (or of this folder: $ARGUMENTS).

1. Look at the structure first (list the files; skip `node_modules`, `.git`, build output and other generated folders), then read the entry points and config files.
2. Present:
   - **🧭 The project in one sentence.**
   - **📂 Tree** of the important folders/files only (≤ 20 lines), each with a short comment on what it's for:
     ```
     src/
     ├── server.js      # front door: starts the web server
     └── routes/        # one file per page/API endpoint
     ```
   - **🔄 How it flows:** one arrow line for the main path, e.g. `browser → routes/login.js → db.js → database`.
   - **🚪 Where to start reading:** the 2-3 files to open first, and why.
   - **🧰 Tech used:** language, frameworks and key libraries, one line each in plain words.
3. Suggest `/functions <file>` for the most important file.
