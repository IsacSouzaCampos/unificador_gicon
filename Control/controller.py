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

        # dictionary, company_numbers = lib.get_data(texts)
        # dictionary = lib.filter_data(texts, dictionary)

        registers = dict()
        # registers['0400'] = lib.extract_registers(texts, '0400')
        # registers['0500'] = lib.extract_registers(texts, '0500')
        # registers['0600'] = lib.extract_registers(texts, '0600')
        #
        # dictionary[list(dictionary.keys())[0]] = registers['0400'] + dictionary[list(dictionary.keys())[0]]
        # dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0500']
        # dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0600']

        texts_m_regs = lib.extract_m_registers(texts)

        print('*****EXTRAINDO VALORES*****')
        values = ['M100', 'M105', 'M110', 'M200', 'M205', 'M210', 'M500', 'M505', 'M510', 'M600', 'M605', 'M610']
        registers.update({k: list() for k in values})
        for m_regs in texts_m_regs:
            for reg in m_regs:
                reg_value = reg.split('|')[1]
                for value in values:
                    if value == reg_value:
                        registers[value].append(reg)

        for i in [1, 2, 5, 6]:
            print(f'{i = }')
            print(f'{registers[f"M{i}00"] = }')
            print(f'{registers[f"M{i}05"] = }')
            print(f'{registers[f"M{i}10"] = }')
        print('\n')

        for value in [100, 105, 205, 210, 500, 505, 605, 610]:
            registers[f'M{value}'] = lib.order_list(registers[f'M{value}'], 1)

        for i in [1, 2, 5, 6]:
            print(f'{i = }')
            print(f'{registers[f"M{i}00"] = }')
            print(f'{registers[f"M{i}05"] = }')
            print(f'{registers[f"M{i}10"] = }')
        print('\n')

        for value in [100, 105, 500, 505]:
            registers[f'M{value}'] = lib.order_list(registers[f'M{value}'], 2)

        for i in [1, 2, 5, 6]:
            print(f'{i = }')
            print(f'{registers[f"M{i}00"] = }')
            print(f'{registers[f"M{i}05"] = }')
            print(f'{registers[f"M{i}10"] = }')
        print('\n')

        for value in [100, 105, 500, 505]:
            if value == 100:
                registers[f'M{value}'] = lib.sum_columns(registers[f'M{value}'], first_index=3, aliquot_col=4)
            elif value == 210:
                registers[f'M{value}'] = lib.sum_columns(registers[f'M{value}'], first_index=3, aliquot_col=7)
            else:
                registers[f'M{value}'] = lib.sum_columns(registers[f'M{value}'], first_index=3)

        for i in [1, 2, 5, 6]:
            print(f'{i = }')
            print(f'{registers[f"M{i}00"] = }')
            print(f'{registers[f"M{i}05"] = }')
            print(f'{registers[f"M{i}10"] = }')
        print('\n')

        for i, m_regs in enumerate(texts_m_regs):
            texts_m_regs[i] = lib.set_dependencies(m_regs)

        # for text_regs in texts_m_regs:
        #     for reg in text_regs:
        #         print(list(reg.keys())[0])
        # print('\n')

        m_regs = lib.order_m_regs(texts_m_regs)

        # for reg in m_regs:
        #     # print(list(reg.keys())[0])
        #     print(f'{reg = }')

        # final_text = lib.order_lines(result_txt, dictionary, m_regs)
        # lib.write_result(final_text)
        # view.close_main_window()
