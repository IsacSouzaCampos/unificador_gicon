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
        registers['0400'] = lib.extract_registers(texts, '0400')
        registers['0500'] = lib.extract_registers(texts, '0500')
        registers['0600'] = lib.extract_registers(texts, '0600')
        dictionary[list(dictionary.keys())[0]] = registers['0400'] + dictionary[list(dictionary.keys())[0]]
        dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0500']
        dictionary[list(dictionary.keys())[-1]] = dictionary[list(dictionary.keys())[-1]] + registers['0600']

        final_text = lib.order_lines(result_txt, dictionary)

        lib.write_result(final_text)

        view.close_main_window()
