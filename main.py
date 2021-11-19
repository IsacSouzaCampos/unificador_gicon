import os


def main():
    text = list()
    for file in os.listdir('arquivos'):
        if '.py' in file:
            continue

        try:
            with open(f'arquivos/{file}', 'r') as fin:
            # with open(fr'arquivos\{file}', 'r') as fin:
                text.append(fin.readlines())
        except Exception as e:
            print(e)
            with open(f'arquivos/{file}', 'r', encoding='utf-8') as fin:
            # with open(fr'arquivos\{file}', 'r', encoding='utf-8') as fin:
                text.append(fin.readlines())

    dictionary = dict()

    for i, line in enumerate(text[0]):
        if '|0140|' in line:
            num = int(line.split('|')[1])  # numero da filial
            dictionary[num] = f'0;{i}'  # texto 0, linha i

    comp_numbers = list()
    for text_index, t in enumerate(text):
        i = 0
        size = len(t)
        while i < size:
            line = t[i]
            if '|0140|' in line and line.split('|')[1] == '0140':
                num = int(line.split('|')[2])  # numero da filial
                if num not in dictionary.keys():
                    comp_numbers.append(num)
                    dictionary[num] = f'{text_index};{i};'  # texto 0, linha i
                    i += 1
                    while i < size:
                        line = t[i]
                        if ('|0140|' in line and line.split('|')[1] == '0140') or '|0990|' in line:
                            dictionary[num] = dictionary[num] + f'{i};'
                            break
                        i += 1
            i += 1

    for n in sorted(comp_numbers):
        print(n, dictionary[n])


if __name__ == '__main__':
    main()

