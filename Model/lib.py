import os


class Lib:
    def extract_files_lines(self):
        texts_lines = list()
        for file in os.listdir('arquivos'):
            try:
                text_lines = self.extract_file_lines('arquivos', file)
            except Exception as e:
                raise e
            if text_lines is not None:
                texts_lines.append(text_lines)

        return texts_lines

    @staticmethod
    def extract_file_lines(directory: str, file: str) -> list or None:
        if os.path.isdir(fr'{directory}\{file}') or 'resultado' in file:
            return

        try:
            with open(fr'arquivos\{file}', 'r') as fin:
                return fin.readlines()
        except:
            try:
                with open(fr'arquivos\{file}', 'rb') as fin:
                    text = fin.read().decode('ISO-8859-1')
                    return text.splitlines()
            except Exception as e:
                raise Exception(file, e)

    @staticmethod
    def extract_result_file_lines() -> list:
        try:
            with open(r'arquivos\resultado.txt', 'rb') as fin:
                text = fin.read().decode('ISO-8859-1')
                result_txt = text.splitlines()
        except:
            raise Exception

        return result_txt

    @staticmethod
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

    @staticmethod
    def filter_data(texts, dictionary: dict) -> dict:
        for key in dictionary:
            filtered_list = list()
            data = dictionary[key]
            lines = texts[data[0]][data[1]:data[2]]
            for line in lines:
                if line.split('|')[1] == '0450':
                    filtered_list.append(line)
            dictionary[key] = filtered_list
        # print(f'{dictionary.keys() = }')
        return dictionary

    @staticmethod
    def extract_0400_registers(texts):
        _0400_registers = list()
        for text in texts:
            for line in text:
                if line.split('|')[1] == '0400':
                    _0400_registers.append(line)

        return _0400_registers

    @staticmethod
    def extract_0500_registers(texts):
        _0500_registers = list()
        for text in texts:
            for line in text:
                if line.split('|')[1] == '0500':
                    _0500_registers.append(line)

        return _0500_registers

    @staticmethod
    def order_lines(result_txt: list, dictionary: dict) -> list:
        size = len(result_txt)
        final_text = list()
        i = 0
        while i < size:
            line = result_txt[i]
            splitted_line = line.split('|')
            if splitted_line[1] == '0140':
                # print(f'{splitted_line[2] = }')
                final_text.append(line.strip())
                while i < size:
                    line = result_txt[i + 1]
                    if line.split('|')[1] not in ['0150', '0190', '0200', '0400', '0450']:
                        # print(f'{line = }')
                        for d_line in dictionary[int(splitted_line[2])]:
                            final_text.append(d_line.strip())
                        break
                    else:
                        final_text.append(line.strip())
                    i += 1
            else:
                final_text.append(line.strip())
            i += 1

        return final_text

    @staticmethod
    def write_result(final_text: list):
        with open(r'arquivos\resultado_final.txt', 'w', encoding='ISO-8859-1') as fout:
            for line in final_text:
                print(line, file=fout)