# End-to-End AI Generated Podcast

This repository contains the codebase for creating AI-generated news podcasts, available at [DreamPodcasts](https://dreampodcasts.com/). The project explores the possibilities of content creation using Large Language Models (LLMs), extending their capabilities beyond typical output limits. This baseline code can be adapted to produce various categories of podcasts, such as horror, daily news, children's content, travel explorations, and more.

## Features

1. **Multi-Source News Integration**: Incorporates DuckDuckGo web search within the LLM pipeline to reduce bias and ensure diverse news sourcing.
2. **Advanced Text-to-Speech (TTS)**: Utilizes an open-source TTS model capable of conveying expressions and emotions.
3. **Unlimited Podcast Duration**: No restrictions on the length of generated podcast episodes.
4. **Automated Episode Generation**: Episodes are generated automatically at a specified time each day.

## Getting Started

1. **Install Dependencies**: Install the required packages by running:
   ```bash
   pip install -r requirements.txt

2. Set Up API Tokens: Create a file named secret_token.txt and add your OpenAI token.

3. Configure the Script:

    Update the date in main.py to today's date.

    Adjust file paths within the script to match your system's configuration.

4. Run the Script: Execute the main.py file to start generating your podcast episode.

## Code Structure
scrapping.py: Scrappes the news from the base source website. 

summary.py: Summarizes the scraped content to minimize the tokens.

web_search.py: Integrates DuckDuckGo for web search and news aggregation from different sources.

script.py: Manages the generation of podcast scripts using the scrapped and summarized content.

tts.py: Converts the generated text into speech, incorporating emotions and expressions and making .mp3 file. 

## Future Enchancements
Voice Cloning: Plans to incorporate voice cloning technology to create realistic guest voices on the podcast.

Automated Uploads: Integration of automation scripts to streamline the uploading of episodes to Spotify and the website.
