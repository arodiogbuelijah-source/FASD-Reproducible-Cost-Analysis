# Reproducible FASD Cost Analysis

This repository contains the executable proof-of-concept analysis described in
the accompanying manuscript. It generates deterministic synthetic data,
validates the records, calculates direct healthcare and criminal justice cost
outputs, writes machine-readable results, and creates an HTML report.

## Reproduce

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/coverage_report.py
PYTHONPATH=src python3 scripts/benchmark.py --runs 30
```

The analysis uses Python's standard library only. The random seed is
`20260916`. Identical code, configuration and interpreter versions should
produce byte-identical CSV and JSON analytical outputs.

## Important scope statement

All person-level records are synthetic. Unit costs are software-test
parameters and are not estimates of the economic burden of FASD. Parameters
drawn from external publications retain their published price basis; the proof
of concept applies no inflation or currency adjustment.

## Repository structure

- `src/fasd_costs`: data generation, validation, costing and pipeline modules
- `data/unit_costs.csv`: parameter values, provenance and price basis
- `tests`: positive, negative and repeatability tests
- `scripts/benchmark.py`: repeated execution and timing procedure
- `outputs`: generated analytical outputs and execution metadata
- `Dockerfile`: pinned container definition
- `Jenkinsfile`: continuous-integration definition
- `.github/workflows/ci.yml`: public automated test and coverage workflow

GitHub Actions runs the automated tests and coverage procedure on pushes and
pull requests. The Jenkins definition remains available as an alternative
pipeline specification and includes the benchmark and container-build stages.

## Availability

The source code is publicly available at:

https://github.com/arodiogbuelijah-source/FASD-Reproducible-Cost-Analysis

Version 1.0.0 is permanently archived on Zenodo:

https://doi.org/10.5281/zenodo.22787519

The repository is distributed under the MIT License.
