# dte-triage-tool
Tool to support Desktop Test Engineering triage test cases for future automation

## Setup
You will need to build the UI before starting up streamlit.
Inside `src/UI/`:

* `npm install`

If you wish to run the custom component in a separate serve, then:
* `npm run start`

Otherwise, to build the UI component:
* `npm run build`

After either starting the UI server or building the component, run the streamlit app from the root of the project:
* `uv run streamlit run main.py`

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

We store secrets securely. Please note the following:
* Do not use the `-u` flag in hurl when writing test harness logic, this
  exposes secrets to the public in the GHA readouts in event of a failure.
* We save the entire value of the `.env` file as a secret in GHA, which
  contains the following keys:
  * TESTRAIL_BASE_URL
  * TESTRAIL_USERNAME
  * TESTRAIL_API_KEY
  * BUGZILLA_BASE_URL
  * BUGZILLA_API_KEY
  * fx_desk_id=17
* To obtain values, please talk to Ben C to be added to the vault.
