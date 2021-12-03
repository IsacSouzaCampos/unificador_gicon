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
        except:
            view.error_2()
            sys.exit()

        dictionary, company_numbers = lib.get_data(texts)
        dictionary = lib.filter_data(texts, dictionary)

        registers = dict()
        # registers['0400'] = lib.extract_registers(texts, '0400')
        # registers['0500'] = lib.extract_registers(texts, '0500')
        # registers['0600'] = lib.extract_registers(texts, '0600')

        registers['M100'] = lib.extract_registers(texts, 'M100')
        registers['M100'] = lib.order_list(registers['M100'], 1)
        registers['M100'] = lib.group_list(registers['M100'], 1)

        temp_registers = list()
        for reg in registers['M100']:
            temp_registers.append(lib.order_list(reg, 2))
        registers['M100'] = temp_registers

        for reg in registers['M100']:
            print(f'{reg = }')
        print()

        temp_registers = []
        for reg in registers['M100']:
            temp_registers.append(lib.group_list(reg, 2))
        registers['M100'] = temp_registers

        temp_registers = []
        for reg in registers['M100']:
            for r in reg:
                temp_registers.append(lib.sum_columns(r, first_index=3))
        registers['M100'] = temp_registers

        for reg in registers['M100']:
            print(f'{reg = }')

        # dictionary[list(dictionary.keys())[0]] = registers['0400'] + dictionary[list(dictionary.keys())[0]]
        # dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0500']
        # dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0600']

        # final_text = lib.order_lines(result_txt, dictionary)

        # lib.write_result(final_text)

        view.close_main_window()
