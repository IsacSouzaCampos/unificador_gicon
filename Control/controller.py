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

        registers['M100'], registers['M105'], registers['M110'], \
            registers['M200'], registers['M205'], registers['M210'], \
            registers['M500'], registers['M505'], registers['M510'], \
            registers['M600'], registers['M605'], registers['M610'] = lib.sum_m_regs_cols(texts)

        for i in [4, 8]:
            registers[f'M{i}00'] = lib.extract_m_registers(texts, i)

        m_regs = list()
        for reg_value in ['M100', 'M105', 'M110', 'M200', 'M205', 'M210', 'M500', 'M505', 'M510',
                          'M600', 'M605', 'M610']:
            for reg in registers[reg_value]:
                m_regs.append(reg)

        # m_600s = lib.extract_m_registers(texts, 6)
        # m_600s = [line for line in m_600s if 'M600' in line]
        # m_600s = lib.sum_columns(m_600s, first_index=1)

        # m_regs2 = list()
        # for reg_value in [f'M{i}00' for i in range(6, 9)]:
        #     for reg in registers[reg_value]:
        #         m_regs2.append(reg)
        #
        # m_regs2 = [line for line in m_regs2 if 'M600' not in line]
        #
        # m_regs = m_regs1 + [m_600s] + m_regs2

        final_text = lib.order_lines(result_txt, dictionary, m_regs)
        lib.write_result(final_text)
        view.close_main_window()
