# Reproducible FASD Cost Analysis

[![Reproducibility checks](https://github.com/arodiogbuelijah-source/FASD-Reproducible-Cost-Analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/arodiogbuelijah-source/FASD-Reproducible-Cost-Analysis/actions/workflows/ci.yml)

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

## Container execution

```bash
docker build -t fasd-cost-framework .
docker run --rm fasd-cost-framework
```

The container executes the automated test suite. GitHub Actions also runs the
native tests, coverage measurement, 30-run benchmark, container build and
containerised tests on pushes and pull requests.

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
- `Jenkinsfile`: alternative continuous-integration specification
- `.github/workflows/ci.yml`: public automated reproducibility workflow
- `CITATION.cff`: software citation metadata

## Reproducibility evidence

The archived 30-run local benchmark in `outputs/benchmark.json` was executed
against commit `a65fece3d6c49216dbdb5bb35a932626b6fbe198`. It recorded 30
successful runs with identical output hashes. The GitHub Actions workflow
provides public, version-specific evidence for later commits. Docker and GitHub
Actions results should be interpreted separately from the unexecuted Jenkins
specification.

## Availability and citation

The source code is publicly available at:

https://github.com/arodiogbuelijah-source/FASD-Reproducible-Cost-Analysis

Version 1.0.0 is permanently archived on Zenodo:

https://doi.org/10.5281/zenodo.22787519

Please cite the archived release using `CITATION.cff`. The repository is
distributed under the MIT License. Contributions should follow
`CONTRIBUTING.md`, and security-related concerns should follow
`SECURITY.md`.
