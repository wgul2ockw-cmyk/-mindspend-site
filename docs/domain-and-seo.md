# mindspend.co: hosting, DNS, and SEO

## Detected host

The website is `wgul2ockw-cmyk/-mindspend-site`, a plain HTML/CSS/JavaScript marketing and support site. The separate private `MindSpend` repository is the native iOS app; this change does not turn it into a web app.

GitHub Pages publishes `main` from `/` using branch-based deployment (`build_type: legacy`). Preserve that source and `.nojekyll`. There is no Next.js, Vite, Cloudflare, Netlify, Vercel, server, database, or framework metadata API to configure. `CNAME` must contain exactly `mindspend.co`. The GitHub Pages custom-domain setting must also show that domain.

Before this change, the public site was `https://wgul2ockw-cmyk.github.io/-mindspend-site/`. All existing `.html` and blog paths remain available. Directory-style home/blog links consolidate the preferred URLs without deleting `index.html`. GitHub Pages handles the old host and www redirects once the domain is active. It does not support arbitrary `_redirects` or server-level rewrite rules; canonical tags consolidate `index.html` aliases.

## Exact DNS records

DNS is currently hosted on Spaceship (`launch1.spaceship.net`, `launch2.spaceship.net`). In **Advanced DNS → mindspend.co → DNS records → Custom records**, use these values with TTL **3600 seconds / 1 hour**, or Automatic:

| Type | Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | wgul2ockw-cmyk.github.io |

Replace the website parking records only. Before the change, apex A answers were `34.216.117.25` and `54.149.79.189`. Preserve unrelated MX/TXT and email records. Keep the existing Spaceship nameservers. The www target is a hostname: no `https://`, slash, or repository path.

Optional IPv6 support uses four additional `AAAA` records at `@`: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`. Existing conflicting apex AAAA records must not remain. No wildcard is needed.

Configure the GitHub custom domain before switching DNS. After propagation, wait for GitHub's certificate and enable **Enforce HTTPS**. A pending DNS/certificate check is not proof the domain is live. Verify HTTPS on both apex and www, a real article path, and an unknown path returning HTTP 404. GitHub says DNS propagation and certificate controls may take up to 24 hours.

## SEO implementation

- Unique Thai title and description, HTTPS canonical, robots index/follow, Open Graph and Twitter summary-large-image metadata on all 10 published pages.
- Shared 1200 × 630 PNG social preview using the existing logo and approved mascot; image URL, dimensions, content type and alt text included.
- Original logo reused for favicon.ico, 48px PNG favicon, 180px Apple touch icon, and 192/512px web manifest icons. Manifest uses browser display mode; it does not claim offline functionality.
- Schema.org Organization, WebSite, page types, MobileApplication, BreadcrumbList and BlogPosting. Article dates and author match visible bylines. No unverified reviews, rating counts, offers, store URLs or Android claims are added. Software-app rich results are not claimed.
- `robots.txt` allows crawling and advertises the 10-URL `sitemap.xml`. The article template and real 404 page use `noindex, follow` and are omitted from the sitemap. They remain crawlable so bots can see noindex.
- Blog social/copy links use the canonical production URL; home/blog navigation uses the preferred directory URLs. Broken `#premium` / `#guru` links are repaired. Changelog's existing visual title becomes H1. No-JavaScript visitors can see reveal sections.
- Removed the missing `assets/qr.png` request and its nonfunctional QR placeholder. A working app-store QR requires the real download URL.
- Privacy policy's Thai/English toggle remains on one URL. No fictional translated URLs or hreflang pairs are generated.

## Maintenance and build

Requires Python 3.9+; no third-party Python packages. Node/npm is optional shorthand.

```sh
python3 scripts/site.py check  # or npm run audit:seo
python3 scripts/site.py build  # or npm run build
```

`build` validates metadata, JSON-LD, sitemap, canonical consistency, H1s, local links/fragments and PNG dimensions, then creates `_site/` from a public-file allowlist. This is a verification/package artifact; branch-based Pages continues publishing the committed root files. The new GitHub Actions validation workflow runs on pull requests and main pushes; the existing Pages deployment is retained.

Edit `scripts/seo-pages.json` for metadata. For a new article, copy the template, replace TODO values, remove noindex, add a config entry with the visible publication date, then run `python3 scripts/site.py write` and `python3 scripts/site.py build`. Generated SEO is committed in HTML so bots never need JavaScript to get it. The audit fails if a page is missing from the indexable/noindex registry or generated content drifts.

## Remaining product/content facts to confirm

Existing App Store/Google Play and social profile buttons use placeholder `#` links. Existing support addresses use `support@mindspend.app`; changing website DNS does not create a mailbox. The site's privacy language and company footer should be reconciled with the current iOS release and developer details in a separate content review. These pre-existing claims were not expanded into schema. Supply verified store/profile URLs before replacing those links.

After HTTPS works, verify the property in Google Search Console and submit `https://mindspend.co/sitemap.xml`. Search Console's ownership TXT value is account-specific and cannot be invented. Indexing and rankings require Google's crawl and are not guaranteed by a successful build.

## Recovery

For a content regression, revert the release commit via a new commit and let the existing Pages job redeploy; keep the valid CNAME/domain mapping. For a domain rollback, first restore a working DNS destination and then remove the Pages custom-domain setting and CNAME together. Do not leave GitHub DNS pointing to an unclaimed/deleted Pages site. The pre-change source is the parent of this release's commit.

## References

- [GitHub Pages custom-domain and DNS instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [Spaceship DNS record management](https://www.spaceship.com/en-GB/knowledgebase/dns-records-types/)
- [Google software-app structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app)
