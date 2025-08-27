# dte-triage-tool
Tool to support Desktop Test Engineering triage test cases for future automation

## Environment

We use `uv` to manage our environment, as a way to test-pilot this tool to replace
`pipenv` in other DTE-managed Python projects. See
[Astral's docs](https://docs.astral.sh/uv/) for more information, including how to
add, remove, and update dependencies.

To initialize env:
* `uv sync`
* `source .venv/bin/activate` on Mac / Linux / WSL
* `.venv\Scripts\activate` on PowerShell

## Testing

We use `hurl` to test our API requests. See documentation at
[Hurl's page](https://hurl.dev/).

We use `playwright` to test our UI. See documentation at the
[Playwright project page](https://playwright.dev/python/docs/intro) for more.

We use `pytest` to bring it all together.
* [Pytest documentation](https://docs.pytest.org/en/stable/)
* [Pytest Playwright](https://playwright.dev/python/docs/test-runners)
