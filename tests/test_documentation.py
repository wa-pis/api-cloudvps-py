import ast
import re
import unittest
from pathlib import Path


class DocumentationTests(unittest.TestCase):
    def test_readme_python_examples_parse_independently(self):
        readme = (Path(__file__).parents[1] / "README.rst").read_text()
        blocks = re.findall(
            r"\.\. code-block:: python\n\n((?:   .*\n|\n)+)",
            readme,
        )
        self.assertTrue(blocks)
        for block in blocks:
            source = "\n".join(line[3:] for line in block.splitlines())
            with self.subTest(source=source.splitlines()[0]):
                ast.parse(source)


if __name__ == "__main__":
    unittest.main()
