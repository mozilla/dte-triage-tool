import subprocess
from dotenv import load_dotenv
from os import environ

TEST_LOC = "tests/hurl/hurl_files"

def test_run_hurl(hurl_test, vars_file, result):
    load_dotenv()
    userauth = f"{environ['USERNAME']}:{environ['API_KEY']}"
    hurl_output = subprocess.check_output(
        f"hurl -u {userauth} --variables-file {TEST_LOC}/{vars_file} {TEST_LOC}/{hurl_test}.hurl --test".split(" "),
        stderr=subprocess.STDOUT
    )
    result_str = "Success" if result == "pass" else "Failure"
    assert result_str in hurl_output.decode()
