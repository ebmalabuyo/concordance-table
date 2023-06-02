import io
import unittest

from concordance import (
    build_stop_words_table, build_concordance_table, write_concordance_table)


class Tests(unittest.TestCase):
    def test_fake_file1(self) -> None:
        stop_words_file = io.StringIO('a\nand\nare\nfor\nnot\nthe\n')

        in_file = io.StringIO(
            'quicksort topology earthquake\n'
            'washington fourscore and seven years ago\n'
            'stop words are handled correctly\n'
            'a the and not for\n'
        )

        out_file = io.StringIO()

        correct_out = (
            'ago: 2\n'
            'correctly: 3\n'
            'earthquake: 1\n'
            'fourscore: 2\n'
            'handled: 3\n'
            'quicksort: 1\n'
            'seven: 2\n'
            'stop: 3\n'
            'topology: 1\n'
            'washington: 2\n'
            'words: 3\n'
            'years: 2\n'
        )

        stop_words = build_stop_words_table(stop_words_file)
        concordance_table = build_concordance_table(in_file, stop_words)
        write_concordance_table(out_file, concordance_table)

        self.assertEqual(out_file.getvalue(), correct_out)

    def test_file1(self) -> None:
        with open('text_files/stop_words.txt') as stop_words_file:
            stop_words = build_stop_words_table(stop_words_file)

        with open('text_files/file1.txt') as in_file:
            concordance_table = build_concordance_table(in_file, stop_words)

        with open('text_files/file1_con.txt', 'w') as out_file:
            write_concordance_table(out_file, concordance_table)

        with open('text_files/file1_con.txt') as student_out, \
             open('text_files/file1_sol.txt') as correct_out:
            self.assertEqual(student_out.read(), correct_out.read())

    def test_declaration(self) -> None:
        with open('text_files/stop_words.txt') as stop_words_file:
            stop_words = build_stop_words_table(stop_words_file)

        with open('text_files/declaration.txt') as in_file:
            concordance_table = build_concordance_table(in_file, stop_words)

        with open('text_files/declaration_con.txt', 'w') as out_file:
            write_concordance_table(out_file, concordance_table)

        with open('text_files/declaration_con.txt') as student_out, \
             open('text_files/declaration_sol.txt') as correct_out:
            self.assertEqual(student_out.read(), correct_out.read())


if __name__ == '__main__':
    unittest.main()
