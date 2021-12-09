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
        except Exception as e:
            print(e)
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
        except Exception as e:
            print(e)
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
        return dictionary

    @staticmethod
    def extract_registers(texts, reg_num):
        registers = list()
        for text in texts:
            for line in text:
                if line.split('|')[1] == reg_num:
                    registers.append(line.strip())

        return registers

    @staticmethod
    def extract_m_registers(texts, reg_type: int):
        registers = list()
        for text in texts:
            for line in text:
                if f'M{reg_type}' in line.split('|')[1]:
                    registers.append(line.strip())

        return registers

    @staticmethod
    def order_lines(result_txt: list, dictionary: dict, m_registers: list) -> list:
        size = len(result_txt)
        final_text = list()
        i = 0
        while i < size:
            line = result_txt[i]
            splitted_line = line.split('|')
            if splitted_line[1] == '0140':
                final_text.append(line.strip())
                while i < size:
                    line = result_txt[i + 1]
                    if line.split('|')[1] not in ['0150', '0190', '0200', '0400', '0450']:
                        for d_line in dictionary[int(splitted_line[2])]:
                            final_text.append(d_line.strip())
                        break
                    else:
                        final_text.append(line.strip())
                    i += 1
            elif splitted_line[1] == 'M001':
                final_text.append(line.strip())
                for m_regs_line in m_registers:
                    final_text.append(m_regs_line.strip())
            else:
                final_text.append(line.strip())
            i += 1

        return final_text

    @staticmethod
    def order_list(lst: list, col: int) -> list:
        i = 0
        while i < len(lst) - 1:
            _current = lst[i].split('|')[1:-2]  # remove campos vazios ['', 'M100', ..., '']
            _next = lst[i + 1].split('|')[1:-2]
            if int(_next[col]) < int(_current[col]):
                temp = lst[i]
                lst[i] = lst[i + 1]
                lst[i + 1] = temp
                if i > 0:
                    i -= 2
            i += 1

        return lst

    @staticmethod
    def group_list(lst: list, col: int) -> list:
        if not lst:
            return []
        if len(lst) == 1:
            return [lst]

        size = len(lst)
        temp_list = list()
        groups = list()
        for i in range(size - 1):
            _current = lst[i].split('|')[1:-2]  # remove campos vazios ['', 'M100', ..., '']
            _next = lst[i + 1].split('|')[1:-2]
            if _current[col] != _next[col]:
                temp_list.append(lst[i])
                groups.append(temp_list)
                temp_list = []
            else:
                temp_list.append(lst[i])

        if temp_list:
            groups.append(temp_list)

        last = lst[-1].split("|")[1:-2]
        next_to_last = lst[-2].split("|")[1:-2]
        if last[col] == next_to_last[col]:
            if groups:
                groups[-1].append(lst[-1])
            else:
                groups.append([lst[-1]])
        else:
            groups.append([lst[-1]])

        return groups

    @staticmethod
    def group_aliquot(lst: list, col: int) -> list:
        if not lst:
            return []
        if len(lst) == 1:
            return [lst]

        size = len(lst)
        temp_list = list()
        groups = list()
        for i in range(size - 1):
            _current = lst[i].split('|')[1:-2]  # remove campos vazios ['', 'M100', ..., '']
            _next = lst[i + 1].split('|')[1:-2]
            if round(float(_current[col].replace(',', '.')), 2) != round(float(_next[col].replace(',', '.')), 2):
                temp_list.append(lst[i])
                groups.append(temp_list)
                temp_list = []
            else:
                temp_list.append(lst[i])

        if temp_list:
            groups.append(temp_list)

        last = lst[-1].split("|")[1:-2]
        next_to_last = lst[-2].split("|")[1:-2]
        if round(float(next_to_last[col].replace(',', '.')), 2) == round(float(last[col].replace(',', '.')), 2):
            if groups:
                groups[-1].append(lst[-1])
            else:
                groups.append([lst[-1]])
        else:
            groups.append([lst[-1]])

        return groups

    @staticmethod
    def sum_columns(lst: list, first_index: int, aliquot_col: int = None) -> str:
        lst_splitted = list()
        for line in lst:
            lst_splitted.append(line.split('|')[1:-1])

        aliquot = -1
        if aliquot_col is not None:
            aliquot = lst_splitted[0][aliquot_col]

        size = len(lst_splitted[0][:-1])
        result = [0 if c.replace(',', '').isnumeric() else c for c in lst_splitted[0][first_index:]]
        for line in lst_splitted:
            for i, pos in enumerate(range(first_index, size + 1)):
                value = line[pos].replace(',', '.')
                if value.replace('.', '').isnumeric():
                    result[i] += float(value)

                result[i] = round(result[i], 2) if isinstance(result[i], float) else result[i]
                if result[i] == 0:
                    result[i] = int(result[i])

        if aliquot_col is not None:
            aliquot = aliquot.replace(',', '.')
            aliquot = round(float(aliquot), 2)
            result[aliquot_col - first_index] = str(aliquot).replace('.', ',')

        init = lst[0].split("|")[1:-2][:first_index]
        return f'|{"|".join([str(element).replace(".", ",") for element in init + result])}|'

    def sum_m_regs_cols(self, texts):
        registers = dict()
        for reg_value in ['M100', 'M105', 'M110', 'M200', 'M205', 'M210', 'M500', 'M505', 'M510',
                          'M600', 'M605', 'M610']:
            registers[reg_value] = self.extract_registers(texts, reg_value)

        for reg_value in ['M100', 'M105', 'M110', 'M205', 'M210', 'M500', 'M505', 'M510',
                          'M600', 'M605', 'M610']:
            registers[reg_value] = self.order_list(registers[reg_value], 1)
            registers[reg_value] = self.group_list(registers[reg_value], 1)

        for reg_value in ['M100', 'M105', 'M110']:
            temp_registers = []
            for reg in registers[reg_value]:
                temp_registers.append(self.order_list(reg, 2))
            registers[reg_value] = temp_registers

            temp_registers = []
            for regs in registers[reg_value]:
                temp_registers.append(self.group_list(regs, 2))
            registers[reg_value] = temp_registers

        # group by aliquot
        for reg_value in ['M100']:
            temp_registers1 = []
            for regs1 in registers[reg_value]:
                temp_registers2 = []
                for regs2 in regs1:
                    temp_registers2.append(self.group_aliquot(regs2, 4))
                temp_registers1.append(temp_registers2)
            registers[reg_value] = temp_registers1

        temp_registers = []
        for regs1 in registers['M100']:
            for regs2 in regs1:
                for lst in regs2:
                    temp_registers.append(self.sum_columns(lst, first_index=3, aliquot_col=4))
        registers['M100'] = temp_registers

        temp_registers = []
        for regs in registers['M105']:
            for lst in regs:
                temp_registers.append(self.sum_columns(lst, first_index=3))
        registers['M105'] = temp_registers

        temp_registers = []
        for regs in registers['M110']:
            for lst in regs:
                temp_registers.append(self.sum_columns(lst, first_index=3))
        registers['M110'] = temp_registers

        registers['M200'] = [self.sum_columns(registers['M200'], first_index=1)]

        temp_registers = []
        for lst in registers['M205']:
            temp_registers.append(self.sum_columns(lst, first_index=3))
        registers['M205'] = temp_registers

        temp_registers = []
        for lst in registers['M210']:
            temp_registers.append(self.sum_columns(lst, first_index=2, aliquot_col=7))
        registers['M210'] = temp_registers

        return registers['M100'], registers['M105'], registers['M110'], \
            registers['M200'], registers['M205'], registers['M210'], \
            registers['M500'], registers['M505'], registers['M510'], \
            registers['M600'], registers['M605'], registers['M610']

    @staticmethod
    def write_result(final_text: list):
        with open(r'arquivos\resultado_final.txt', 'w', encoding='ISO-8859-1') as fout:
            for line in final_text:
                print(line, file=fout)
