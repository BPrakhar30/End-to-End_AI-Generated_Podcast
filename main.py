import os
from pathlib import Path
import json
from datetime import datetime
from openai import OpenAI
from scrapping import scrape_and_save_content
from summary import summarize_text
from script import process_news_and_generate_scripts
from tts import generate_tts_for_script
from web_search import append_summary_to_files 

# Parameters
sports_url = "https://www.cnn.com/sport"
urls = [sports_url]

# Current date
date = "July 8"    # change this

base_dir = Path(r"aipodcast\scrapping")
save_dir = Path(fr"aipodcast\web_search_sports_pipeline\data\scrapped_news\{date}")
input_directory = save_dir
individual_output_directory = Path(fr"aipodcast\web_search_sports_pipeline\data\news_summaries\individual_news_summary\{date}")
combined_output_directory = Path(fr"aipodcast\web_search_sports_pipeline\data\news_summaries\combined_news_summary\{date}")

summaries_dir = individual_output_directory
introduction_file = combined_output_directory / 'combined_summaries.txt'
output_script_file = Path(fr"aipodcast\web_search_sports_pipeline\data\podcast_script\{date}") / 'podcast_script.txt'


prepend_audio_path = base_dir / "podcast/music/dreampodsintrofinal_out.mp3"
outro_file_path = base_dir / "podcast/music/dreampodsoutrofinal.mp3"
output_audio_directory = Path(fr"aipodcast\web_search_sports_pipeline\data\podcast_episode\{date}")

# Reading the api key
with open('secret_token.txt', 'r') as file:
    api_key = file.read().strip()
client = OpenAI(api_key=api_key)


if __name__ == "__main__":
    # Scraping and saving content
    scrape_and_save_content(save_dir, urls)
    
    # Summarizing the content
    summarize_text(api_key, input_directory, individual_output_directory, combined_output_directory)

    # Appending the news from different sources
    append_summary_to_files(api_key, individual_output_directory, "full")
 
    # Generating the podcast script
    process_news_and_generate_scripts(api_key, summaries_dir, introduction_file, output_script_file)

    # Generating TTS for the script
    generate_tts_for_script(client, output_script_file, prepend_audio_path, outro_file_path, output_audio_directory)