# Advent of Code Solutions **

Welcome to my Advent of Code repository. Here you'll find my solutions to the Advent of Code programming puzzle. I'm currently working through the 2025 puzzles and occasionally hopping back to earlier years to fill in gaps. This project is a work in progress and will be updated as I solve more challenges.

## Built with Pure Python

All solutions in this repository are written in **pure Python** — no external dependencies required. That decision keeps the code simple and portable, nudges me to lean on the standard library, and helps me keep sharpening my Python skills.

## Project Structure

```text
AdventOfCode/
├── README.md
├── <year>/
│   ├── day_<N>/
│   │   ├── main.py
│   │   └── <data.txt> (add your own input)
├── utils/
│   ├── __init__.py
│   ├── files.py
│   └── ...
```

- `<year>/day_<N>/` — solutions for each day of Advent of Code for a given year, with input data and Python scripts.
- `data.txt` — files live in each `day_<N>` folder, but they are not committed here to respect Advent of Code's policy — drop your own puzzle input before running.
- `utils/` — utility scripts for input parsing, math helpers, and other reusable tools.

## About Advent of Code

[Advent of Code](https://adventofcode.com/) is an annual set of holiday-themed programming challenges. Feel free to explore the puzzles yourself—it’s a solid opportunity to practice coding, problem-solving, and algorithms.

---

Released under the MIT License.
