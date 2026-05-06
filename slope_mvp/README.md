# Slope MVP

Math textbook chapter → competency hierarchy Excel file.

## Setup

```bash
cd slope_mvp
uv sync
cp .env.example .env  # add your ANTHROPIC_API_KEY
```

## Run

```bash
uv run python main.py --input examples/chapter_slope.txt --topic "Slope of Lines" --out out.xlsx
```

## Test

```bash
uv run pytest
```
