# Contributing

Thank you for considering a contribution to this proof-of-concept research
software project.

## Before submitting a change

1. Keep all examples synthetic and free of identifiable or confidential data.
2. Preserve the distinction between software-test outputs and empirical FASD
   cost estimates.
3. Run the automated tests, coverage check and benchmark:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/coverage_report.py
PYTHONPATH=src python3 scripts/benchmark.py --runs 30
```

4. If Docker is available, build the image and run the containerised tests:

```bash
docker build -t fasd-cost-framework .
docker run --rm fasd-cost-framework
```

## Pull requests

Describe the purpose of the change, the files affected and the checks performed.
Update documentation and tests when behaviour changes. Do not present synthetic
outputs as clinical, epidemiological or policy estimates.
