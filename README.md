# End-to-End AI Generated Podcast

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Spotify](https://img.shields.io/badge/Listen-Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white)](https://open.spotify.com/episode/1MpizVeG2DQrifcPd1M3dm?trackId=1MpizVeG2DQrifcPd1M3dm)
[![LLM](https://img.shields.io/badge/LLM-GPT--4%20%7C%20Llama-412991)](https://platform.openai.com/)
[![TTS](https://img.shields.io/badge/TTS-Voice%20Cloning-6366F1)](https://github.com/BPrakhar30/End-to-End_AI-Generated_Podcast)

Automated pipeline that scrapes news, generates podcast scripts with LLMs, and synthesizes expressive speech - producing daily AI-generated podcast episodes.

**Sample episode:** [Haunted Whispers in The Forbidden City on Spotify](https://open.spotify.com/episode/1MpizVeG2DQrifcPd1M3dm?trackId=1MpizVeG2DQrifcPd1M3dm)

## Features

- **Multi-source news** - DuckDuckGo web search in the LLM pipeline for diverse sourcing
- **Expressive TTS** - Open-source text-to-speech with emotion and intonation
- **Unlimited duration** - No hard cap on episode length
- **Daily automation** - Scheduled episode generation

## Pipeline

```
News scrape -> Summarize -> Web search enrich -> Script generation -> TTS -> MP3
```

| Module | Role |
|--------|------|
| `scrapping.py` | Scrape news from base sources |
| `summary.py` | Compress content to reduce token usage |
| `web_search.py` | DuckDuckGo aggregation for multi-source news |
| `script.py` | Generate podcast script from scraped content |
| `tts.py` | Convert script to expressive MP3 audio |

## Getting started

```bash
pip install -r requirements.txt
```

1. Create `secret_token.txt` with your OpenAI API key
2. Update the date and file paths in `main.py`
3. Run:

```bash
python main.py
```

## Roadmap

- Voice cloning for realistic guest voices
- Automated upload to Spotify

## Author

Built during CMU research - part of a broader generative media pipeline (Llama 3 + GPT-4 + TTS).
