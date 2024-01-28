import nbformat
from nbformat import NotebookNode as Notebook
import re
import sys
from dataclasses import dataclass


# For colored terminal output
class COLOR:
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    END = "\033[0m"


@dataclass
class Reference:
    """
    Code comments that reference markdown content.
    """

    text: str
    cell_index: int
    cell_metadata: dict


@dataclass
class CheckResult:
    passed: bool
    msg: str


def get_references(nb):
    """
    Find code cell comments that reference markdown.
    That is, comments are of the form:
      #| content: ....
    """
    references = []
    for index, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        matches = re.findall(r"(?<=^#\| content:).*?$", cell.source, re.MULTILINE)
        references += [Reference(match, index, cell.metadata) for match in matches]
    return references


def check_references_exist(references, nb) -> CheckResult:
    """
    Check all content references exist in the notebook markdown.
    """
    markdown = "\n".join(
        cell.source for cell in nb.cells if cell.cell_type == "markdown"
    )
    unfound_references = [ref for ref in references if ref.text.strip() not in markdown]
    if unfound_references == []:
        return CheckResult(True, "")
    msg = (
        f"  {COLOR.RED}Content tests reference the following markdown,\n"
        f"  but this markdown does not exist in the notebook:{COLOR.END}\n"
    )
    for ref in unfound_references:
        msg += f"  {COLOR.CYAN}Cell {ref.cell_index}:{COLOR.END} "
        msg += f"#| content:{COLOR.BOLD}{ref.text}{COLOR.END}\n"
    return CheckResult(False, msg)


def check_cell_tags(references, nb, tag="remove-cell") -> CheckResult:
    """
    Check all cells containing references have appropriate cell tags.
    """
    bad_cells = set(
        ref.cell_index
        for ref in references
        if tag not in ref.cell_metadata.get("tags", {})
    )
    if bad_cells == set():
        return CheckResult(True, "")
    msg = f'  {COLOR.RED}The following cells are missing "{tag}" tags:{COLOR.END}\n'
    for cell in sorted(list(bad_cells)):
        msg += f"  {COLOR.CYAN}Cell {cell}{COLOR.END} which contains references:\n"
        for ref in references:
            if ref.cell_index == cell:
                msg += f"    #| content:{COLOR.BOLD}{ref.text}{COLOR.END}\n"
    return CheckResult(False, msg)


def check_notebook(path: str) -> bool:
    """
    Run checks on notebook file, print messages, and return bool for pass/fail.
    """
    with open(path) as f:
        nb = nbformat.read(f, 4)
    references = get_references(nb)

    results = [
        check_references_exist(references, nb),
        check_cell_tags(references, nb),
    ]
    failed_results = [r for r in results if not r.passed]
    if failed_results:
        print(f"❌ {path}")
        for r in failed_results:
            print(r.msg)
        return False
    print(f"✅ {path}")
    return True


def cli_entry_point():
    """
    To run from the command line
    """
    paths = sys.argv[1:]
    results = [check_notebook(path) for path in paths]
    if all(results):
        sys.exit(0)
    print(f"\nProblems detected in {len([r for r in results if not r])} notebook(s).\n")
    sys.exit(1)
