# น้องมายด์ mascot art — REAL app assets (synced 2026-07-10)

These PNGs are exported from the iOS app's `MindSpend/Assets.xcassets` (the shipping
mascot art), resized with `sips` to ≤800px on the long edge, transparent background.
The site references them directly; if a file is missing the page auto-falls back to a
flat placeholder SVG (`assets/mind-*.svg`), so the site never breaks.

Interaction: any mascot with `data-mind` talks on click/tap (Itim speech bubble via
`assets/mind.js`). Voice rules: observational, register-high / valence-zero —
น้องมายด์ never tells the user what to do.

| File | App source (imageset) | Pose | Used in |
|------|----------------------|------|---------|
| `mind-hero.png`      | `splash_hero`                    | greeting + calc/bolt clouds | Home hero · support header |
| `mind-track.png`     | `Pangolin/pangolin_scanning_v2_1`| calculator + bolt     | How 01 (frame A) |
| `mind-scan-b.png`    | `Pangolin/pangolin_scanning_v2_2`| magnifier over slip   | How 01 (frame B of scan loop) |
| `mind-cheer.png`     | `Pangolin/pangolin_cheer`        | happy ^^ wave         | How 03 · footer wake state |
| `mind-greet.png`     | `splash_hero`                    | greeting + calc/bolt clouds | Relationship section |
| **Feature row — 5 distinct poses (one per card):** | | | |
| `mind-insight.png`   | `Pangolin/pangolin_scanning_v1_1`| magnifier + receipt (examining) | Feature 1 · สรุปเชิงลึก |
| `mind-warm.png`      | `Pangolin/pangolin_waving`       | waving, happy eyes, blush | Feature 2 · อารมณ์ & การเงิน |
| `mind-celebrate.png` | `Pangolin/pangolin_celebrate`    | double thumbs-up + sparkle eyes | Feature 3 · เป้าหมาย · final CTA · changelog |
| `mind-think.png`     | `mind_income_question`           | ? bubble, curious     | Feature 4 · รายงาน · How 02 · FAQ |
| `mind-sleep.png`     | `mind_sleeping`                  | curled, zzz           | Feature 5 · แจ้งเตือน · footer (tap to wake) |

> ⚠️ The app asset named `mind_mirror` is actually the calc+bolt greeting art (misleading name) — the real magnifier "examining" pose lives in `pangolin_scanning_v1_1`, exported here as `mind-insight.png`.
| `mind-stand.png`     | `Pangolin/pangolin_standing`     | neutral standing      | Blog index · post template |
| `mind-king.png`      | `sati_member_mascot_standing`    | premium member pose   | สติ+ section (crown overlaid via `assets/crown-gold.svg`, same glyph as the app's `sati_crown_glyph`) |

`assets/crown-gold.svg` — gold-tinted copy of the app's `sati_crown_glyph/crown.svg`.

To re-export after app art changes:
```bash
sips -Z 640 "<app>/MindSpend/Assets.xcassets/<set>.imageset/<file>.png" --out assets/mascot/<name>.png
```

Optional: `assets/qr.png` — a real QR code pointing to the App Store link, shown in
the final CTA. Falls back to a placeholder box if absent.
