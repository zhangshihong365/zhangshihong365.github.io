#!/usr/bin/env python3
"""Build ready-to-publish HTML from content/site.json; Python standard library only.

Run from any directory: python3 /path/to/this/project/scripts/build.py
"""
import html
import json
import re
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
PROFILE = DATA['profile']
SITE = DATA['site']
BASE = Template((ROOT / 'templates/base.html').read_text(encoding='utf-8'))


def e(value):
    """Treat all content as plain text, including values read from the CV."""
    return html.escape(str(value), quote=True)


ICONS = {
    'pin': '<path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    'scholar': '<path d="m2 9 10-5 10 5-10 5-10-5Zm4 2v6c4 3 8 3 12 0v-6M22 9v8"/>',
    'linkedin': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.01M11 17v-7m0 3c0-4 6-4 6 0v4"/>',
    'file': '<path d="M14 3H5v18h14V8l-5-5Zm0 0v5h5M8 12h8M8 16h8"/>',
    'arrow': '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    'camera': '<path d="M3 6h4l2-3h6l2 3h4v15H3z"/><circle cx="12" cy="13" r="4"/>',
}


def icon(name):
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def link(url, label, css='', external=False):
    extra = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a href="{e(url)}" class="{e(css)}"{extra}>{label}</a>'


def heading(text, anchor):
    return f'<h2 class="section-title" id="{e(anchor)}">{e(text)}</h2>'



def papers_html(items):
    result = '<ol class="publication-list">'
    for p in items:
        authors = e(p['authors']).replace('Zhang, S.', '<strong>Zhang, S.</strong>')
        title = link(p['url'], e(p['title']), external=True) if p.get('url') else e(p['title'])
        status = '<span class="status">Under review</span>' if p['status'] == 'review' else ''
        result += (f'<li class="publication" data-status="{e(p["status"])}"><h3>{title}</h3>'
                   f'<p class="authors">{authors}</p><p class="venue">{e(p["venue"])}{status}</p></li>')
    return result + '</ol>'


def projects_html():
    result = []
    for project in DATA['projects']:
        title = link(project['url'], e(project['title']), external=True) if project.get('url') else e(project['title'])
        funding = f'<p class="muted">{e(project["funding"])}</p>' if project.get('funding') else ''
        result.append(f'<article class="project-item"><span class="eyebrow">{e(project["role"])}</span>'
                      f'<h3>{title}</h3>{funding}</article>')
    return ''.join(result)



def patents_html():
    return ''.join(f'<article class="record"><h3>{e(p["title"])}</h3>'
                   f'<p class="muted">{e(p["type"])} · {e(p["number"])}</p></article>'
                   for p in DATA['patents'])


def home():
    # Link exact institution/person names without linking Wuhan University of Technology.
    links = DATA.get('about_links', {})
    patterns = [re.escape(name) + ('(?! of Technology)' if name == 'Wuhan University' else '') for name in links]
    def linked_paragraph(text):
        if not patterns:
            return e(text)
        result, start = [], 0
        for match in re.finditer('|'.join(patterns), text):
            result.append(e(text[start:match.start()]))
            result.append(link(links[match.group()], e(match.group()), external=True))
            start = match.end()
        result.append(e(text[start:]))
        return ''.join(result)
    about = ''.join(f'<li>{linked_paragraph(p)}</li>' for p in DATA['about'])
    about += '<li>' + link('cv.html', 'Curriculum Vitae') + '</li>'
    def news_text(item):
        text = e(item['text'])
        if item.get('url') and item.get('link_text'):
            text = text.replace(e(item['link_text']), link(item['url'], e(item['link_text']), external=True), 1)
        return text
    news = ''.join(f'<li><span class="news-date">{e(n["date"])}</span><div><span class="news-type {e(n["type"].lower())}">{e(n["type"])}:</span> {news_text(n)}</div></li>' for n in DATA['news'])
    p = DATA['platforms'][0]
    return (f'<h1>About me</h1><ul class="intro-list">{about}</ul>'
            '<div class="section-heading"><h2>News</h2></div>'
            f'<ul class="news-list">{news}</ul>'
            f'<div class="section-heading"><h2>Research in practice</h2>{link("softwares.html", "Explore platforms " + icon("arrow"))}</div>'
            f'<figure class="featured-platform"><a href="softwares.html#platform-1"><img src="{e(p["image"])}" alt="{e(p["alt"])}" width="3012" height="1550" loading="lazy"></a>'
            f'<figcaption>{link("softwares.html#platform-1", e(p["title"]))}</figcaption></figure>')


def research():
    themes = ''.join(f'<li><h3>{e(t["title"])}</h3><p>{e(t["text"])}</p></li>' for t in DATA['themes'])
    return (f'<h1>{e(SITE["research_label"])}</h1><p class="lead">Geospatial approaches to building energy, renewable energy systems, and urban resilience.</p>'
            '<nav class="section-nav" aria-label="Research sections"><a href="#interests">Research interests</a><a href="#publications">Publications</a><a href="#projects">Projects</a><a href="#patents">Patents</a></nav>'
            f'{heading("Research interests", "interests")}<ul class="research-themes">{themes}</ul>'
            f'{heading("Publications", "publications")}'
            f'{papers_html(DATA["publications"])}'
            f'{heading("Research projects", "projects")}{projects_html()}'
            f'{heading("Patents", "patents")}{patents_html()}')


def supervision_html():
    return ''.join(f'<article class="record"><span class="eyebrow">{e(s["period"])}</span><p>{e(s["text"])}</p></article>' for s in DATA['supervision'])


def team():
    intro = e(DATA['team_intro']).replace('Urban Group', '<strong>Urban Group</strong>', 1).replace('Smart Building and Construction Lab', link(DATA['team_lab_url'], 'Smart Building and Construction Lab', external=True), 1)
    result = '<h1>Team</h1>' + f'<p class="team-intro">{intro}</p>'
    result += '<div class="team-members team-members-first">'
    for index, member in enumerate(DATA.get('team_members', [])):
        if index == 3:
            result += '</div><div class="team-members">' 
        portrait = f'<img src="{e(member["image"])}" alt="{e(member["name"])}" loading="lazy">'
        name = e(member['name'])
        if member.get('url'):
            portrait = link(member['url'], portrait, external=True)
            name = link(member['url'], name, external=True)
        result += f'<figure class="team-member">{portrait}<figcaption>{name}</figcaption></figure>'
    result += '</div>'
    return result + f'{heading("Student supervision", "supervision")}{supervision_html()}'



def teaching_html():
    return ''.join(f'<article class="record"><div class="record-header"><h3>{e(t["course"])} · {e(t["title"])}</h3><span class="record-date">{e(t["term"])}</span></div><p>{e(t["role"])}</p><p class="muted">{e(t["institution"])}</p></article>' for t in DATA['teaching'])


def teaching():
    return '<h1>Teaching</h1><p class="lead">Courses, tutorials, and guest lectures.</p>' + teaching_html()


def softwares():
    result = '<h1>Software</h1><p class="lead">Interactive geospatial platforms for energy modelling and building decarbonization.</p>'
    for i, p in enumerate(DATA['platforms'], 1):
        result += (f'<article class="platform" id="platform-{i}"><h2>{e(p["title"])}</h2>'
                   f'<p class="muted">{e(p["subtitle"])}</p><figure><img src="{e(p["image"])}" alt="{e(p["alt"])}" loading="lazy">'
                   f'<figcaption>{e(p["subtitle"])}</figcaption></figure><p>{e(p["description"])}</p>')
        if p['url']:
            result += link(p['url'], 'Visit platform ' + icon('arrow'), 'text-link', True)
        else:
            result += '<p class="small-note">Public link coming soon.</p>'
        result += '</article>'
    return result


def talks_html():
    return ''.join(f'<article class="talk"><div class="talk-date">{e(t["date"])}</div><div><h3>{e(t["title"])}</h3><p>{e(t["event"])}</p><p class="muted">{e(t["host"])}</p><p class="muted talk-location">{icon("pin")}<span>{e(t["location"])}</span></p></div></article>' for t in DATA['talks'])


def talks():
    return '<h1>Talks</h1><p class="lead">Conference presentations, seminars, and invited talks.</p>' + talks_html()


def service_html():
    s = DATA['service']
    result = heading('Internships', 'internships')
    for item in s['internships']:
        title = e(item['title'])
        if item.get('url') and item.get('link_text'):
            title = title.replace(e(item['link_text']), link(item['url'], e(item['link_text']), external=True), 1)
        result += (f'<article class="record"><div class="record-header"><h3>{title}</h3>'
                   f'<span class="record-date">{e(item["dates"])}</span></div>')
        if item.get("location"):
            result += f'<p class="muted">{e(item["location"])}</p>'
        result += '</article>'
    result += heading('Conference service', 'conferences')
    for item in s['conferences']:
        result += f'<article class="record"><h3>{e(item["title"])}</h3><p class="muted">{e(item["description"])}</p></article>'
    result += heading('Journal reviewer', 'reviewing')
    for area, journals in s['reviewing'].items():
        result += f'<h3>{e(area)}</h3><p class="journal-list">' + '; '.join(e(j) for j in journals) + '.</p>'
    result += heading('Memberships', 'memberships') + '<ul>'
    result += ''.join(f'<li>{e(m)}</li>' for m in s['memberships']) + '</ul>'
    return result


def service():
    return '<h1>Service</h1><p class="lead">Contributing to the geospatial, built environment, and energy research communities.</p>' + '<div class="service-details">' + service_html() + '</div>'


def records_html(items):
    return ''.join(
        f'<article class="record"><div class="record-header"><h3>{e(r["institution"])}</h3>'
        f'<span class="record-date">{e(r["dates"])}</span></div><p>{e(r["title"])}</p>'
        f'<p class="muted">Supervisor: {e(r["supervisor"])} · {e(r["location"])}</p></article>'
        for r in items)


def cv():
    return ('<h1>Curriculum Vitae</h1>'
            f'{heading("Education", "education")}{records_html(DATA["education"])}'
            f'{heading("Experience", "experience")}{records_html(DATA["experience"])}')



def moments():
    result = '<h1>Moments</h1><p class="lead">Beyond the research — people, places, and everyday discoveries.</p>'
    for m in DATA['moments']:
        result += '<article class="moment">'
        if m.get('date'):
            result += f'<time datetime="{e(m["date"])}">{e(m["date"])}</time>'
        result += f'<h2>{e(m["title"])}</h2>'
        if m.get('text'):
            result += f'<p>{e(m["text"])}</p>'
        images = m.get('images', [])
        if m.get('image'):
            images = [{'src': m['image'], 'alt': m.get('alt', m['title'])}] + images
        if images:
            gallery_class = 'moment-gallery moment-gallery-two' if len(images) == 2 else 'moment-gallery'
            result += f'<div class="{gallery_class}">'
            for photo in images:
                result += '<figure>' + link(photo['src'], f'<img src="{e(photo["src"])}" alt="{e(photo["alt"])}" loading="lazy">', external=True)
                if photo.get('caption'):
                    result += f'<figcaption>{e(photo["caption"])}</figcaption>'
                result += '</figure>'
            result += '</div>'
        result += '</article>'
    result += ('<a class="photography-entry" href="photography.html">'
               f'{icon("camera")}<span><strong>My Photography Portfolio</strong>'
               '<span>A collection of places, light, and everyday moments.</span></span>'
               f'{icon("arrow")}</a>')
    return result + visitor_map_html()


def photography():
    result = '<a href="moments.html">← Back to Moments</a><h1>My Photography Portfolio</h1>'
    if not DATA.get('photography'):
        return result + '<p class="lead">Photographs will be shared here soon.</p>'
    result += '<div class="photography-gallery">'
    for photo in DATA['photography']:
        result += '<figure>' + link(photo['src'], f'<img src="{e(photo["src"])}" alt="{e(photo["alt"])}" loading="lazy">', external=True)
        if photo.get('caption'):
            result += f'<figcaption>{e(photo["caption"])}</figcaption>'
        result += '</figure>'
    return result + '</div>'


PAGES = [
    ('index', 'About me', home),
    ('research', SITE['research_label'], research),
    ('team', 'Team', team),
    ('teaching', 'Teaching', teaching),
    ('softwares', 'Software', softwares),
    ('talks', 'Talks', talks),
    ('service', 'Service', service),
    ('cv', 'CV', cv),
    ('moments', 'Moments', moments),
]


def visitor_map_html():
    config = DATA.get('visitor_map', {})
    if not config.get('enabled', False):
        return ''
    return (f'<section class="visitor-map" aria-labelledby="visitor-map-title" data-site-url="{e(config.get("site_url", ""))}" data-widget-id="{e(config.get("widget_id", ""))}">'
            '<h2 id="visitor-map-title">Visitors around the world</h2>'
            '<div class="visitor-map-frame"><img class="visitor-map-placeholder" src="assets/images/visitor-world.svg" alt="World map; visitor tracking is not yet enabled" width="720" height="360">'
            '<div id="visitor-map-widget"></div></div>'
            '<p class="visitor-map-status" role="status">Visitor tracking is not yet enabled.</p>'
            '<noscript><p>JavaScript is required to display live visitor locations.</p></noscript></section>')


def build():
    profile_links = f'<li class="location-item"><span class="location">{icon("pin")}{e(PROFILE["location"])}</span></li>'
    for key, label, symbol in [('email', 'Email', 'mail'), ('scholar', 'Google Scholar', 'scholar'), ('linkedin', 'LinkedIn', 'linkedin')]:
        url = PROFILE[key]
        if key == 'email':
            url = 'mailto:' + url
        profile_links += '<li>' + link(url, icon(symbol) + e(label), external=key in ('scholar', 'linkedin')) + '</li>'
    profile_links += '<li>' + link('cv.html', icon('file') + 'Curriculum Vitae') + '</li>'
    if PROFILE['portrait']:
        portrait = f'<img class="portrait" src="{e(PROFILE["portrait"])}" alt="{e(PROFILE["name"])}" width="178" height="178">'
    else:
        portrait = f'<span class="portrait portrait-placeholder" role="img" aria-label="{e(PROFILE["name"])} initials">{e(PROFILE["initials"])}</span>'
    for slug, title, renderer in PAGES + [('photography', 'My Photography Portfolio', photography)]:
        nav = ''.join(f'<a href="{p}.html"' + (' aria-current="page"' if p == slug or (slug == 'photography' and p == 'moments') else '') + f'>{e(t)}</a>' for p, t, _ in PAGES[1:])
        result = BASE.substitute(
            title=e(title), name=e(PROFILE['name']), description=e(SITE['description']),
            home_current='aria-current="page"' if slug == 'index' else '',
            navigation=nav, portrait=portrait, role=e(PROFILE['role']),
            department=e(PROFILE['department']), institution=e(PROFILE['institution']),
            profile_links=profile_links, content=renderer(), email=e(PROFILE['email']),
            year=SITE['year'], updated=e(SITE['updated']))
        (ROOT / f'{slug}.html').write_text(result, encoding='utf-8')
    print(f'Built {len(PAGES) + 1} static pages in {ROOT}')


if __name__ == '__main__':
    build()
