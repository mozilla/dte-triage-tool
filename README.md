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

To add a test:
* Create the hurl description file at tests/hurl/hurl_files/[name].hurl
* If you need variables defined, add those additional key-value pairs to
  a file in that same folder, with file extension .vars
* Update /tests/hurl/manifest.yaml like this example:
    ```yaml
    get_sample_payload:
        result: pass
        variables-file: suite_tests
    ```
* If you need to test that something fails, set `result` to `fail`
* If you need to skip a test, set `result` to `skip`

We use `playwright` to test our UI. See documentation at the
[Playwright project page](https://playwright.dev/python/docs/intro) for more.

We use `pytest` to bring it all together.
* [Pytest documentation](https://docs.pytest.org/en/stable/)
* [Pytest Playwright](https://playwright.dev/python/docs/test-runners)
