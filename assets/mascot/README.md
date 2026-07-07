# น้องมายด์ mascot art — sourced from the APP's real assets (2026-07-07)

Every slot below is now filled with art copied from the MindSpend app itself
(`MindSpend/Assets.xcassets`) — **do not generate new mascot art for the site;
when the app gains new poses, re-copy from the app.** The `onerror` → flat SVG
fallback (`assets/mind-*.svg`) remains wired as a safety net only.

The app currently ships 4 distinct poses, so several site slots intentionally
reuse the same pose. If a dedicated pose is drawn later (celebrate arms-up,
waving, crowned king, heart-hug, peeking), drop it over the matching filename —
paths are stable, no code change needed.

**Specs (unchanged):** transparent PNG · ~400–800px long edge · green-bodied
น้องมายด์ per the app art.

| File | Currently filled with (app asset) | Used in |
|------|-----------------------------------|---------|
| `mind-hero.png`      | `sati_member_mascot_standing` (800px) | Home hero, About hero bubble avatar |
| `mind-track.png`     | `mind_income_question`               | Home how-01 |
| `mind-think.png`     | `mind_thinking`                      | Home how-02, Help-centre hero, Blog featured |
| `mind-celebrate.png` | `mind_thinking`                      | Home how-03 |
| `mind-feat-1.png`    | `mind_thinking` (400px)              | Home feature card 1 (สรุปเชิงลึก), Blog card |
| `mind-feat-2.png`    | `sati_member_mascot_standing` (400px)| Home feature card 2 (อารมณ์ & การเงิน) |
| `mind-feat-3.png`    | `mind_income_question` (400px)       | Home feature card 3 (เป้าหมาย), Blog card |
| `mind-feat-4.png`    | `mind_thinking` (400px)              | Home feature card 4 (รายงาน) |
| `mind-feat-5.png`    | `mind_sleeping` (400px)              | Home feature card 5 (แจ้งเตือนอ่อนโยน) |
| `mind-king.png`      | `sati_member_mascot_standing`        | สติ+ premium section |
| `mind-heart.png`     | `sati_member_mascot_standing`        | Relationship section, About hero |
| `mind-peek.png`      | `mind_sleeping` (700px)              | Final CTA + footer corner (ทุกหน้า) |

`assets/logo.jpg` is the real app icon (`AppLogo.imageset/Mindspend Logo final.png`,
converted to JPG 512px) — nav, footer, favicon on every page.

Optional still owed: `assets/qr.png` — a real QR code pointing to the App Store
link, shown in the final CTA. Falls back to a placeholder box if absent.
