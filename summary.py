import os
import openai

def summarize_text(api_key, input_dir, individual_output_dir, combined_output_dir):
    openai.api_key = api_key
    combined_summaries = []

    # Ensuring the output directories exist
    os.makedirs(individual_output_dir, exist_ok=True)
    os.makedirs(combined_output_dir, exist_ok=True)

    # Reading each text file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                article = file.read()

            try:
                title_response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert in generating titles for the news articles that are searchable query on the web. Generate a short and crisp title for the following news article that can be searched easily on the web. Do not include any special characters or question marks."},
                        {"role": "user", "content": article}
                    ],
                    temperature=0.3
                )
                title = title_response.choices[0].message.content.strip()
                title = title.replace('"', '').replace(':', '').replace('/', '').replace('\\', '').strip()
            except Exception as e:
                title = filename.replace('.txt', '')

            # Generating the summary using LLM
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert in writing the news summary. You have to summarize the following news in not more than 150 words. Just write the summarized points without using any special symbols and do not give headings to the summary. Just give only one summarized paragraph for each news."},
                        {"role": "user", "content": article}
                    ],
                    temperature=0.3
                )
                summary = response.choices[0].message.content
                summary = summary.replace('"', '').strip()
            except Exception as e:
                summary = "No Summary Available"
            
            # Writing the summary to an output file with the same name
            individual_output_file_path = os.path.join(individual_output_dir, f"{title}.txt")
            with open(individual_output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(summary)
            
            # Appending the summary to the combined list
            combined_summaries.append(f"{title}:\n{summary}\n\n")

    # Writing the combined summaries to a single output file
    combined_output_file_path = os.path.join(combined_output_dir, 'combined_summaries.txt')
    with open(combined_output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(combined_summaries)

    # Generating a final 200-word summary of the combined summaries
    with open(combined_output_file_path, 'r', encoding='utf-8') as file:
        combined_content = file.read()

    try:
        final_response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in summarizing text. Please summarize the following content into one paragraph not exceeding 200 words."},
                {"role": "user", "content": combined_content}
            ],
            temperature=0.3
        )
        final_summary = final_response.choices[0].message.content
        final_summary = final_summary.replace('"', '').strip()
    except Exception as e:
        final_summary = "No Summary Available"

    with open(combined_output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(final_summary)

    return f"Individual summaries have been written to {individual_output_dir} and combined summary to {combined_output_file_path}"