# MindSpend search expansion — 10 September 2026

The site is reachable and its homepage appears in an exact-domain Google search. The work here broadens the useful tasks a search visitor can complete: understand the app's free core, start a monthly plan, calculate a savings contribution, split a bill, or review a receipt workflow. It expands 17 indexable pages to 25, preserving established URLs.

## Evidence and limits

- Live baseline: homepage and sitemap returned HTTP 200. Homepage permits indexing and has a self canonical. Google Search Console's verified URL-prefix property is `https://mindspend.co/`, not the unverified domain property.
- Search Console on 10 September: sitemap status Success; last read 9 September; 17 discovered pages. Overview showed 0 clicks and indexing data still processing. Discovered is not indexed; zero recorded clicks is not a confirmed keyword ranking.
- No connected keyword-volume or backlink provider. The priorities below reflect product fit and observed search intent, not measured monthly volume, keyword difficulty scores, or proven rankings. Search Console will provide the useful first-party evidence as impressions arrive.
- MindSpend's official app download URL remains unverified. Existing contact CTA is retained. No third-party app with the same name is linked as this product.

## Keyword map

One useful destination covers closely related phrases; we do not create separate copies for each word order. Difficulty is a qualitative assessment of breadth and competing product pages, not a numeric SEO-tool measurement. Current positions are unmeasured for every term below.

| Query | Intent | Priority | Qualitative difficulty | Destination |
|---|---|---|---|---|
| MindSpend | Brand navigation | High | Brand-name ambiguity | `/`, `/en.html` |
| budget tracker free | Product / free tool | High | Hard | `/free-budget-tracker.html` |
| free budget tracker | Product / free tool | High | Hard | `/free-budget-tracker.html` |
| free expense tracker | Product comparison | High | Hard | `/free-budget-tracker.html` |
| expense tracker app for iPhone | Product comparison | High | Hard | `/free-budget-tracker.html` |
| money manager app | Product comparison | Medium | Hard | `/en.html` |
| monthly budget planner | Tool | High | Hard | `/monthly-budget-planner.html` |
| budget calculator | Tool | High | Hard | `/monthly-budget-planner.html` |
| free budget planner | Tool | High | Hard | `/monthly-budget-planner.html` |
| 50/30/20 budget calculator | Specific tool | High | Moderate | `/monthly-budget-planner.html` |
| savings goal calculator | Specific tool | High | Moderate | `/savings-goal-calculator.html` |
| how much to save each month for a goal | Informational / tool | High | Moderate | `/savings-goal-calculator.html` |
| savings goal tracker | Product / tool comparison | Medium | Moderate | `/savings-goal-calculator.html` |
| split bill calculator | Specific tool | High | Moderate | `/split-bill-calculator.html` |
| tip calculator | Tool | Medium | Hard | `/split-bill-calculator.html` |
| receipt scanner app | Product comparison | Medium | Hard | `/receipt-scanner.html` |
| Thai payment slip reader | Specific workflow | High | Moderate | `/receipt-scanner.html` |
| แอปบันทึกรายรับรายจ่ายฟรี | Product comparison | High | Hard | `/budget-tracker-free-th.html` |
| แอปบันทึกรายจ่าย iPhone | Product comparison | High | Moderate | `/budget-tracker-free-th.html` |
| ตารางรายรับรายจ่ายฟรี | Download / template | High | Moderate | `/budget-tracker-free-th.html` |
| วางแผนงบรายเดือน | Informational / tool | High | Moderate | `/monthly-budget-planner-th.html` |
| คำนวณเงินออม | Specific tool | High | Moderate | `/savings-goal-calculator-th.html` |
| หารบิล | Specific tool | High | Moderate | `/split-bill-calculator-th.html` |
| สแกนสลิป บันทึกรายจ่าย | Specific workflow | High | Moderate | `/receipt-scanner-th.html` |
| เงินเดือนหมดไปไหน | Informational | Medium | Moderate | `/blog/salary-gone-where.html` |

## Audit findings and implemented changes

| Surface | Finding | Priority | Implementation |
|---|---|---|---|
| Thai / English homepage | Brand-led hero did not promptly identify the budget / expense task | High | Product and free-core context in title, description, eyebrow, and introductory text; preserves the approved visual hierarchy |
| Free tracker pair | Visitors needed a clearer comparison of CSV, browser tools, native app and paid automation | High | Direct expense-tracker H1, task comparison table, receipt/privacy limits, links to usable tools |
| Budget / savings / shared expenses | No immediate web tool for visitors arriving with a calculation task | High | Three calculators in two languages, worked examples, formulas, limitations and next steps |
| Receipt scanning | Feature existed in app but had no dedicated workflow explanation | High | Bilingual original guide covering receipt vs payment slip, draft review, duplicates, AI consent and app access |
| Crawl paths | New destinations require ordinary links, not only a sitemap | High | Home links to three calculators; free-tracker pair and related links connect all four topics |
| Sitemap | No meaningful modification dates or language relationships | Medium | Explicit dates for changed pages and reciprocal language alternates; no invented dates for unchanged pages |
| Structured data | New tools need accurate page identity | Medium | WebApplication for actual free tools, Article for receipt guide, breadcrumb and language metadata; no invented ratings or app store offers |
| Integrity | New templates and calculator arithmetic could drift silently | High | Render consistency in CI; conservation and edge-case tests; duplicate-ID check added to existing SEO audit |

## Search landscape observations

These are observations of public product pages, not a backlink or ranking comparison.

| Site | Observed positioning | Useful implication for MindSpend |
|---|---|---|
| [Crena](https://crena.app/en/) | Direct free iPhone expense-tracker introduction and monthly-budget positioning | State platform and free scope before detailed product storytelling |
| [Wallet Note](https://walletnote.app/) | Thai-first income/expense tracking with clear free and paid boundaries | Write native Thai explanations and make feature access explicit |
| [CashJot](https://www.cashjot.com/) | Daily expense workflow and specific no-bank-linking use cases | Explain the exact workflow and privacy boundary rather than broad unsupported promises |

No verified domain-authority score, backlink count, competitor publishing cadence, or market-wide search-volume estimate is available. Broad English terms face established apps and tools; narrower task-specific pages provide a clearer starting point without guaranteeing lower ranking difficulty.

## Validation

- Static SEO audit and production build: 25 indexable + 2 deliberately noindex pages; titles/descriptions unique; canonicals, reciprocal hreflang, XML, internal targets/fragments, schema, icons, and ordinary crawl reachability pass.
- Both generators reproduce the committed HTML; all JavaScript syntax checks pass.
- Four automated test groups cover exact-cent conservation over multiple amounts/group sizes/tip rates, savings final payments, overallocated budgets, zero values, invalid values and bounds.
- Browser checks: all 12 new or substantially updated pages at 320px have one H1, no document overflow, and no broken loaded images. Thai 390px and English 1440px screenshots inspected.
- Interactive checks: budget shortfall, USD formatting, savings 100 over three months (33.34 / 33.34 / 33.32), blank input clearing old output, and 1,200 + 10% / four people = 330. Enter-key calculation retains the same URL with no input query string.
- Calculator controls are disabled in source until JavaScript initializes; no-JavaScript readers retain formulas, examples, links and downloads without submitting entered amounts through a native GET form.
- Core Web Vitals: no field-data claim. The Search Console baseline has insufficient field data; browser layout checks are not a Lighthouse or real-user score.

## Next measurements and dependencies

1. Confirm production content after Pages deployment; resubmit the existing sitemap once so Google sees the expanded URL set.
2. Inspect the homepage and principal free-tracker URL in the verified Search Console property. Request recrawl when appropriate; repeated requests do not force inclusion.
3. Compare 28-day Search Console windows once enough data exists: query impressions, clicks, CTR and average position by page, language, country and device. Avoid reading a zero-impression page's average position as zero rank.
4. When the user supplies the official App Store/TestFlight URL, replace the contact-download path and verify the correct developer/product. This is the largest remaining conversion dependency.
5. Prioritize future content from actual queries and user questions. Extend an existing page for a synonym; add a new page only when it can answer a materially different task. Editorial partnerships or external posts require separate user authorization.

## Sources for implementation choices

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [People-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Spam policies: doorway and scaled content abuse](https://developers.google.com/search/docs/essentials/spam-policies)
- [Accurate sitemap lastmod](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping)
- [Software application structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app)
- [CFPB introductory budget exercise](https://www.consumerfinance.gov/consumer-tools/educator-tools/youth-financial-education/teach/activities/analyzing-budgets/)

Implementation and deployment are measurable deliverables. Google indexing, traffic, ranking and app-download conversion remain separate outcomes.
