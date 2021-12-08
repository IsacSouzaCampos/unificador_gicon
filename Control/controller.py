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

        # M100 e M200 separar pelas aliquotas (coluna 5)
        for reg_value in ['M100', 'M105', 'M200']:
            registers[reg_value] = lib.extract_registers(texts, reg_value)

        for reg_value in ['M100', 'M105']:
            registers[reg_value] = lib.order_list(registers[reg_value], 1)
            registers[reg_value] = lib.group_list(registers[reg_value], 1)

            temp_registers = []
            for reg in registers[reg_value]:
                temp_registers.append(lib.order_list(reg, 2))
            registers[reg_value] = temp_registers

            # for reg in registers[reg_value]:
            #     print(f'{reg = }')
            # print()

            temp_registers = []
            for regs in registers[reg_value]:
                # print(f'{regs = }')
                temp_registers.append(lib.group_list(regs, 2))
            registers[reg_value] = temp_registers

            # for reg in registers[reg_value]:
            #     print(f'{reg = }')
            # print()

            # temp_registers = []
            # for reg in registers[reg_value]:
            #     # print(f'{reg = }')
            #     for r in reg:
            #         temp_registers.append(lib.sum_columns(r, first_index=3))
            # registers[reg_value] = temp_registers

            # for reg in registers[reg_value]:
            #     print(f'{reg = }')
            # print()

        for reg_value in ['M100']:
            temp_registers1 = []
            for regs1 in registers[reg_value]:
                temp_registers2 = []
                for regs2 in regs1:
                    # print(f'{regs2 = }')
                    temp_registers2.append(lib.group_aliquot(regs2, 4))
                temp_registers1.append(temp_registers2)
            registers[reg_value] = temp_registers1

        temp_registers = []
        for regs1 in registers['M100']:
            for regs2 in regs1:
                for lst in regs2:
                    temp_registers.append(lib.sum_columns(lst, first_index=3, aliquot_col=4))
        registers['M100'] = temp_registers

        temp_registers = []
        for regs in registers['M105']:
            for lst in regs:
                temp_registers.append(lib.sum_columns(lst, first_index=3))
        registers['M105'] = temp_registers

        registers['M200'] = [lib.sum_columns(registers['M200'], first_index=1)]

        for reg in registers['M100']:
            print(f'{reg = }')
        print()

        for reg in registers['M105']:
            print(f'{reg = }')
        print()

        for reg in registers['M200']:
            print(f'{reg = }')
        print()

        # dictionary[list(dictionary.keys())[0]] = registers['0400'] + dictionary[list(dictionary.keys())[0]]
        # dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0500']
        # dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0600']

        # final_text = lib.order_lines(result_txt, dictionary)

        # lib.write_result(final_text)

        view.close_main_window()
