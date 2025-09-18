import subprocess
from dotenv import load_dotenv
from os import environ
from tempfile import TemporaryDirectory
from pathlib import Path

TEST_LOC = "tests/hurl/hurl_files"
BASE_VARS = f"{TEST_LOC}/base.vars"
VARS_TO_HURLIFY = ["TESTRAIL_USERNAME", "TESTRAIL_API_KEY"]


def test_run_hurl(hurl_test, vars_file, result):
    """Execute the hurl tests"""
    load_dotenv()
    for var in VARS_TO_HURLIFY:
        environ[f"HURL_{var}"] = environ.get(var)
    # We add the explicit vars file to the base.vars
    # TODO: What if we need to overwrite?
    this_vars_file = BASE_VARS
    if vars_file != "base.vars":
        temp_dir = TemporaryDirectory()
        temp_file = Path(temp_dir.name, "tmp.vars")
        with (
            open(BASE_VARS) as bv,
            open(f"{TEST_LOC}/{vars_file}.vars") as vf,
            open(temp_file, "w") as tvf,
        ):
            vars_text = bv.read() + vf.read()
            tvf.write(vars_text)
        this_vars_file = temp_file

    # TODO: catch subprocess.CalledProcessError
    command = (
        f"hurl --variables-file {this_vars_file} {TEST_LOC}/{hurl_test}.hurl --test"
    )
    hurl_output = subprocess.check_output(
        command.split(" "),
        stderr=subprocess.STDOUT,
    )
    result_str = "Success" if result == "pass" else "Failure"
    assert result_str in hurl_output.decode()
