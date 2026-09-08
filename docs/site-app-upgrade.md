# September 2026 product site upgrade

The previous homepage illustrated the old Wallet and upcoming-money screens,
omitted the current MindScore and Community work, and linked store badges to `#`.
The product site now introduces the current app through the original Mind mascot,
an interactive five-part tour, and complete Thai and English homepages.

## Scope and sources

The app baseline is MindSpend main `957c96501a1557b58944216623c3fcf49207b631`,
verified against GitHub on 8 September 2026. Product descriptions were checked
against the R249 language, R252–255 Home/logging, R256 MindScore, R257 assets,
Community integration and Milestones change notes and their current source.

- MindScore: 30-day history gate, Monday-start weekly stamp, missing-data states,
  Health/Behavior/Adaptive. The score artwork uses the documented example
  76 and pillars 76/79/72; it is labeled fictional and is not a live calculation.
- Groups and bills are local. Received/undo is a status change, with no payment
  transfer or income entry. No public feed, invitations or recipient web service
  is advertised. The app's separate recipient-link destination is outside this release.
- Milestones only claim evidence-supported behavior. Unsupported definitions
  remain described as coming later.
- CloudSyncManager, ReceiptAIConsent, ImportAIConsentStore, MindAIConsent and
  SplitLinkBuilder inform the updated data-flow descriptions in both privacy languages.
- EntitlementGate informs the free history and custom-category limits. Actual
  StoreKit prices and trial eligibility are left to the in-app purchase screen.
- The iOS deployment target is 17.6. The app-store distribution status of this
  development baseline is not represented as verified.

No official App Store/TestFlight URL could be established from the repository.
Apple search returned apps belonging to other developers, so download calls to
action route to the existing contact page. Replace them only with a verified
official URL. Existing contact details are retained; no messages were sent.

## Architecture and maintenance

- `scripts/render_home.py` is the shared Thai/English authoring source. It renders
  `index.html` and `en.html` and preserves each page's generated SEO block.
- `assets/site-v2.css` and `assets/site-v2.js` contain the product-page presentation
  and progressive enhancements. All copy is static HTML; no translation API,
  build dependency, remote data, application account or backend was added.
- The only persisted website preference is the existing `ms-theme` key. Tour,
  spending-perspective and score-example selections are transient DOM state.
- The original mascot assets, existing guides, CSV downloads and canonical domain
  remain. Home no longer carries its own duplicated inline style system.
- Existing support pages keep their routes and anchors. FAQ uses native details;
  `assets/site-refresh.css` aligns supporting pages, while the shared interaction
  script adds accessible mobile navigation. The guide article content is retained
  apart from corrections to obsolete product claims and navigation.
- No Swift, HomeView state, DataStore, model schema, secrets or app resources changed.

To author and verify:

```sh
python3 scripts/render_home.py
python3 scripts/site.py write
python3 scripts/render_home.py --check
python3 scripts/site.py build
node --check assets/site-v2.js
node --check assets/mind.js
git diff --check
```

The local Homebrew Python 3.14 has an unrelated expat dynamic-link failure;
`/usr/bin/python3` successfully runs these checks. CI uses Python 3.12. The renderer
declares UTF-8 explicitly for compatibility with the system Python 3.9 tokenizer.

## Verification and release gates

- Static integrity: 17 indexable pages, 2 noindex pages, canonical and reciprocal
  language alternates, schema/social metadata, sitemap, image paths and local links.
- Production artifact generated in `_site`; rendering reproducibility and both
  JavaScript syntax checks pass. These checks are also wired into CI.
- Browser: 1280px desktop, 390px mobile and 320px narrow layout; Thai/English,
  light/dark, theme retained across navigation, all five tour tabs, Arrow/Home/End
  tab controls, planned/impulse sample, ready/building MindScore states, native FAQ
  disclosures, mobile navigation, and privacy-language switching.
- Support, About, Changelog and Privacy were checked at 320px with no horizontal
  page overflow or failed loaded images. The checked browser session had no
  warning/error logs. Reduced motion and no-JS fallbacks were source-reviewed;
  OS-level reduced-motion emulation and a physical-device test were not performed.

Before merging, CI must pass on the proposed commit. After merging, confirm the
GitHub Pages build and verify the new homepage, English page, FAQ and assets on
`https://mindspend.co/`.

Rollback: revert the single site-upgrade merge commit if the homepage, product
tour, contact path or static assets fail in production. This is a static change
with no data migration or new external service.
