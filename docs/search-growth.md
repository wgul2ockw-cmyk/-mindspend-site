# MindSpend search content

Published content is static HTML, with no JavaScript needed to read the guides or find their links. Run `npm run build` before committing changes.

## Page ownership

| Search intent | English | Thai |
|---|---|---|
| Free budget and expense tracking | `/free-budget-tracker.html` | `/budget-tracker-free-th.html` |
| Financial freedom through cash-flow planning | `/financial-freedom.html` | `/financial-freedom-th.html` |
| Mindful spending and better money habits | `/spending-habits.html` | `/spending-habits-th.html` |

Each pair has its own canonical URLs, reciprocal `en` / `th` hreflang, and English `x-default`. These are six pages for three distinct reader needs; add substantive content to the existing owner page before creating overlapping pages for keyword variations. The homepage remains the Thai product page.

The daily expense logs and monthly budget worksheets in `assets/downloads/` are blank UTF-8 BOM CSVs, in both languages. They are manual worksheets with no formulas, bank connection, or app sync. Keep the download labels and description accurate. The free core app tier is distinct from the optional Sati+ trial. The published app limits were taken from the existing homepage/FAQ, not inferred from a competitor with the same name.

## Related project

`https://jovey.co/mindspend/` is a separate project story with editorial links to this site's guides. MindSpend's About page links to Jovey and its creator page. Use direct canonical links with descriptive anchors. Do not add repeated keyword links or represent different organisations as the same schema.org entity. The MobileApplication entity links to the Jovey project story with `sameAs`; Jovey's organisation no longer claims to be the MindSpend website.

## Verification

`scripts/site.py` checks metadata drift, unique titles/descriptions, one H1, language declarations, reciprocal/self-referencing hreflang, sitemap coverage, local files/fragments, image dimensions, and that every indexable page can be reached through ordinary links from home. Keep Article bylines and publication dates visible and consistent with metadata.

The existing GitHub Pages `main` / root deployment and custom-domain configuration are retained. Revert a release through a new commit for a content rollback; do not change DNS or CNAME for a content problem.

## Search measurement

The Search Console property and sitemap were verified before this change. The existing sitemap URL is still `https://mindspend.co/sitemap.xml`; the registry now contains 16 indexable URLs. Sitemap acceptance is distinct from indexing or rankings. Compare impressions, clicks, CTR, and average position by page, query, country, and device once data is available. No search-volume, difficulty, backlink-authority, or current-ranking measurements were available for this release.

References: [Google's localized-page instructions](https://developers.google.com/search/docs/specialty/international/localized-versions) and [spam policies](https://developers.google.com/search/docs/essentials/spam-policies). Public financial guides cite Bank of Thailand and CFPB sources inline; the worked examples are original illustrations, not app efficacy claims.
