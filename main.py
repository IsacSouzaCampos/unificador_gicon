import sys
import os

import PySimpleGUI as sg


def main():
    texts = list()
    for file in os.listdir('arquivos'):
        if '.py' in file:
            continue

        try:
            with open(fr'arquivos\{file}', 'r') as fin:
                texts.append(fin.readlines())
        except Exception as e:
            print(e)
            with open(fr'arquivos\{file}', 'r', encoding='utf-8') as fin:
                texts.append(fin.readlines())

    validate(texts)
    dictionary, company_numbers = get_data(texts)

    final_text = list()
    for n in sorted(company_numbers):
        # print(n, dictionary[n])
        data = dictionary[n]
        final_text += texts[data[0]][data[1]:data[2]]

    _max = 0
    _min = len(texts[0])
    for key in dictionary:
        data = dictionary[key]
        if data[0] == 0:
            if data[1] < _min:
                _min = data[1]
            if data[2] > _max:
                _max = data[2]

    header = texts[0][:_min]
    footer = texts[0][_max:]

    final_text = header + final_text + footer

    with open('resultado.txt', 'w', encoding='utf-8') as fout:
        for line in final_text:
            print(line, end='', file=fout)


def validate(texts):
    cnpjs = list()
    for text in texts:
        cnpjs.append(text[0].split('|')[9])

    for cnpj in cnpjs:
        if cnpj != cnpjs[0]:
            sg.popup('Certifique-se de que há apenas arquivos de uma empresa na pasta e tente novamente.')
            sys.exit()


def get_data(texts):
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


if __name__ == '__main__':
    sg.theme('default1')
    layout = [[sg.Text('Processando...', pad=((60, 60), (1, 1)))]]
    window = sg.Window('Unificador', layout, disable_close=True, finalize=True)
    main()
    window.close()
