# genpark-branch-and-bound-integer-programming-skill

[![GitHub stars](https://img.shields.io/github/stars/Alpha-Park/genpark-branch-and-bound-integer-programming-skill?style=social)](https://github.com/Alpha-Park/genpark-branch-and-bound-integer-programming-skill/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0%20external-brightgreen.svg)](#)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard%20Compatible-orange.svg)](#)

> Autonomous Agent Branch and Bound Mixed-Integer Linear Programming (MILP) Solver with LP Relaxation Pruning

Part of the **GenPark Autonomous Operations Research & Combinatorial Optimization Swarm**.

## Architecture Overview

```mermaid
graph TD
    A[MILP Problem Formulation] --> B[Root Node LP Relaxation]
    B --> C{Integer Feasible?}
    C -->|Yes| D[Update Incumbent Best Solution]
    C -->|No| E[Select Most Fractional Variable]
    E --> F[Branch Floor x <= floor]
    E --> G[Branch Ceil x >= ceil]
    F --> H[LP Relaxation with Bound Pruning]
    G --> I[LP Relaxation with Bound Pruning]
    H --> J{Subproblem Pruning Criteria}
    I --> J
    J -->|Infeasible / Bounded| K[Prune Subtree]
    J -->|Fractional Feasible| E
    J -->|Integral & Better| D
    D --> L[Optimal MILP Solution]
```

## Features

- **Pure Python Standard Library**: Zero external dependencies (no NumPy, SciPy, or PuLP needed). Runs anywhere.
- **Production-Grade Design**: Type annotations, exhaustive edge cases, robust numerical stability.
- **MCP Server Ready**: Built-in stdio Model Context Protocol (MCP) server for Claude / Cursor / Agent tool calling.
- **Benchmark Validated**: 100% verified test coverage in isolated sandbox environments.

## Quickstart

```bash
git clone https://github.com/Alpha-Park/genpark-branch-and-bound-integer-programming-skill.git
cd genpark-branch-and-bound-integer-programming-skill
python example_usage.py
```

## Model Context Protocol (MCP) Usage

```bash
python mcp_server.py
```

## License

MIT License. Designed for autonomous agentic workflows.
