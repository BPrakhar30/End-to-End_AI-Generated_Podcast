import os
import openai

def read_summary_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:  
            return file.read().strip()

def generate_podcast_script(api_key, prompt, system_message):
    openai.api_key = api_key
    try:
        response = openai.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

def process_news_and_generate_scripts(api_key, summaries_dir, introduction_file, output_file):
    # Reading all summary files
    summaries = []
    for file_name in os.listdir(summaries_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(summaries_dir, file_name)
            summary = read_summary_file(file_path)
            summaries.append(summary)
    
    # Generating the introduction
    introduction_text = read_summary_file(introduction_file)
    system_message_intro = "Act as Dan, the host of the news podcast show 'Dreampods News'. Write an introduction based on the provided news summary. Do not narrate the news yet, just give an introduction. Do not include any special characters, just introduction with normal text."
    introduction_script = generate_podcast_script(api_key, introduction_text, system_message_intro)
    
    # Generating scripts for each summary
    system_message_news = "Act as Dan, the host of the news podcast show 'Dreampods News'. Write the script for the news in Dan's style. Do not include any introduction or conclusion, just the news narration, without any special symbols or brackets. Give narration text in a single paragraph. When the news has repeating information, just narrate that information once."
    scripts = []
    for summary in summaries:
        script = generate_podcast_script(api_key, summary, system_message_news)
        scripts.append(script + "\n\n")
    
    # Generating the conclusion
    introduction_text = read_summary_file(introduction_file)
    system_message_intro = "Act as Dan, the host of the news podcast show 'Dreampods News'. Write a conclusion for the episode based on the provided news summaries. Do not narrate the news, just give a conclusion without any special characters."
    conclusion_script = generate_podcast_script(api_key, introduction_text, system_message_intro)

    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    # Writing all scripts to a single output file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(introduction_script + "\n\n")
        output_file.writelines(scripts)
        output_file.write(conclusion_script)

    return f"Podcast script has been written to {output_file}"
