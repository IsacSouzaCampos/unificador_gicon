import os


def main():
    text = list()
    for file in os.listdir('arquivos'):
        if '.py' in file:
            continue

        try:
            with open(fr'arquivos\{file}', 'r') as fin:
                text.append(fin.readlines())
        except Exception as e:
            print(e)
            with open(fr'arquivos\{file}', 'r', encoding='utf-8') as fin:
                text.append(fin.readlines())

    dictionary = dict()
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

    final_text = list()
    for n in sorted(comp_numbers):
        print(n, dictionary[n])
        data = dictionary[n]
        final_text += text[data[0]][data[1]:data[2]]

    _max = 0
    _min = len(text[0])
    for key in dictionary:
        data = dictionary[key]
        if data[0] == 0:
            if data[1] < _min:
                _min = data[1]
            if data[2] > _max:
                _max = data[2]

    header = text[0][:_min]
    footer = text[0][_max:]

    final_text = header + final_text + footer

    with open('resultado.txt', 'w', encoding='utf-8') as fout:
        for line in final_text:
            print(line, end='', file=fout)


if __name__ == '__main__':
    main()
