import unittest

from src.utils.utils import format_sequence, is_sequence_valid, get_complementary_sequence
from src.translator import translate_dna_to_protein, mutation_change, mutation_delete, mutation_add

class TestDNAUtilities(unittest.TestCase):
    def test_format_sequence(self):
        self.assertEqual("ATGCGT", format_sequence("atg cgt"))
        self.assertEqual("ATG", format_sequence("AUG"))
        self.assertEqual("ATTTTTGCG", format_sequence("  A uuuu tgcg    "))

    def test_is_sequence_valid(self):
        self.assertTrue(is_sequence_valid("ATGCGT"))
        self.assertFalse(is_sequence_valid("ATGX"))

    def test_get_complementary_sequence(self):
        self.assertEqual("TACGCA", get_complementary_sequence("ATGCGT"))

class TestTranslator(unittest.TestCase):
    def test_translate_dna_to_protein(self):
        self.assertEqual(["Met", "Arg"], translate_dna_to_protein("ATGCGT"))
        with self.assertRaises(ValueError):
            translate_dna_to_protein("ATGX")

    def test_mutation_change(self):
        self.assertEqual("TTGCGT", mutation_change("ATGCGT", [(0, "T")]))
        self.assertEqual("ATGCAT", mutation_change("ATGCGT", [(4, "A")]))
        self.assertEqual("TTGCAT", mutation_change("ATGCGT", [(0, "T"), (4, "A")]))
        self.assertEqual("TTGCCT", mutation_change("ATGCGT", [(0, "T"), (4, "A"), (4, "C")]))

    def test_mutation_delete(self):
        self.assertEqual("TCGT", mutation_delete("ATGCGT", [0, 2]))
        with self.assertRaises(ValueError):
            mutation_delete("ATGCGT", [0, -4])
        with self.assertRaises(TypeError):
            mutation_delete("ATGCGT", [0, 's'])

    def test_mutation_add(self):
        self.assertEqual("TATAGCGT", mutation_add("ATGCGT", [(0, "T"), (2, "A")]))

if __name__ == "__main__":
    unittest.main()
