#!/usr/bin/env python3
"""Static SEO generation, integrity audit, and production packaging (stdlib only)."""
import html
import json
from pathlib import Path
import re
import shutil
import struct
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = 'https://mindspend.co'
PAGES = json.loads((ROOT / 'scripts/seo-pages.json').read_text())
EXCLUDED = {'blog/post-template.html', '404.html'}
START, END = '<!-- SEO:START -->', '<!-- SEO:END -->'
SOCIAL = ORIGIN + '/assets/og/mindspend.png'
ALT = 'MindSpend — เข้าใจการใช้เงิน ได้อย่างไม่ตัดสิน พร้อมน้องมายด์'

def canonical(path):
    return ORIGIN + '/' + (path[:-10] if path.endswith('index.html') else path)

def plain(value):
    return html.unescape(re.sub('<[^>]+>', '', value)).strip()

def metadata(path, data, source):
    url = canonical(path)
    title, desc = data['title'], data['description']
    article = data['type'] in ('BlogPosting', 'Article')
    language = data.get('lang', 'th')
    image_alt = ALT if language == 'th' else 'MindSpend — understand your spending without judgment, with Mind'
    tags = [f'<title>{html.escape(title)}</title>']
    def meta(key, value, prop=False):
        tags.append(f'<meta {"property" if prop else "name"}="{key}" content="{html.escape(value, quote=True)}">')
    meta('description', desc)
    meta('robots', 'index, follow, max-image-preview:large')
    tags.append(f'<link rel="canonical" href="{url}">')
    for lang, target in data.get('alternates', {}).items():
        tags.append(f'<link rel="alternate" hreflang="{lang}" href="{canonical(target)}">')
    for key, value in {
        'og:site_name':'MindSpend', 'og:locale':'th_TH' if language == 'th' else 'en_US',
        'og:type':'article' if article else 'website', 'og:url':url,
        'og:title':title, 'og:description':desc, 'og:image':SOCIAL,
        'og:image:secure_url':SOCIAL, 'og:image:type':'image/png',
        'og:image:width':'1200', 'og:image:height':'630', 'og:image:alt':image_alt,
    }.items(): meta(key, value, True)
    for key, value in {'twitter:card':'summary_large_image', 'twitter:title':title,
        'twitter:description':desc, 'twitter:image':SOCIAL, 'twitter:image:alt':image_alt}.items(): meta(key, value)
    meta('theme-color', '#F7F3ED')
    meta('application-name', 'MindSpend')
    # Relative assets keep the existing GitHub project-path preview usable too.
    prefix = '../' * (len(Path(path).parts) - 1) or './'
    tags.extend([
        f'<link rel="icon" href="{prefix}favicon.ico" sizes="any">',
        f'<link rel="icon" type="image/png" sizes="48x48" href="{prefix}assets/icons/favicon-48.png">',
        f'<link rel="apple-touch-icon" sizes="180x180" href="{prefix}assets/icons/apple-touch-icon.png">',
        f'<link rel="manifest" href="{prefix}site.webmanifest">',
    ])
    publisher = {'@type':'Organization', '@id':ORIGIN+'/#organization',
        'name':'MindSpend', 'url':ORIGIN+'/',
        'logo':{'@type':'ImageObject', 'url':ORIGIN+'/assets/icons/icon-512.png', 'width':512, 'height':512}}
    website = {'@type':'WebSite', '@id':ORIGIN+'/#website', 'name':'MindSpend',
        'url':ORIGIN+'/', 'inLanguage':['th', 'en'], 'publisher':{'@id':publisher['@id']}}
    page = {'@type':'WebPage' if article else data['type'], '@id':url+'#webpage',
        'url':url, 'name':title, 'description':desc, 'inLanguage':language,
        'isPartOf':{'@id':website['@id']},
        'primaryImageOfPage':{'@type':'ImageObject','url':SOCIAL,'width':1200,'height':630}}
    graph = [publisher, website, page]
    if path != 'index.html':
        items = [('MindSpend', ORIGIN+'/')]
        if path.startswith('blog/') and article: items.append(('บทความ', ORIGIN+'/blog/'))
        items.append((title, url))
        crumbs = {'@type':'BreadcrumbList', '@id':url+'#breadcrumbs',
            'itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':link}
                               for i,(name,link) in enumerate(items)]}
        page['breadcrumb'] = {'@id':crumbs['@id']}
        graph.append(crumbs)
    if path == 'index.html':
        app = {'@type':'MobileApplication','@id':ORIGIN+'/#app', 'name':'MindSpend',
            'url':ORIGIN+'/', 'description':desc,'applicationCategory':'FinanceApplication',
            'operatingSystem':'iOS', 'inLanguage':'th', 'publisher':{'@id':publisher['@id']},
            'image':ORIGIN+'/assets/icons/icon-512.png', 'sameAs':'https://jovey.co/mindspend/'}
        # No fabricated app-store URL, ratings, prices, or Android availability.
        page['about'] = {'@id':app['@id']}
        graph.append(app)
    if article:
        headline = plain(re.search(r'<h1\b[^>]*>(.*?)</h1>', source, re.S)[1])
        meta('article:published_time', data['published'], True)
        author = {'@type':'Organization','@id':ORIGIN+'/about.html#team','name':'MindSpend Team','url':ORIGIN+'/about.html'}
        graph.extend([author, {'@type':data['type'], '@id':url+'#article',
            'headline':headline,'description':desc,'url':url,'inLanguage':language,
            'datePublished':data['published'], 'author':{'@id':author['@id']},
            'publisher':{'@id':publisher['@id']}, 'image':SOCIAL,
            'mainEntityOfPage':{'@id':page['@id']},'isPartOf':{'@id':website['@id']}}])
    payload = json.dumps({'@context':'https://schema.org','@graph':graph}, ensure_ascii=False, indent=2).replace('<','\\u003c')
    tags.append('<script type="application/ld+json">\n'+payload+'\n</script>')
    return START+'\n'+'\n'.join(tags)+'\n'+END

def generated():
    yield 'CNAME', 'mindspend.co\n'
    yield 'robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: https://mindspend.co/sitemap.xml\n'
    # Let crawlers fetch noindex pages. Blocking them here would hide the noindex directive.
    urls = '\n'.join(f'  <url><loc>{canonical(p)}</loc></url>' for p in PAGES)
    yield 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'\n</urlset>\n'
    manifest = {'id':'./', 'name':'MindSpend', 'short_name':'MindSpend', 'lang':'th',
        'description':'เข้าใจการใช้เงิน ได้อย่างไม่ตัดสิน', 'start_url':'./','scope':'./',
        'display':'browser','background_color':'#F7F3ED','theme_color':'#F7F3ED',
        'icons':[{'src':f'assets/icons/icon-{size}.png','sizes':f'{size}x{size}','type':'image/png','purpose':'any'} for size in (192,512)]}
    yield 'site.webmanifest', json.dumps(manifest, ensure_ascii=False, indent=2)+'\n'

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.ids=set(); self.h1=0
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if 'id' in a: self.ids.add(a['id'])
        if tag=='h1': self.h1+=1

def write():
    for path, data in PAGES.items():
        target=ROOT/path; source=target.read_text()
        block=metadata(path,data,source)
        if START in source:
            source=re.sub(re.escape(START)+r'.*?'+re.escape(END), lambda _:block,source,flags=re.S)
        else:
            head,body=source.split('</head>',1)
            head=re.sub(r'<title>.*?</title>\s*','',head,flags=re.S)
            head=re.sub(r'<meta\b[^>]*(?:name="description"|property="og:[^"]+")[^>]*>\s*','',head)
            head=re.sub(r'<link\b[^>]*rel="icon"[^>]*>\s*','',head)
            head=head.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'+block)
            source=head+'</head>'+body
        target.write_text(source)
    for path,value in generated(): (ROOT/path).write_text(value)
    print('SEO metadata generated for',len(PAGES),'pages.')

def check():
    errors=[]
    def require(ok,message):
        if not ok: errors.append(message)
    paths=set(PAGES)|EXCLUDED
    found={str(p.relative_to(ROOT)) for p in ROOT.glob('*.html')}|{str(p.relative_to(ROOT)) for p in (ROOT/'blog').glob('*.html')}
    require(found==paths,'Every HTML page must be registered or explicitly noindex: '+str(found^paths))
    docs={p:Document((ROOT/p).read_text()) for p in paths}
    for path in paths:
        source=(ROOT/path).read_text(); doc=docs[path]
        require(doc.h1==1,f'{path}: expected one H1')
        require(any(t=='meta' and a.get('name')=='viewport' for t,a in doc.tags),f'{path}: missing viewport')
        for tag,a in doc.tags:
            if tag=='img': require('alt' in a,f'{path}: image missing alt')
            if tag not in ('a','img','link','script','source'): continue
            ref=a.get('src') or a.get('href')
            if not ref or ref=='#': continue
            u=urlsplit(urljoin(canonical(path),ref))
            if u.scheme not in ('http','https') or u.netloc!='mindspend.co': continue
            rel=unquote(u.path).lstrip('/')
            if not rel or rel.endswith('/'): rel+='index.html'
            require((ROOT/rel).is_file(),f'{path}: broken local target {ref}')
            if u.fragment and rel in docs:
                require(unquote(u.fragment) in docs[rel].ids,f'{path}: broken fragment {ref}')
        if path in EXCLUDED:
            require(any(t=='meta' and a.get('name')=='robots' and 'noindex' in a.get('content','') for t,a in doc.tags),f'{path}: missing noindex')
            continue
        language=PAGES[path].get('lang', 'th')
        require(any(t=='html' and a.get('lang')==language for t,a in doc.tags),f'{path}: HTML language mismatch')
        alternates=PAGES[path].get('alternates', {})
        if alternates:
            require(alternates.get(language)==path,f'{path}: missing self-referencing hreflang')
            for lang,target in alternates.items():
                require(target in PAGES,f'{path}: unknown hreflang target {target}')
                if target in PAGES:
                    require(PAGES[target].get('alternates')==alternates,f'{path}: nonreciprocal hreflang')
                    if lang!='x-default': require(PAGES[target].get('lang','th')==lang,f'{path}: hreflang target language mismatch')
        expected=metadata(path,PAGES[path],source)
        require(expected in source,f'{path}: metadata drift; run npm run seo:write')
        require(len(re.findall(r'<title>',source))==1,f'{path}: duplicate title')
        for attr,val in [('name','description'),('name','robots'),('property','og:url'),('name','twitter:card')]:
            require(sum(t=='meta' and a.get(attr)==val for t,a in doc.tags)==1,f'{path}: duplicate/missing {val}')
        require(sum(t=='link' and a.get('rel')=='canonical' for t,a in doc.tags)==1,f'{path}: duplicate/missing canonical')
        require('wgul2ockw-cmyk.github.io/-mindspend-site' not in source,f'{path}: legacy URL still present')
        require('TODO' not in source,f'{path}: placeholder in published page')
        blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S)
        require(len(blocks)==1,f'{path}: expected one structured-data graph')
        for block in blocks: json.loads(block)
    # Indexable pages must be discoverable through ordinary HTML links from home.
    reached={'index.html'}
    pending=['index.html']
    while pending:
        path=pending.pop()
        for tag,a in docs[path].tags:
            if tag!='a' or not a.get('href'): continue
            u=urlsplit(urljoin(canonical(path),a['href']))
            if u.netloc!='mindspend.co': continue
            target=unquote(u.path).lstrip('/')
            if not target or target.endswith('/'): target+='index.html'
            if target in PAGES and target not in reached:
                reached.add(target); pending.append(target)
    require(reached==set(PAGES),'Orphan indexable pages: '+str(set(PAGES)-reached))
    require(len({d['title'] for d in PAGES.values()})==len(PAGES),'Duplicate page titles')
    require(len({d['description'] for d in PAGES.values()})==len(PAGES),'Duplicate descriptions')
    for path,expected in generated(): require((ROOT/path).read_text()==expected,f'{path}: generated file drift')
    sitemap=ET.parse(ROOT/'sitemap.xml')
    urls=[e.text for e in sitemap.findall('.//{*}loc')]
    require(set(urls)=={canonical(p) for p in PAGES} and len(urls)==len(PAGES),'Sitemap coverage mismatch')
    for path,size in [('assets/og/mindspend.png',(1200,630)),('assets/icons/favicon-48.png',(48,48)),
        ('assets/icons/apple-touch-icon.png',(180,180)),('assets/icons/icon-192.png',(192,192)),('assets/icons/icon-512.png',(512,512))]:
        file=ROOT/path
        require(file.exists(),f'Missing image {path}')
        if file.exists():
            data=file.read_bytes()
            require(data[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',data[16:24])==size,f'{path}: invalid dimensions')
    require((ROOT/'favicon.ico').is_file(),'Missing favicon.ico')
    require((ROOT/'.nojekyll').is_file(),'Missing .nojekyll')
    if errors:
        print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
    print(f'PASS: {len(PAGES)} indexable pages, {len(EXCLUDED)} noindex pages, canonical/schema/social metadata, sitemap, icons and internal links.')

def build():
    check()
    out=ROOT/'_site'
    if out.exists(): shutil.rmtree(out)
    out.mkdir()
    files=list(PAGES)+list(EXCLUDED)+['CNAME','robots.txt','sitemap.xml','site.webmanifest','favicon.ico','.nojekyll','styles.css','theme.css']
    for path in files:
        target=out/path; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/path,target)
    shutil.copytree(ROOT/'assets',out/'assets')
    print('Production static artifact built at _site/ (same pages and assets as branch-based GitHub Pages).')

if __name__=='__main__':
    actions={'write':write,'check':check,'build':build}
    action=sys.argv[1] if len(sys.argv)>1 else 'check'
    if action not in actions: raise SystemExit('Usage: site.py write|check|build')
    actions[action]()
