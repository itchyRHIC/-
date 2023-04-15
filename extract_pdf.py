import PyPDF2
import openai

openai.api_key = '//OpenAIのAPIキー//'

def extract_pdf_text(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        text = []
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text.append(page.extract_text())

        return text


def get_summary(text):
    # system = """与えられた文章の翻訳を行い、かつポイントをlatex形式で書かれた数式を含めて3点にまとめてください。フォーマットは以下に従ってください。'''
    #         タイトルの日本語訳
    #         ・要点1
    #         ・要点2
    #         ・要点3
    #         本文の日本語訳
    #         '''"""    
    system = """与えられた文章のポイントを数式を含めて3点にまとめてください。フォーマットは以下に従ってください。'''
            ・要点1
            ・要点2
            ・要点3
            '''"""

    summary = []
    for page in text:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model="gpt-4",
            messages=[
                {'role': 'system', 'content':system},
                {'role':'user', 'content':page}
            ],
            temperature=0.25,
        )
        summary.append(response['choices'][0]['message']['content'])
    return summary


def save_text_to_file(text, output_file):
    with open(output_file, "w") as file:
        for page in text: 
            file.write(page)
            file.write('\n\n')


if __name__ == "__main__":
    print('name of input file: ')
    pdf_file_path = input()
    print('name of output file: ')
    output_file_path = input()
    
    extracted_text = extract_pdf_text(pdf_file_path)
    summary_text = get_summary(extracted_text)
    save_text_to_file(summary_text, output_file_path)

    print(f"Extracted text saved to {output_file_path}")
