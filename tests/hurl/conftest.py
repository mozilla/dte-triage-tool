import yaml
import logging

MANIFEST_LOC = "tests/hurl/manifest.yaml"


def pytest_generate_tests(metafunc):
    """Convert Hurl tests to PyTests"""
    manifest = yaml.safe_load(open(MANIFEST_LOC))
    argnames = ["hurl_test", "vars_file", "result"]
    argvalues = []
    for k, v in manifest.items():
        vars_file = "base.vars"
        if v.get("variables-file"):
            vars_file = v["variables-file"]
        if v["result"] != "skip":
            argvalues.append((k, vars_file, v["result"]))
    logging.warning(argvalues)
    if "hurl_test" in metafunc.fixturenames:
        metafunc.parametrize(argnames, argvalues, ids=[a[0] for a in argvalues])
