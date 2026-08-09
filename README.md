<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/cicca-dark.png">
    <img src="./assets/cicca-light.png" width="330" alt="CICCA">
  </picture>
</p>

<h1 align="center">Lê Trần Minh Đạt</h1>
<p align="center"><b>AI Engineer</b> — LLMOps · DevOps · Custom AI systems</p>

<p align="center">
  <a href="https://portfolio.cicca.dpdns.org">
    <img src="https://img.shields.io/badge/portfolio.cicca.dpdns.org-AE1D41?style=for-the-badge&logo=vercel&logoColor=E23E63&labelColor=1f1f1f&color=1f1f1f">
  </a>
  <a href="https://www.linkedin.com/in/dat-le-139a85284/">
    <img src="https://img.shields.io/badge/-Le%20Tran%20Minh%20Dat-AE1D41?style=for-the-badge&logoColor=E23E63&labelColor=1f1f1f&color=1f1f1f&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjggMTI4Ij48cGF0aCBmaWxsPSIjMDA3NmIyIiBkPSJNMTE2IDNIMTJhOC45MSA4LjkxIDAgMDAtOSA4Ljh2MTA0LjQyYTguOTEgOC45MSAwIDAwOSA4Ljc4aDEwNGE4LjkzIDguOTMgMCAwMDktOC44MVYxMS43N0E4LjkzIDguOTMgMCAwMDExNiAzeiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yMS4wNiA0OC43M2gxOC4xMVYxMDdIMjEuMDZ6bTkuMDYtMjlhMTAuNSAxMC41IDAgMTEtMTAuNSAxMC40OSAxMC41IDEwLjUgMCAwMTEwLjUtMTAuNDlNNTAuNTMgNDguNzNoMTcuMzZ2OGguMjRjMi40Mi00LjU4IDguMzItOS40MSAxNy4xMy05LjQxQzEwMy42IDQ3LjI4IDEwNyA1OS4zNSAxMDcgNzV2MzJIODguODlWNzguNjVjMC02Ljc1LS4xMi0xNS40NC05LjQxLTE1LjQ0cy0xMC44NyA3LjM2LTEwLjg3IDE1VjEwN0g1MC41M3oiLz48L3N2Zz4=">
  </a>
  <a href="mailto:datltmse@gmail.com">
    <img src="https://img.shields.io/badge/datltmse@gmail.com-AE1D41?style=for-the-badge&logo=Gmail&logoColor=E23E63&labelColor=1f1f1f&color=1f1f1f">
  </a>
  <a href="https://github.com/letranminhdat1516">
    <img src="https://img.shields.io/badge/letranminhdat1516-AE1D41?style=for-the-badge&logo=Github&logoColor=E23E63&labelColor=1f1f1f&color=1f1f1f">
  </a>
  <br><br>
  <a href="https://github.com/letranminhdat1516">
    <img align="center" src="https://streak-stats.demolab.com/?user=letranminhdat1516&hide_border=true&background=1f1f1f&stroke=1f1f1f&ring=E23E63&fire=E23E63&currStreakLabel=E23E63&sideLabels=c9d1d9&currStreakNum=ffffff&sideNums=ffffff&dates=8b949e" />
  </a>
</p>

<br>

I'm an AI engineer working in **LLMOps** — I build custom AI systems and then keep them running in production, which is the part most demos skip.

In the past year I shipped an on-prem RAG enrollment advisor for a 19-branch academy reaching **100,000+ learners**, running under systemd and Docker Compose entirely inside the client's VPN; a self-hosted voice agent on LiveKit that a coffee shop takes real orders through every day; a patient-monitoring vision system live on production RTSP cameras; an AI trading platform on AWS built by a 3-engineer team in **20 days**; and a VAS-compliant .NET 10 accounting ERP shipped to EC2 through GitHub Actions ahead of its regulatory deadline.

Every one of them logs each LLM call — tokens, cost, latency, errors — because a system you can't measure is a system you can't operate. The same instinct shows up everywhere else in my work: multi-provider failover written by hand because one outage meant lost orders, a 5-frame temporal validation strategy because false alarms erode trust faster than missed ones, and local ONNX embeddings on CPU because zero API cost beats a cheap API.

Outside of work I play games, self-host more than I probably should, and enjoy talking shop with people who build things.

<br>

## What I've shipped

- **RAG enrollment advisor** — hybrid retrieval (bge-m3 ONNX embeddings on CPU + Vietnamese full-text over pgvector), anti-hallucination guardrails, human-in-the-loop advisor cockpit, full per-call cost telemetry. On-prem, VPN-only.
- **Voice ordering agent** — real-time LiveKit agent with hand-built multi-provider LLM failover and a self-learning RAG loop; rolled out text → voice → real-time voice, self-hosted and still operated by me.
- **IPBMS patient monitoring** — led 4 engineers; YOLO pose estimation on live RTSP streams, event-driven Normal/Warning/Danger alerts over WebSocket, LLM-generated incident reports for care staff.
- **VAS-compliant ERP** — .NET 10 + PostgreSQL accounting platform audited against 164 regulatory test cases I authored, live with a company using it daily.
- **AI trading platform** — led 3 engineers zero-to-production in 20 days; built the trading engine and in-app assistant, set the architecture and delivery plan.

<br>

## What I work with

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,ts,cs,dotnet,nodejs,nestjs,react,postgres,redis,docker,aws,githubactions,linux,git,opencv&theme=dark&perline=8" />
  </a>
</p>

- **LLM / AI infra** — multi-provider LLM routing & fallback, hybrid RAG (pgvector + full-text), local ONNX embeddings (bge-m3), anti-hallucination guardrails, human-in-the-loop workflows, YOLO pose estimation, OpenCV, RTSP streaming
- **Backend** — .NET 10, Node.js 20, NestJS, REST API design, WebSocket, async streaming, event-driven architecture
- **Data** — PostgreSQL 16, pgvector, Redis 7, Supabase, RustFS (S3-compatible)
- **Cloud & LLMOps** — AWS (EC2, Bedrock, S3, IAM), Azure OpenAI, Docker Compose, GitHub Actions CI/CD, systemd, Linux provisioning, on-prem / VPN deployment
- **Practices** — SRS authoring, regulatory test-case design, compliance engineering, per-call LLM cost/latency/error instrumentation

<br>

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=letranminhdat1516&hide_border=true&bg_color=1f1f1f&color=E23E63&line=E23E63&point=ffffff&area=true&area_color=AE1D41" width="98%" />
</p>

<p align="center"><sub>B.Eng. Software Engineering · FPT University HCMC · GPA 3.47/4.0</sub></p>
