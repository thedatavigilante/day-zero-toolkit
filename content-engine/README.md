# Content Engine
### CLI Content Generator — The Data Vigilante

Built for [@neurospicydatawhiz](https://www.tiktok.com/@neurospicydatawhiz) · Sierra Napier · 2026

Generates on-brand social media and GitHub content across TikTok, LinkedIn, Twitter/X, and GitHub — tactical, direct, no fluff.

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your API key
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY

# 3. Run it
python generate.py --platform tiktok --topic "DOGE layoffs and your FEHB rights"
```

---

## Usage

```bash
python generate.py --platform <platform> --topic "<topic>"
```

| Flag | Required | Description |
|------|----------|-------------|
| `--platform` / `-p` | Yes | `tiktok`, `linkedin`, `twitter`, `github` |
| `--topic` / `-t` | Yes | What the content is about |
| `--format` / `-f` | No | Sub-format: `POST` or `CAROUSEL` (linkedin), `README_SECTION` or `RELEASE_NOTES` (github) |
| `--model` / `-m` | No | Claude model (default: `claude-sonnet-4-6`) |
| `--output` / `-o` | No | Custom output filepath |
| `--no-save` | No | Print only, don't save to file |

---

## Examples

```bash
# TikTok script about FEHB rights
python generate.py -p tiktok -t "DOGE layoffs and your FEHB rights"

# LinkedIn post about the Black Box Key
python generate.py -p linkedin -t "Why the Black Box Key matters" -f POST

# LinkedIn carousel
python generate.py -p linkedin -t "3 programs you can stack after a federal layoff" -f CAROUSEL

# Twitter thread
python generate.py -p twitter -t "Vocational rehab stacking strategy"

# GitHub release notes
python generate.py -p github -t "Day Zero Toolkit v1.1" -f RELEASE_NOTES

# GitHub README section
python generate.py -p github -t "Federal Worker Benefits Guide" -f README_SECTION
```

Output is saved to `output/` automatically. Pass `--no-save` to print only.

---

## How It Works

Each platform has a dedicated system prompt in `prompts/` that enforces format and tone.
All prompts are grounded in the base persona (`prompts/base_persona.txt`) — tactical, real, neurodivergent-friendly, anti-toxic-positivity.

The model is Claude (`claude-sonnet-4-6`) via the Anthropic SDK.

---

## Project Structure

```
content-engine/
├── generate.py               # CLI entry point
├── requirements.txt
├── .env.example
├── prompts/
│   ├── base_persona.txt      # Brand voice anchor
│   ├── tiktok.txt
│   ├── linkedin.txt
│   ├── twitter.txt
│   └── github.txt
├── templates/
│   ├── tiktok_hook.md        # Hook formula reference
│   └── linkedin_carousel.md  # Carousel structure reference
└── output/                   # Generated content (gitignored)
```

---

*Built with rage, research, and real receipts. — Sierra Napier, The Robin Hood of AI*
