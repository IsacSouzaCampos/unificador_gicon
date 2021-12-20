import sys

from Model.lib import Lib
from View.view import View


class Controller:
    @staticmethod
    def run():
        lib = Lib()
        view = View()

        view.start_main_window()

        try:
            texts = lib.extract_files_lines()
        except Exception as e:
            view.error_1(e)
            sys.exit()

        try:
            result_txt = lib.extract_result_file_lines()
        except Exception as e:
            print(e)
            view.error_2()
            sys.exit()

        dictionary, company_numbers = lib.get_data(texts)
        dictionary = lib.filter_data(texts, dictionary)

        registers = dict()
        registers['0400'] = lib.extract_registers(texts, '0400')
        registers['0500'] = lib.extract_registers(texts, '0500')
        registers['0600'] = lib.extract_registers(texts, '0600')

        dictionary[list(dictionary.keys())[0]] = registers['0400'] + dictionary[list(dictionary.keys())[0]]
        dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0500']
        dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0600']

        # print('*****EXTRAINDO VALORES*****')
        texts_m_regs = lib.extract_m_registers(texts)

        registers_parents = lib.gen_parentness(texts_m_regs)

        # for reg in registers:
        #     print(reg)

        values = set()
        for i in [1, 2, 6]:
            values.add(f'M{i}00')
            values.add(f'M{i}05')
            values.add(f'M{i}10')
            registers[f'M{i}00'] = list()
            registers[f'M{i}05'] = list()
            registers[f'M{i}10'] = list()

        for lst in registers_parents:
            for register in lst:
                # print(f'{register = }')
                reg_value = register.split('|')[1]
                if reg_value in values:
                    registers[reg_value].append(register)

        # print('*****SOMANDO COLUNAS*****')

        # *********** M100 ***********
        reg_value = 'M100'
        # print(f'{registers["M100"] = }')
        registers[reg_value] = lib.order_list(registers[reg_value], 1)
        temp = list()
        for group1 in lib.group_list(registers[reg_value], 1):
            group1 = lib.order_list(group1, 2)
            # print(f'{group1 = }')
            for group2 in lib.group_list(group1, 2):
                group2 = lib.order_list(group2, 4)
                for group3 in lib.group_list(group2, 4):
                    res = lib.sum_columns(group3, first_index=3, aliquot_col=4)
                    # print(f'{res = }')
                    temp.append(res)
        registers[reg_value] = temp
        # print(f'{registers["M100"] = }')

        # *********** M105 ***********
        reg_value = 'M105'
        # print(f'{registers["M105"] = }')
        registers['M105'] = lib.order_list(registers[reg_value], 1)
        temp = list()
        for group1 in lib.group_list(registers[reg_value], 1):
            group1 = lib.order_list(group1, 2)
            for group2 in lib.group_list(group1, 2):
                res = lib.sum_columns(group2, first_index=3)
                temp.append(res)
        registers[reg_value] = temp
        # print(f'{registers["M105"] = }')

        # *********** M200 ***********
        reg_value = 'M200'
        # print(f'{registers["M200"] = }')
        registers[reg_value] = [lib.sum_columns(registers[reg_value], first_index=1)]
        # print(f'{registers["M200"] = }')

        # *********** M205 ***********
        reg_value = 'M205'
        # print(f'{registers["M205"] = }')
        registers[reg_value] = lib.order_list(registers[reg_value], 1)
        temp = list()
        for group1 in lib.group_list(registers[reg_value], 1):
            group1 = lib.order_list(group1, 2)
            for group2 in lib.group_list(group1, 2):
                temp.append(lib.sum_columns(group2, first_index=3))
        registers[reg_value] = temp
        # print(f'{registers["M205"] = }')

        # *********** M210 ***********
        reg_value = 'M210'
        # print(f'{registers["M210"] = }')
        registers[reg_value] = lib.order_list(registers[reg_value], 1)
        temp = list()
        for group1 in lib.group_list(registers[reg_value], 1):
            group1 = lib.order_list(group1, 7)
            for group2 in lib.group_list(group1, 7):
                temp.append(lib.sum_columns(group2, first_index=2, aliquot_col=7))
        registers[reg_value] = temp
        # print(f'{registers["M210"] = }')

        # *********** M500 ***********
        reg_value = 'M500'
        registers[reg_value] = list()
        # print(f'{registers_parents = }')
        for rp in registers_parents:
            for register in rp:
                if 'M5' in register.split('|')[1]:
                    registers[reg_value].append(register)
        # print(f'{registers["M500"] = }')
        groups = dict()
        key = ''
        for register in registers[reg_value]:
            if register.split('|')[1] == 'M500':
                aliquot = round(float(register.split('|')[5].replace(',', '.')), 2)
                values = register.split('|')[1:4] + [str(aliquot)]
                key = '|'.join(values)
                if key in groups:
                    groups[key].append(register)
                else:
                    groups[key] = [register]
            else:
                groups[key].append(register)
        # print(f'{registers["M500"]}')
        temp = list()
        for key, regs in groups.items():
            m_500 = [reg for reg in regs if reg.split('|')[1] == 'M500']
            m_500 = lib.order_list(m_500, 1)
            for group1 in lib.group_list(m_500, 1):
                group1 = lib.order_list(group1, 2)
                for group2 in lib.group_list(group1, 2):
                    group2 = lib.order_list(group2, 4)
                    for group3 in lib.group_list(group2, 4):
                        temp.append(lib.sum_columns(group3, first_index=3, aliquot_col=4))
            m_505 = [reg for reg in regs if reg.split('|')[1] == 'M505']
            m_505 = lib.order_list(m_505, 1)
            for group1 in lib.group_list(m_505, 1):
                group1 = lib.order_list(group1, 2)
                for group2 in lib.group_list(group1, 2):
                    temp.append(lib.sum_columns(group2, first_index=3))
        # print(f'{temp = }')
        registers[reg_value] = temp
        # print(f'{registers["M500"] = }')

        # *********** M600 ***********
        reg_value = 'M600'
        # print(f'{registers["M600"] = }')
        registers[reg_value] = [lib.sum_columns(registers[reg_value], first_index=1)]
        # print(f'{registers["M600"] = }')

        # *********** M605 ***********
        reg_value = 'M605'
        # print(f'{registers["M605"] = }')
        registers[reg_value] = lib.order_list(registers[reg_value], 1)
        temp = list()
        for group1 in lib.group_list(registers[reg_value], 1):
            group1 = lib.order_list(group1, 2)
            for group2 in lib.group_list(group1, 2):
                temp.append(lib.sum_columns(group2, first_index=3))
        registers[reg_value] = temp
        # print(f'{registers["M605"] = }')

        # *********** M610 ***********
        reg_value = 'M610'
        # print(f'{registers["M610"] = }')
        registers[reg_value] = lib.order_list(registers[reg_value], 1)
        temp = list()
        for group1 in lib.group_list(registers[reg_value], 1):
            group1 = lib.order_list(group1, 7)
            for group2 in lib.group_list(group1, 7):
                temp.append(lib.sum_columns(group2, first_index=2, aliquot_col=7))
        registers[reg_value] = temp
        # print(f'{registers["M610"] = }')

        m_regs = list()
        for reg_value in ('M100', 'M105', 'M200', 'M205', 'M210', 'M500', 'M600', 'M605', 'M610'):
            for register in registers[reg_value]:
                m_regs.append(register)
        # print(f'{m_regs = }')

        final_text = lib.order_lines(result_txt, dictionary, m_regs)
        lib.write_result(final_text)
        view.close_main_window()
