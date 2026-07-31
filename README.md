<div align="center">

<img src="assets/header.svg" width="100%" alt="Dolmaa Sharma — systems · AI infrastructure · security" />

<br/><br/>

<a href="https://linkedin.com/in/dolmaasharma24"><img src="https://img.shields.io/badge/LINKEDIN-dolmaasharma24-161b22?style=flat-square&labelColor=e3b341" alt="LinkedIn" /></a>
&nbsp;
<a href="mailto:dolmaasharma2005@gmail.com"><img src="https://img.shields.io/badge/EMAIL-dolmaasharma2005@gmail.com-161b22?style=flat-square&labelColor=e3b341" alt="Email" /></a>

</div>

<img src="assets/divider.svg" width="100%" alt="" />

I build infrastructure for systems that can't assume good input — a shell gate in Rust that decides whether an AI agent's command is allowed to run, signed telemetry for remote exams where the client is presumed compromised, retrieval pipelines assembled from parts rather than borrowed from a framework.

Mostly Python and TypeScript, increasingly Rust. CS at VIT Bhopal. I'd rather write the measurement than the adjective, and I document what a thing *doesn't* do next to what it does.

<img src="assets/divider.svg" width="100%" alt="" />

## Selected work

<details open>
<summary><b>shellguard</b> &nbsp;·&nbsp; a command gate for AI agents &nbsp;·&nbsp; <code>Rust</code></summary>

<br/>

Decides whether an agent's shell command should run, then confines whatever it lets through.

Every rule keys on **program identity**, not on the string you typed — so `find . -name "*.log" -exec rm -rf /etc {} \;` is judged as an `rm`, despite containing no `rm` in argv position. It unwraps `sudo`, `env -i`, `xargs`, `timeout`, `nice`, `bash -c`, ANSI-C quoting (`$'\x72\x6d'`), and commands hidden inside default-value expansions and redirect targets.

| | full gate | parse only |
|---|---|---|
| p50 | 2.8 µs | 542 ns |
| p99 | 13.4 µs | 1.5 µs |
| max | 35.7 µs | 21.9 µs |

<sub>58 000 samples over a 145-command corpus, M2 MacBook Air, release build.</sub>

Verdicts combine by severity rather than declaration order — `Allow < Confine < Ask < Deny` — so no broad allow can outrank a narrow deny. An unmatched command defaults to **`Confine`, not `Allow`**: "no rule matched" means the ruleset had nothing to say, which for agent-authored input is the common case rather than evidence of safety.

Two layers, because one isn't enough: a userspace gate that produces a reason a human can act on, and a kernel sandbox — Seatbelt on macOS, Landlock + seccomp-BPF on Linux — that contains what the gate permits. The gate is *not* a security boundary and the design docs say so; static analysis of shell is undecidable and `eval "$(curl x)"` is a one-line proof.

`Rust` `seccomp-BPF` `Landlock` `Seatbelt` `static analysis`

**[→ source](https://github.com/Dolmaa24/AgentShield-Micro-Runtime)**

</details>

<details open>
<summary><b>Proctoring AI</b> &nbsp;·&nbsp; edge-to-cloud exam integrity &nbsp;·&nbsp; <code>Python</code> <code>TypeScript</code></summary>

<br/>

Computer vision runs on the candidate's machine in real time; the backend holds policy, state, identity and evidence. **Raw video never touches the telemetry path.**

The client is treated as hostile by construction: per-session key derivation, HMAC-signed events, and a simulator that ships six scripted client-tampering modes so the integrity checks are tested against the attack rather than assumed. Policy lives in 16 declarative rules, separated from the fusion layer that does temporal filtering with no I/O of its own. The proctor console **fails closed** — there is no unauthenticated mode, because those endpoints carry every candidate's flags.

Nine components, run end-to-end: camera → MediaPipe → IPC → signed WebSocket → gateway → fusion → proctor console.

`FastAPI` `MediaPipe` `Electron` `LiveKit` `SQLite` `HMAC` `pytest`

**[→ source](https://github.com/Dolmaa24/Proctoring-AI)**

</details>

<details>
<summary><b>XG_Backend</b> &nbsp;·&nbsp; AI recruitment pipeline &nbsp;·&nbsp; <code>Python</code></summary>

<br/>

An async REST API that runs the whole hiring loop: multi-modal resume parsing (PyMuPDF + Tesseract OCR, so scanned PDFs work), dense-vector semantic matching against job posts instead of keyword ATS filtering, and rubric-based LLM interviews with deterministic weighted ranking.

Non-blocking FastAPI I/O, Celery for the heavy ML, PostgreSQL for ACID state, Alembic migrations, Dockerised. Rate limiting, path-traversal guards and prompt-injection defence are treated as backend requirements rather than features.

`FastAPI` `PostgreSQL` `Celery` `Docker` `sentence-transformers` `Alembic`

**[→ source](https://github.com/Dolmaa24/XG_Backend)**

</details>

<details>
<summary><b>Modular RAG Pipeline</b> &nbsp;·&nbsp; retrieval built from parts &nbsp;·&nbsp; <code>Python</code></summary>

<br/>

Ingestion → chunking → embedding → vector store → retrieval → generation, each stage decoupled and swappable. Built from scratch rather than on a framework, specifically so the mechanics stay visible.

Local `all-MiniLM-L6-v2` embeddings (384-dimensional, no paid API in the loop), ChromaDB persisted to disk and tuned for cosine similarity, Groq for inference, and prompt templates that keep answers strictly grounded in retrieved context. Parses encrypted PDFs via pycryptodome.

`Python` `ChromaDB` `HuggingFace` `Groq` `MIT`

**[→ source](https://github.com/Dolmaa24/RAG)**

</details>

<details>
<summary><b>AuraAI</b> &nbsp;·&nbsp; encrypted chat on $0 of infrastructure &nbsp;·&nbsp; <code>JavaScript</code></summary>

<br/>

AES-256-GCM encryption and HMAC-SHA-512 signing run entirely in the browser through the Web Crypto API — no external crypto libraries, and plaintext never leaves the device. PBKDF2 at 100 000 iterations derives the session keys; a fresh 96-bit IV per message.

Ships a **crypto inspector**: open any message you sent and read its IV, HMAC, ciphertext and fingerprint. Streaming multi-model inference (Llama 3.3 70B, Mixtral, Gemma), vision input, file context, voice I/O — with the API key held server-side and 200 req/15 min rate limiting. Vercel + Render, total infrastructure cost $0.

`Web Crypto API` `AES-256-GCM` `PBKDF2` `Groq` `Vercel` `Render`

**[→ live](https://chatbot-theta-two-23.vercel.app)** &nbsp;·&nbsp; **[→ source](https://github.com/Dolmaa24/CHATBOT)**

</details>

<details>
<summary><b>Finget</b> &nbsp;·&nbsp; decision-first personal finance &nbsp;·&nbsp; <code>TypeScript</code></summary>

<br/>

Most expense trackers tell you what you spent last month. Finget computes a **Safe Daily Allowance** — what you can spend today without breaking the budget — by subtracting obligations, savings goals and month-to-date spend from income in real time.

An SSE-streamed AI coach with a persistent conversation-memory model and live injection of your actual financial context. A what-if simulator that prices a purchase in *days of delay* against a savings goal. And "Friends Mode" shared wallets routed through explicit `?context=` parameters rather than implicit global state — so scope is always legible in the request.

`React` `TypeScript` `Vite` `Tailwind` `SSE` `Node.js`

**[→ source](https://github.com/Dolmaa24/Finget)**

</details>

<img src="assets/divider.svg" width="100%" alt="" />

## Stack

| | |
|---|---|
| **languages** | Python · TypeScript · Rust · JavaScript · SQL |
| **backend** | FastAPI · async SQLAlchemy · Celery · PostgreSQL · SQLite · Docker · Alembic |
| **AI systems** | RAG from first principles · sentence-transformers · ChromaDB · HuggingFace · Groq · MediaPipe |
| **security** | AES-256-GCM · HMAC · PBKDF2 · seccomp-BPF · Landlock · Seatbelt · threat modelling |
| **frontend** | React · TypeScript · Vite · Tailwind · Electron |

<img src="assets/divider.svg" width="100%" alt="" />

## Signals

<div align="center">

<img src="assets/languages.svg" width="100%" alt="Language distribution: Python 43.1%, Rust 26.2%, JavaScript 12.3%, TypeScript 11.9%, CSS 4.6%, HTML 1.5%" />

<br/><br/>

<img src="https://raw.githubusercontent.com/Dolmaa24/Dolmaa24/output/snake.svg" width="100%" alt="Contribution grid animation" />

</div>

<!--
  Optional — a 3D contribution skyline. The workflow that generates it is already
  committed at .github/workflows/3d-contrib.yml; run it once from the Actions tab,
  then delete these two comment lines to switch the image on.

  <div align="center">
  <img src="profile-3d-contrib/profile-night-view.svg" width="100%" alt="3D contribution skyline" />
  </div>
-->

<img src="assets/divider.svg" width="100%" alt="" />

## Reach me

<div align="center">

Open to internships and collaboration on systems, AI infrastructure and security tooling.

<br/>

<a href="mailto:dolmaasharma2005@gmail.com"><img src="https://img.shields.io/badge/EMAIL-dolmaasharma2005@gmail.com-161b22?style=flat-square&labelColor=e3b341" alt="Email" /></a>
&nbsp;
<a href="https://linkedin.com/in/dolmaasharma24"><img src="https://img.shields.io/badge/LINKEDIN-dolmaasharma24-161b22?style=flat-square&labelColor=e3b341" alt="LinkedIn" /></a>

<br/><br/>

<img src="assets/footer.svg" width="100%" alt="I document what a thing doesn't do, next to what it does." />

</div>
