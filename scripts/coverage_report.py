import ast
import json
import sys
import trace
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "fasd_costs"
sys.path.insert(0, str(ROOT / "src"))


def statement_lines(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {node.lineno for node in ast.walk(tree) if isinstance(node, ast.stmt)}


runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=1)
tracer = trace.Trace(count=True, trace=False, ignoredirs=[sys.prefix, sys.exec_prefix])

def discover_and_run():
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    return runner.run(suite)

result = tracer.runfunc(discover_and_run)
counts = tracer.results().counts

total = 0
covered = 0
files = {}
for path in sorted(SRC.glob("*.py")):
    statements = statement_lines(path)
    executed = {line for (filename, line), count in counts.items() if Path(filename).resolve() == path.resolve() and count}
    hit = len(statements & executed)
    total += len(statements)
    covered += hit
    files[path.name] = {"statements": len(statements), "covered": hit}

report = {
    "method": "Python trace execution mapped to AST statement lines",
    "tests_successful": result.wasSuccessful(),
    "tests_run": result.testsRun,
    "statements": total,
    "covered_statements": covered,
    "statement_coverage_percent": round(100 * covered / total, 1),
    "files": files,
}
(ROOT / "outputs").mkdir(exist_ok=True)
(ROOT / "outputs" / "coverage.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if result.wasSuccessful() else 1)
