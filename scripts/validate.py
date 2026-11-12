#!/usr/bin/env python3
"""Offline integrity checks for curated patterns, source review provenance, and upstream backlog."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
ERRORS = []
REQUIRED = {'id', 'title', 'domain', 'priority', 'projects', 'signals', 'approach', 'avoid', 'verification', 'source_urls', 'source_review', 'related'}
STATUSES = {'reviewed', 'index_only', 'pending_primary_review'}


def error(message):
    ERRORS.append(message)


def load(path):
    try:
        return json.loads((ROOT / path).read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        error(f'{path}: {exc}')
        return {}


def check():
    catalog = load('data/patterns.json')
    sources_doc = load('data/sources.json')
    backlog = load('data/upstream-index.json')
    if catalog.get('schema_version') != 1 or sources_doc.get('schema_version') != 1 or backlog.get('schema_version') != 1:
        error('schema_version must be 1 for all JSON files')
    cards = catalog.get('cards', [])
    sources = sources_doc.get('sources', [])
    entries = backlog.get('items', [])
    if not isinstance(cards, list) or not isinstance(sources, list) or not isinstance(entries, list):
        error('cards/sources/items must be arrays')
        return 0, 0
    ids = set()
    for card in cards:
        if not isinstance(card, dict):
            error('non-object card')
            continue
        pid = card.get('id', '')
        missing = REQUIRED - card.keys()
        if missing:
            error(f'{pid}: missing {sorted(missing)}')
        if not isinstance(pid, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', pid):
            error(f'{pid}: invalid id')
        if pid in ids:
            error(f'{pid}: duplicate id')
        ids.add(pid)
        if card.get('priority') not in {'P0','P1','P2','P3'}:
            error(f'{pid}: invalid priority')
        if card.get('source_review') not in STATUSES:
            error(f'{pid}: invalid source_review')
        for key in ['title','domain','signals','approach','avoid','verification']:
            if not isinstance(card.get(key), str) or not card[key].strip():
                error(f'{pid}: empty {key}')
        for key in ['projects','source_urls','related']:
            if not isinstance(card.get(key), list):
                error(f'{pid}: {key} must be an array')
        if not card.get('source_urls'):
            error(f'{pid}: needs a source URL')
    by_url = {}
    for src in sources:
        if not isinstance(src, dict):
            error('non-object source')
            continue
        url=src.get('url','')
        if url in by_url:
            error(f'duplicate primary source URL: {url}')
        by_url[url] = src
        if not isinstance(url,str) or urlsplit(url).scheme != 'https':
            error(f'primary source URL must be HTTPS: {url}')
        if src.get('status') not in STATUSES:
            error(f'invalid source review status: {url}')
        if not isinstance(src.get('patterns'),list) or not src['patterns']:
            error(f'{url}: source pattern IDs missing')
        else:
            for pid in src['patterns']:
                if pid not in ids: error(f'{url}: unknown pattern {pid}')
    # Each card must refer to recorded sources and reverse relationships must match.
    for card in cards:
        if not isinstance(card,dict):continue
        pid=card.get('id','?')
        for rel in card.get('related',[]):
            if rel not in ids:error(f'{pid}: unknown related {rel}')
        referenced=[]
        for url in card.get('source_urls',[]):
            source=by_url.get(url)
            if source is None:
                error(f'{pid}: missing source {url}')
            else:
                referenced.append(source['status'])
                if pid not in source.get('patterns',[]):error(f'{pid}: missing reverse source relation {url}')
        if referenced:
            # Card review status reflects most conservative available source review, unless
            # a reviewed source independently substantiates the pattern.
            if card.get('source_review') == 'reviewed' and 'reviewed' not in referenced:
                error(f'{pid}: reviewed without reviewed primary source')
            if card.get('source_review') == 'index_only' and 'index_only' not in referenced:
                error(f'{pid}: index_only without index-only source')
            if card.get('source_review') == 'pending_primary_review' and 'pending_primary_review' not in referenced:
                error(f'{pid}: pending without pending source')
    for url,src in by_url.items():
        for pid in src.get('patterns',[]):
            card=next((c for c in cards if c.get('id')==pid),{})
            if url not in card.get('source_urls',[]):error(f'{url}: missing forward card relation {pid}')
    seen_urls=set(); occurrence_count=0
    for item in entries:
        if not isinstance(item,dict):
            error('non-object upstream item');continue
        url=item.get('url','')
        if not isinstance(url,str) or urlsplit(url).scheme not in {'http','https'}:
            error(f'invalid upstream URL: {url}')
        if url in seen_urls:error(f'duplicate upstream index URL: {url}')
        seen_urls.add(url)
        if item.get('review_status') != 'not_reviewed_from_index':
            error(f'upstream index must not claim review: {url}')
        occur=item.get('occurrences',[])
        if not isinstance(occur,list) or not occur:
            error(f'upstream index missing occurrences: {url}')
        else: occurrence_count+=len(occur)
    if backlog.get('unique_urls') != len(entries) or backlog.get('link_occurrences') != occurrence_count:
        error('upstream index counts mismatch')
    # Optional project-specific decision cases; each must link existing pattern IDs.
    cases_file = ROOT / 'data/staya-scenarios.json'
    if cases_file.exists():
        cases = load('data/staya-scenarios.json')
        if cases.get('schema_version') != 1:
            error('STAYA scenario schema_version must be 1')
        if cases.get('version') != catalog.get('version'):
            error('STAYA scenarios version does not match patterns version')
        seen_case_ids = set()
        for case in cases.get('items', []):
            case_id = case.get('id', '')
            if case_id in seen_case_ids or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', case_id):
                error(f'invalid or duplicate scenario id: {case_id}')
            seen_case_ids.add(case_id)
            if case.get('decision_status') != 'proposed':
                error(f'{case_id}: do not mark unexecuted QA as successful')
            if not case.get('must_consider') or not case.get('acceptance'):
                error(f'{case_id}: scenario needs patterns and acceptance conditions')
            for pid in case.get('must_consider', []):
                if pid not in ids: error(f'{case_id}: unknown pattern {pid}')
    # General-purpose DevOps/update scenarios: proposed only, never presumed executed.
    qa_file = ROOT / 'data/devops-scenarios.json'
    if qa_file.exists():
        qa = load('data/devops-scenarios.json')
        if qa.get('schema_version') != 1 or qa.get('version') != catalog.get('version'):
            error('devops scenarios schema/version mismatch')
        seen_devops = set()
        for case in qa.get('items', []):
            case_id = case.get('id', '')
            if not isinstance(case_id, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', case_id) or case_id in seen_devops:
                error(f'invalid or duplicate devops scenario id: {case_id}')
            seen_devops.add(case_id)
            if case.get('decision_status') != 'proposed':
                error(f'{case_id}: scenario must remain proposed until tested in project')
            if not case.get('must_consider') or not case.get('acceptance'):
                error(f'{case_id}: missing pattern links or acceptance')
            for pid in case.get('must_consider', []):
                if pid not in ids: error(f'{case_id}: unknown pattern {pid}')
    # Proposed performance case links and version must follow catalog.
    perf_file = ROOT / 'data/performance-scenarios.json'
    if perf_file.exists():
        perf = load('data/performance-scenarios.json')
        if perf.get('schema_version') != 1 or perf.get('version') != catalog.get('version'):
            error('performance scenario schema/version mismatch')
        perf_ids = set()
        for case in perf.get('items', []):
            cid = case.get('id', '')
            if not isinstance(cid, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', cid) or cid in perf_ids:
                error(f'invalid or duplicate perf scenario id: {cid}')
            perf_ids.add(cid)
            if case.get('decision_status') != 'proposed': error(f'{cid}: proposed only, no physical proof')
            if not case.get('must_consider') or not case.get('acceptance'): error(f'{cid}: missing links/acceptance')
            for pid in case.get('must_consider', []):
                if pid not in ids: error(f'{cid}: unknown pattern {pid}')
    # Keep proposed QA cases referentially correct and version-aligned.
    qa_file = ROOT / 'data/qa-scenarios.json'
    if qa_file.exists():
        qa = load('data/qa-scenarios.json')
        if qa.get('schema_version') != 1 or qa.get('version') != catalog.get('version'):
            error('qa scenarios schema/version mismatch')
        qa_ids = set()
        for case in qa.get('items', []):
            cid = case.get('id', '')
            if not isinstance(cid, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', cid) or cid in qa_ids:
                error(f'invalid or duplicate QA scenario id: {cid}')
            qa_ids.add(cid)
            if case.get('decision_status') != 'proposed': error(f'{cid}: QA must remain proposed')
            if not case.get('must_consider') or not case.get('acceptance'): error(f'{cid}: missing QA links/acceptance')
            for pid in case.get('must_consider', []):
                if pid not in ids: error(f'{cid}: unknown pattern {pid}')
    # Proposed WPF accessibility QA cases must match current catalog.
    a11y_path = ROOT / 'data/wpf-accessibility-scenarios.json'
    if a11y_path.exists():
        doc = load('data/wpf-accessibility-scenarios.json')
        if doc.get('schema_version') != 1 or doc.get('version') != catalog.get('version'):
            error('wpf-accessibility scenarios schema/version mismatch')
        seen_a11y = set()
        for case in doc.get('items', []):
            cid = case.get('id', '')
            if not isinstance(cid, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', cid) or cid in seen_a11y:
                error(f'invalid or duplicate WPF scenario id: {cid}')
            seen_a11y.add(cid)
            if case.get('decision_status') != 'proposed': error(f'{cid}: only proposed QA')
            if not case.get('must_consider') or not case.get('acceptance'): error(f'{cid}: empty QA links/acceptance')
            for pid in case.get('must_consider', []):
                if pid not in ids: error(f'{cid}: unknown pattern {pid}')
    return len(cards),len(by_url)


if __name__ == '__main__':
    cards,sources=check()
    print(f'cards={cards} source_urls={sources} errors={len(ERRORS)}')
    for problem in ERRORS:print('ERROR:', problem)
    sys.exit(bool(ERRORS))
