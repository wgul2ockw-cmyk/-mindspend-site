# น้องมายด์ mascot art — copied from the app's real assets

All art here is copied from the MindSpend app (`MindSpend/Assets.xcassets`) — the
shipping น้องมายด์. **Do not generate new mascot art for the site;** when the app
gains a pose, re-copy it. The `onerror` → flat SVG fallback (`assets/mind-*.svg`)
stays wired as a safety net only.

Two waves are merged here — the theme-aware sub-page set and the index/interaction
set — so a few filenames overlap by concept. Current on-disk mapping:

| File | App asset | Used in |
|------|-----------|---------|
| `mind-greet.png`     | `splash_hero` (greeting + calc/bolt clouds) | **index hero** · relationship section |
| `mind-track.png`     | `pangolin_scanning_v2_1` (calc + bolt)      | index how-01 (frame A) |
| `mind-scan-b.png`    | `pangolin_scanning_v2_2` (magnifier)        | index how-01 (frame B, scan loop) |
| `mind-cheer.png`     | `pangolin_cheer` (happy wave)               | index how-03 · footer wake state |
| `mind-insight.png`   | `pangolin_scanning_v1_1` (magnifier+receipt)| index feature 1 (สรุปเชิงลึก) |
| `mind-warm.png`      | `pangolin_waving` (blush wave)              | index feature 2 (อารมณ์ & การเงิน) |
| `mind-celebrate.png` | `pangolin_celebrate` (thumbs-up)            | index feature 3 (เป้าหมาย) · final CTA · changelog |
| `mind-think.png`     | `mind_income_question` (? bubble)           | index feature 4 (รายงาน) · support · blog |
| `mind-sleep.png`     | `mind_sleeping` (curled, zzz)               | index feature 5 (แจ้งเตือน) · footer |
| `mind-king.png`      | `sati_member_mascot_standing`               | สติ+ premium section |
| `mind-hero.png`      | `sati_member_mascot_standing`               | about hero |
| `mind-heart.png`     | `sati_member_mascot_standing`               | about / relationship |
| `mind-peek.png`      | `mind_sleeping`                             | sub-page footers (about/faq/support/blog) |
| `mind-feat-1..5.png` | mixed app poses (400px)                     | blog cards |

Interaction: any mascot with `data-mind` talks on tap (Itim speech bubble via
`assets/mind.js`) — observational voice, register-high / valence-zero.

`assets/crown-gold.svg` — gold-tinted copy of the app's `sati_crown_glyph`.
`assets/packs/*.svg` — premium icon-pack samples from the app's Travel/Grocery packs.
`assets/logo.jpg` — the real app icon.

> ⚠️ Naming trap: the app asset literally named `mind_mirror` is the calc+bolt art,
> **not** a magnifier. The real magnifier "examining" pose is `pangolin_scanning_v1_1`
> (→ `mind-insight.png`).

To re-export after app art changes:
```bash
sips -Z 640 "<app>/MindSpend/Assets.xcassets/<set>.imageset/<file>.png" --out assets/mascot/<name>.png
```

Optional still owed: `assets/qr.png` — real QR to the App Store link (final CTA falls
back to a placeholder box if absent).
