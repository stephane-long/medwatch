# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Medwatch** is an AI-powered medical news surveillance tool designed for journalists to monitor healthcare, medical research, and professional health topics. It aggregates relevant sources and generates structured reports with automatic tier classification (authorities > academic > accredited media > other).

The project is in early stages with a minimal initial implementation focusing on NewsAPI integration.

## Quick Start

### Setup
1. **Install dependencies**: `pip install requests`
2. **Configure API key**: Replace `"VOTRE_CLE_NEWS_API"` in `scripts/news_fetcher.py.py` with a valid NewsAPI key (free tier available at newsapi.org)
3. **Run a search**: `python3 scripts/news_fetcher.py "query text" [days]`
   - Example: `python3 scripts/news_fetcher.py "maladie de Crohn" 7`
   - Returns JSON array of articles from the past N days

### As a Claude Skill
The tool can be invoked as a Claude Skill through SKILL.md. Claude will:
1. Parse user intent to extract search query and timeframe
2. Execute the fetcher script
3. Format results with summaries for the user

## Architecture

### Current Structure
```
medwatch/
├── CLAUDE.md              # This file
├── SKILL.md               # Claude Skill configuration
└── scripts/
    └── news_fetcher.py.py # NewsAPI integration (main entry point)
```

### How It Works Today
- **Single data source**: NewsAPI (French & international health news)
- **Basic output**: Raw JSON from API
- **No processing**: Articles returned as-is without filtering or classification

### Planned Architecture (Phase 2)
The system should evolve to support:
- **Multiple data sources**: Tavily API + NewsAPI + PubMed RSS + Tier 1 scraping (HAS, Ansm, Santé Publique France)
- **Source classification**: Automatic Tier assignment (1=Authorities, 2=Academic, 3=Media, 4=Other)
- **Content extraction**: Fetch full articles and extract 300-500 character summaries
- **Structured output**: JSON + Markdown reports with organized sources by tier
- **Full workflow**: orchestrator.py → search → extract → synthesize → report

## Key Implementation Notes

### SKILL.md Contract
The SKILL.md file defines:
- Command format: `python3 news_fetcher.py "{query}" {days}`
- Expected output: JSON array of articles
- Claude's responsibility: query preprocessing, output formatting, presentation

**Important**: Keep news_fetcher.py output as valid JSON (array or error object) so Claude can reliably parse results.

### API Key Management
- NewsAPI key must be inserted in `scripts/news_fetcher.py.py` (currently hardcoded)
- Future: Move to `.env` file when expanding to multiple APIs
- Free tier: 100 requests/day (sufficient for development/testing)

### Known Issues
1. **Filename typo**: `news_fetcher.py.py` should be renamed to `news_fetcher.py` (minor issue, doesn't affect functionality)
2. **No filtering**: Raw API results include irrelevant articles—future versions need relevance filtering
3. **French-only bias**: Current search is `language: "fr"` only—consider multilingual support for international medical sources

## Next Steps (Priority Order)

1. **Expand data sources**:
   - Add Tavily API for web search (news + sources)
   - Integrate PubMed RSS for academic papers
   - Add direct scraping of Tier 1 sources (HAS, Ansm)
   - Implement deduplication across sources

2. **Add content processing**:
   - Fetch full article text from URLs
   - Extract key metadata (date, author, domain)
   - Generate 300-500 character summaries
   - Classify sources by tier

3. **Build the orchestrator**:
   - Create `src/orchestrator.py` to coordinate workflow
   - Implement `src/synthesizer.py` for tier ranking and report generation
   - Add JSON and Markdown output templates

4. **Improve reliability**:
   - Add error handling for API failures
   - Implement request retries with backoff
   - Cache results locally (SQLite or JSON)
   - Add comprehensive test suite

5. **Optimize UX**:
   - Better Claude Skill output formatting
   - Support for saved searches / alerts
   - Performance profiling (target: <20s per report)

## Development Practices

- **Language**: Python 3.9+
- **Dependencies**: Keep minimal (requests + standard library for now)
- **Testing**: Unit tests in `tests/` directory (use pytest)
- **Code style**: Follow PEP 8
- **API keys**: Never commit API keys; use environment variables in production

## Reference Documents

- **SKILL.md**: Claude Skill configuration, command format, output expectations
- **newsapi.org**: API documentation and free key signup
