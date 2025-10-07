# dte-triage-tool

Tool to support Desktop Test Engineering triage test cases for future automation

## Issue reporting

If you find an issue with this tool, please create a bug on Mozilla's BugZilla
instance, that blocks [this bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1993049).

## Pre-setup

The tool requires a `.env` file to exist on the root of the directory where you
cloned the repository. Please do not name this file anything else, and **DO NOT
SAVE SECRETS** to any other file, as you will likely push those secrets to our
upstream, where anyone can see them. The following values need to be set:

* `TESTRAIL_BASE_URL=https://mozilla.testrail.io`
* `TESTRAIL_USERNAME=<valid testrail username>`
* `TESTRAIL_API_KEY=<valid testrail api key>`
* `BUGZILLA_BASE_URL=https://bugzilla.mozilla.org`
* `BUGZILLA_API_KEY=<valid bugzilla api key>`

To obtain usernames and API keys for DTE service accounts, please talk to Ben C
to be added to the vault or receive a secure link.

## Setup

If you just want to start the application the fastest way possible, simply run
`./quickstart.sh` from a compatible terminal's command prompt. (Linux including
WSL, Unix including MacOS terminals). If you don't want to do that or it does
not work, try the following:

You will need to build the UI before starting up streamlit.
Inside `src/UI/`:

* `npm install`

If you wish to run the custom component in a separate server, then:
* `npm run start`

Otherwise, to build the UI component:
* `npm run build`

After either starting the UI server or building the component, run the streamlit
app from the root of the project:
* `uv run streamlit run main.py`

## Usage

The UI should be relatively intuitive. In the beta version, we default to
TestRail project 17 (Fx Desktop). **If you want to use the tool to triage test 
cases in other projects, change the Project ID to the appropriate number.**

Note that the Commit Changes button might be below the break on your browser and
you will have to scroll the left hand panel to find it.

When you hit the Commit Changes button, **TestRail changes are immediately
performed.** Bugzilla changes are not, but JSON files containing the relevant info
are produced. They start with `session_` and contain timestamps. It is expected
that occasionally a single session will produce multiple files.

To commit all of these to Bugzilla, there is a script. **Take note**: only run
the script once per suite modified. Don't just produce a bunch of session files
for multiple suites and run them all together. Given any number of sessions **for
the same suite**:

`uv run python update_bugzilla.py session_2025-09-26T16_17_18Z.json session_2025-09-26T16_19_20Z.json`

Where, of course, the session JSON files are replaced by the one(s) that live on
your filesystem. The new suite and case bugs will block 
[the functional root bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1976270)
by default. Change the global variable to assign bugs to a new root metabug.

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
  contains the keys mentioned in the "Pre-Setup" section.
