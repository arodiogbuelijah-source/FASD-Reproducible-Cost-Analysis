# Reproducible FASD Cost Analysis Proof of Concept

This repository contains the executable proof-of-concept analysis described in
the accompanying manuscript. It generates deterministic synthetic data,
validates the records, calculates direct healthcare and criminal justice cost
outputs, writes machine-readable results, and creates an HTML report.

## Reproduce

```bash
python3 -m unittest discover -s tests -v
python3 scripts/benchmark.py --runs 30
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

## Availability

The local Git commit identifies the exact tested version. A public repository
URL and archived release DOI can be added after publication to GitHub and an
archival service such as Zenodo.
