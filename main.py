import sys
import os

import PySimpleGUI as sg


def main():
    texts = list()
    for file in os.listdir('arquivos'):
        if os.path.isdir(fr'arquivos\{file}') or 'resultado' in file:
            continue
            # sg.popup('Certifique-se de que todos os arquivos se encontram no formato ".txt".')
            # sys.exit()

        try:
            with open(fr'arquivos\{file}', 'r') as fin:
                texts.append(fin.readlines())
        except:
            try:
                with open(fr'arquivos\{file}', 'rb') as fin:
                    text = fin.read().decode('ISO-8859-1')
                    texts.append(text.splitlines())
            except Exception as e:
                sg.popup(f'Erro ao ler o arquivo {file}')
                print(e)
                sys.exit()

    with open(r'arquivos\resultado.txt', 'rb') as fin:
        text = fin.read().decode('ISO-8859-1')
        result_txt = text.splitlines()

    # validate(texts)
    dictionary, company_numbers = get_data(texts)

    dictionary = filter_data(texts, dictionary)

    final_text = list()
    for line in result_txt:
        final_text.append(line)
        splitted_line = line.split('|')
        if splitted_line[1] == '0140':
            print(f'{splitted_line[2] = }')
            for d_line in dictionary[int(splitted_line[2])]:
                final_text.append(d_line)

    # header = texts[0][:_min]
    # footer = texts[0][_max:]

    # final_text = header + final_text + footer

    with open(r'arquivos\resultado_final.txt', 'w', encoding='ISO-8859-1') as fout:
        for line in final_text:
            print(line, file=fout)


# def validate(texts: list):
#     cnpjs = list()
#     for text in texts:
#         cnpjs.append(text[0].split('|')[9])
#
#     for cnpj in cnpjs:
#         if cnpj != cnpjs[0]:
#             sg.popup('Certifique-se de que há apenas arquivos de uma empresa na pasta e tente novamente.')
#             sys.exit()


def get_data(texts: list) -> tuple:
    # [text_number(0, 1), initial_line, final_line]
    dictionary = dict()
    company_numbers = list()
    for text_index, t in enumerate(texts):
        i = 0
        size = len(t)
        while i < size:
            line = t[i]
            if '|0140|' in line and line.split('|')[1] == '0140':
                num = int(line.split('|')[2])  # numero da filial
                if num not in dictionary.keys():
                    company_numbers.append(num)
                    dictionary[num] = [text_index, i]
                    i += 1
                    while i < size:
                        line = t[i]
                        if ('|0140|' in line and line.split('|')[1] == '0140') or '|0990|' in line:
                            dictionary[num].append(i)
                            i -= 1
                            break
                        i += 1
            i += 1
    return dictionary, company_numbers


def filter_data(texts, dictionary: dict) -> dict:
    for key in dictionary:
        filtered_list = list()
        data = dictionary[key]
        lines = texts[data[0]][data[1]:data[2]]
        for line in lines:
            if line.split('|')[1] == '0450':
                filtered_list.append(line)
        dictionary[key] = filtered_list
    print(f'{dictionary.keys() = }')
    return dictionary


if __name__ == '__main__':
    sg.theme('default1')
    layout = [[sg.Text('Processando...', pad=((60, 60), (1, 1)))]]
    window = sg.Window('Unificador', layout, disable_close=True, finalize=True)
    main()
    window.close()
