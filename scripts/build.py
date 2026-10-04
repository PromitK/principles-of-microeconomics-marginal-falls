#!/usr/bin/env python3
"""Generate the static course site and README from the canonical content."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
COURSE = json.loads((ROOT / 'content/course.json').read_text())
MATERIALS = json.loads((ROOT / 'content/materials.json').read_text())
FILES = {int(f['name'].split('_')[1]): f for f in MATERIALS if f['name'].startswith('Module_')}
GAMES = {g['id']: g for g in COURSE['games']}
ACTS = {a['id']: a for a in COURSE['acts']}

def esc(value):
    return html.escape(str(value), quote=True)

def ext(url, label, cls='text-link'):
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{label}</a>'

def shell(title, description, content, prefix='', home=False):
    base = prefix + 'index.html'
    links = [('The story', 'story'), ('Course modules', 'modules'), ('For instructors', 'instructors')]
    nav = ''.join(f'<a href="{base}#{anchor}">{label}</a>' for label, anchor in links)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#193e35"><link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">
<link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/site.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner"><a class="brand" href="{base}" aria-label="Marginal Falls course home"><span class="brand-mark" aria-hidden="true">MF</span><span>Marginal Falls<span class="brand-sub">A course in microeconomics</span></span></a><nav aria-label="Main navigation">{nav}</nav></div></header>
<main id="main">{content}</main>
<footer class="site-footer"><div class="container footer-inner"><div><strong>Principles of Microeconomics<br>in Marginal Falls</strong><p>Course materials by Promit K. Chaudhuri<br>Department of Economics · Virginia Tech</p></div><div><p>Marginal Falls games: Promit K. Chaudhuri &amp; Michael Wagnon<br>Co-creators and equal contributors</p><div class="footer-links">{ext('https://marginalfalls.com/', 'Visit Marginal Falls')}{ext('https://promitkchaudhuri.com/', 'Instructor website')}</div><p class="small">Original authors retain their rights. No open reuse license is supplied.</p></div></div></footer>
</body></html>'''

def game_card(g, prefix='', compact=False):
    modules = ', '.join(f'<a href="{prefix}modules/module-{i:02d}.html">Module {i:02d}</a>' for i in g['modules'])
    return f'''<article class="game-card"><span class="eyebrow">{esc(g['concept'])}</span><h3>{esc(g['title'])}</h3><p>{esc(g['description'])}</p><div class="game-meta">{modules}</div>{ext(g['url'], 'Open activity', 'button button-outline')}</article>'''

def module_row(m):
    f = FILES[m['id']]
    game_word = f"{len(m['games'])} {'activity' if len(m['games']) == 1 else 'activities'}" if m['games'] else 'Lecture module'
    search = ' '.join([m['title'], m['topic'], m['story']] + m['concepts'])
    return f'''<article class="module-row" data-module data-search="{esc(search.lower())}" data-has-games="{'true' if m['games'] else 'false'}">
<span class="module-number">{m['id']:02d}</span><div class="module-copy"><h4><a href="modules/module-{m['id']:02d}.html">{esc(m['title'])}</a></h4><p>{esc(m['topic'])}</p><span class="module-detail">{f['pages']} slides · {game_word}</span></div><div class="module-actions"><a class="module-open" href="modules/module-{m['id']:02d}.html">Explore</a><a class="slides-link" href="materials/{f['name']}" target="_blank" rel="noopener noreferrer" aria-label="Open slides for Module {m['id']}">Slides PDF</a></div></article>'''

def build_home():
    acts = []
    for a in COURSE['acts']:
        rows = ''.join(module_row(m) for m in COURSE['modules'] if m['act'] == a['id'])
        acts.append(f'''<section class="act-block" data-act="{a['id']}" id="act-{a['id']}" aria-labelledby="act-title-{a['id']}"><div class="act-intro"><span class="act-roman">{a['roman']}</span><div><span class="eyebrow">Act {a['roman']}</span><h3 id="act-title-{a['id']}">{esc(a['title'])}</h3><p>{esc(a['question'])}</p></div></div><div class="module-list">{rows}</div></section>''')
    route = ''.join(f'<a href="#act-{a["id"]}" class="route-stop"><span>{a["roman"]}</span><strong>{esc(a["title"])}</strong></a>' for a in COURSE['acts'])
    filters = ''.join(f'<button class="filter-button" type="button" data-filter="{a["id"]}" aria-pressed="false">Act {a["roman"]}</button>' for a in COURSE['acts'])
    content = f'''
<section class="hero container"><div class="hero-copy"><p class="eyebrow">ECON 2005 · Principles of Microeconomics</p><h1>Economics comes<br>to <em>Marginal Falls.</em></h1><p class="hero-description">A town to build. Citizens to understand. Markets to bring to life. Learn microeconomics through the choices of one fictional community.</p><p class="author">A course by <strong>Promit K. Chaudhuri</strong><br>Department of Economics · Virginia Tech</p><div class="hero-actions"><a class="button" href="#modules">Explore the course</a></div></div><div class="hero-art"><img src="assets/town.svg" alt="An illustration of a riverside town with a bakery, market stalls, homes, trees, and a bridge"><span class="art-caption">WELCOME TO MARGINAL FALLS<br><span>Every choice has a story.</span></span></div></section>
<div class="stats-band"><div class="container stats-inner"><span><strong>One town</strong> shared across the course</span><span><strong>Five acts</strong> from choices to competition</span><span><strong>16 modules</strong> with complete slide decks</span><span><strong>13 activities</strong> connected to the story</span></div></div>
<section class="section container story-section" id="story"><div><p class="eyebrow">The idea behind the course</p><h2>A familiar place.<br>A new way to think.</h2></div><div class="story-text"><p>Marginal Falls is the setting for the course, with its citizens, bakery, port, markets, and businesses returning as the economics develops. A decision about riverfront land introduces scarcity. An investigation introduces budgets. A bakery order introduces production and costs.</p><p>Buyers and sellers first make their own plans. Then they meet in the Town Square, where prices coordinate their choices. The final act changes the competitive setting and asks how the same economic logic works under different market structures.</p><p class="story-note">The course builds the people behind the curves before bringing the curves together.</p></div></section>
<section class="route-band"><div class="container"><p class="eyebrow">Your journey through the town</p><div class="route-grid">{route}</div></div></section>
<section class="section container" id="modules"><div class="section-heading"><div><p class="eyebrow">The complete course</p><h2>Five acts. Sixteen modules.</h2><p>Follow the story in order, or find the topic you need.</p></div></div>
<div class="course-controls" id="course-controls" hidden><label class="search-field"><span>Find a module</span><input id="module-search" type="search" placeholder="Try demand, bakery, or game theory…" autocomplete="off" aria-controls="module-catalog"></label><div class="filter-set" role="group" aria-label="Filter modules by act"><button class="filter-button active" type="button" data-filter="all" aria-pressed="true">All acts</button>{filters}</div><label class="activity-check"><input id="games-only" type="checkbox"> Modules with activities</label><p id="result-count" class="small" aria-live="polite">16 modules</p></div>
<div id="module-catalog">{''.join(acts)}</div><p id="no-results" class="empty-state" hidden>No modules match this search. <button type="button" id="reset-filters">Clear filters</button></p>
</section>
<section class="section container instructor-section" id="instructors"><div><p class="eyebrow">Bring Marginal Falls to your classroom</p><h2>For instructors</h2><p>The slides provide the economic framework. The activities let a class make decisions and discuss the resulting outcomes.</p><div class="instructor-actions">{ext('https://marginalfalls.com/instructors/', 'Read the instructor manual', 'button')}{ext('https://marginalfalls.com/contact/', 'Request game access', 'button button-outline')}</div></div><ol class="teaching-steps"><li><span>01</span><div><h3>Set up the decision</h3><p>Introduce the relevant town problem and let students explain what they expect.</p></div></li><li><span>02</span><div><h3>Run the activity</h3><p>Open a classroom room, share its code, and guide the class through its decisions.</p></div></li><li><span>03</span><div><h3>Return to the economics</h3><p>Use the class outcome to discuss incentives, constraints, and the relevant model.</p></div></li></ol></section>
<section class="resources-section"><div class="container resources-inner"><div><p class="eyebrow">Course materials</p><h2>Lecture slides</h2><p>Open a module to read its slides and find the activities used in class.</p></div><div class="resource-actions"><a class="button button-outline" href="#modules">Find a module</a></div></div></section>'''
    (OUT / 'index.html').write_text(shell(COURSE['title'], 'A story-based Principles of Microeconomics course set in Marginal Falls, with 16 slide decks and 13 classroom activities.', content, home=True))

def build_modules():
    destination = OUT / 'modules'
    destination.mkdir(exist_ok=True)
    for m in COURSE['modules']:
        a = ACTS[m['act']]
        f = FILES[m['id']]
        points = ''.join(f'<li>{esc(c)}</li>' for c in m['concepts'])
        if m['games']:
            activities = '<div class="games-grid module-games">' + ''.join(game_card(GAMES[g], '../') for g in m['games']) + '</div>'
        else:
            activities = '<p class="lecture-note">This module is taught through its slide deck and classroom discussion. No dedicated live activity is used for this topic.</p>'
        prev = f'<a href="module-{m["id"] - 1:02d}.html">← Previous module</a>' if m['id'] > 1 else '<a href="../index.html#modules">← Course overview</a>'
        nextlink = f'<a href="module-{m["id"] + 1:02d}.html">Next module →</a>' if m['id'] < 16 else '<a href="../index.html#modules">Back to the course →</a>'
        content = f'''<div class="container module-page"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Course home</a><span aria-hidden="true">/</span><a href="../index.html#act-{a['id']}">Act {a['roman']}</a><span aria-hidden="true">/</span><span>Module {m['id']:02d}</span></nav><header class="module-hero"><p class="eyebrow">Act {a['roman']} · {esc(a['title'])} · Module {m['id']:02d}</p><h1>{esc(m['title'])}</h1><p class="module-topic">{esc(m['topic'])}</p><div class="hero-actions"><a class="button" href="../materials/{f['name']}" target="_blank" rel="noopener noreferrer">Open lecture slides</a>{ext(f['url'], 'Google Drive copy', 'button button-outline')}</div><p class="small">{f['pages']} slides · Hubbard &amp; O'Brien, chapter {esc(m['chapter'])}. Drive access may be required.</p></header><div class="module-tabs" role="tablist" aria-label="Module content" hidden><button type="button" id="tab-overview" role="tab" aria-selected="true" aria-controls="panel-overview" tabindex="0">Overview</button><button type="button" id="tab-activity" role="tab" aria-selected="false" aria-controls="panel-activity" tabindex="-1">Activity</button></div><div class="module-body" id="panel-overview" role="tabpanel" aria-labelledby="tab-overview" tabindex="0"><section><p class="eyebrow">The story</p><h2>Where this fits in Marginal Falls</h2><p class="module-story">{esc(m['story'])}</p><div class="discussion-box"><p class="eyebrow">A question to take into class</p><p>{esc(m['question'])}</p></div></section><aside class="concept-panel"><p class="eyebrow">The economic ideas</p><h2>Concepts to follow</h2><ul>{points}</ul><p class="small">Read the slide deck for the definitions, examples, and diagrams.</p></aside></div><section class="module-activities" id="panel-activity" role="tabpanel" aria-labelledby="tab-activity" tabindex="0"><p class="eyebrow">From the slides to the classroom</p><h2>Activities used in this module</h2>{activities}<p class="small game-access">Activities open at marginalfalls.com. Students join using the room code supplied by their instructor.</p></section><nav class="module-pagination" aria-label="Module navigation">{prev}<a href="../index.html#modules">All modules</a>{nextlink}</nav></div>'''
        (destination / f"module-{m['id']:02d}.html").write_text(shell(f"Module {m['id']:02d}: {m['title']} | Marginal Falls", m['topic'], content, prefix='../'))

def build_readme():
    lines = [f"# {COURSE['title']}", '', '**One town. Five acts. Sixteen modules.**', '',
             'A story-based Principles of Microeconomics course by **Promit K. Chaudhuri**, Department of Economics, Virginia Tech (ECON 2005).', '',
             '## Why Marginal Falls?', '',
             "Marginal Falls is a fictional town that develops alongside the course. Its citizens make choices, its bakery produces goods, its port opens to trade, and its businesses compete. Returning to the same setting connects ideas that can otherwise feel like separate textbook chapters.", '',
             "The sequence builds buyers and sellers separately before bringing them together in the Town Square. It then asks when markets work well, when they fail, how labor is valued, and how outcomes change across market structures.", '',
             '## Start here', '',
             '- **Course website:** the complete static site is in [`docs/`](docs/index.html), ready for GitHub Pages.',
             '- **Classroom activities:** [Marginal Falls](https://marginalfalls.com/)',
             '- **Run the activities:** [instructor manual](https://marginalfalls.com/instructors/) · [request instructor access](https://marginalfalls.com/contact/)', '',
             'The bundled PDFs are the primary slide links. The newly uploaded Drive copies currently require access; their public sharing has not been enabled.', '',
             '## The course in five acts', '',
             '| Act | The story | The economics |', '| --- | --- | --- |']
    for a in COURSE['acts']:
        lines.append(f"| {a['roman']}: {a['title']} | {a['question']} | {a['description']} |")
    lines += ['', '## Modules and materials', '',
              'Module order follows the lecture slide decks. Chapter references use Hubbard & O’Brien.', '',
              '| Module | Setting | Topic | Chapter | Slides | Activities |', '| --- | --- | --- | --- | --- | --- |']
    for m in COURSE['modules']:
        f = FILES[m['id']]
        activities = '; '.join(f"[{GAMES[g]['title']}]({GAMES[g]['url']})" for g in m['games']) or '—'
        lines.append(f"| {m['id']:02d} | {m['title']} | {m['topic']} | {m['chapter']} | [PDF](docs/materials/{f['name']}) · [Drive]({f['url']}) | {activities} |")
    lines += ['', '### Source differences', '',
              'The site follows the lecture deck numbering: Town Square (9), Fair Play (10), Town Crisis (11), and Hiring Hall (12), all in Act IV.', '',
              'Module 8 is named Profit and Sensitivity in its filename and Seller Sensitivity on its title slide. Its topic is price elasticity of supply.', '',
              'The original PDFs still contain some links to econgames.promitkchaudhuri.com. The course site uses corresponding marginalfalls.com activity pages, which were checked on 2 October 2026. The Port Ledger Game is linked from Module 2 even though it is not displayed in the current homepage directory.', '',
              '## Using the course', '',
              'Students can read the relevant slides, join an activity using the room code supplied by their instructor, and return to the economic questions after the class outcome is displayed.', '',
              'Instructors should request game access before class and follow the live instructor manual. A useful sequence is to introduce the decision, run the activity, invite students to explain their choices, and connect the outcome to the economic framework in the slides.', '',
              'See [the course guide](guides/COURSE_GUIDE.md) for the teaching sequence and [publishing instructions](guides/PUBLISHING.md) for GitHub Pages.', '',
              '## Repository layout', '',
              '- `content/course.json`: course narrative, module descriptions, and activity mapping.',
              '- `content/materials.json`: verified PDF filenames, Drive links, page counts, and SHA-256 hashes.',
              '- `docs/`: generated website, module pages, assets, and the complete PDF collection.',
              '- `scripts/build.py`: dependency-free site and README generator.',
              '- `.github/workflows/pages.yml`: GitHub Pages publishing workflow.',
              '- `guides/`: course and publishing documentation.', '',
              '## Preview and update', '', 'Requires Python 3.9 or newer. No package installation or frontend build system is needed.', '',
              '```bash', 'python3 scripts/build.py', 'python3 -m http.server 8000 --directory docs', '```', '',
              'Open `http://localhost:8000`. To change descriptions or activity links, edit `content/course.json` and rebuild. To replace PDFs, keep the stable filenames under `docs/materials/` and update the material metadata. To preserve existing Drive links, replace the corresponding Drive file rather than uploading a new copy.', '',
              '## Publish with GitHub Pages', '',
              'Create a public repository named `principles-of-microeconomics-marginal-falls`, upload this folder’s contents including `.github/workflows/pages.yml`, and set **Settings → Pages → Source → GitHub Actions**. The included workflow publishes `docs/` on pushes to `main` or through a manual workflow run. See [the publishing guide](guides/PUBLISHING.md).', '',
              '## Credits and rights', '',
              '**Course and lecture materials:** Promit K. Chaudhuri.', '',
              '**Marginal Falls games and project:** Promit K. Chaudhuri and Michael Wagnon, co-creators and equal contributors, as credited on marginalfalls.com.', '',
              'The games remain hosted at marginalfalls.com; this repository links to them and does not contain the game source code or classroom-session data. Original authors retain their rights. No open reuse license has been added.', '']
    (ROOT / 'README.md').write_text('\n'.join(lines))

if __name__ == '__main__':
    # Keep private planning materials out of the public output.
    (OUT / 'materials/ECON_2005_Syllabus.pdf').unlink(missing_ok=True)
    build_home()
    build_modules()
    build_readme()
    print('Built course home, 16 module pages, and README.')
