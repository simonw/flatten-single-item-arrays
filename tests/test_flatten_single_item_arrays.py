from click.testing import CliRunner
from flatten_single_item_arrays.cli import cli
import json
import pytest
import textwrap


@pytest.mark.parametrize(
    "input,expected_output",
    (
        ([{"foo": "bar", "bar": 5}], [{"foo": "bar", "bar": 5}]),
        ([{"foo": ["bar"], "bar": 5}], [{"foo": "bar", "bar": 5}]),
        (
            [{"foo": ["bar"], "bar": 5}, {"foo": ["baz"], "bar": 5}],
            [{"foo": "bar", "bar": 5}, {"foo": "baz", "bar": 5}],
        ),
        (
            [{"foo": ["bar"], "bar": 5}, {"foo": "baz", "bar": 5}],
            [{"foo": ["bar"], "bar": 5}, {"foo": "baz", "bar": 5}],
        ),
    ),
)
def test_process(input, expected_output, tmpdir):
    filepath = tmpdir / "input.json"
    filepath.write_text(json.dumps(input), "utf-8")
    runner = CliRunner()
    result = runner.invoke(cli, [str(filepath)])
    assert result.exit_code == 0
    assert json.loads(result.output) == expected_output


def test_debug():
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(
        cli,
        ["-", "--debug"],
        input=json.dumps([{"foo": ["bar"], "bar": 5}, {"foo": ["baz"], "bar": 5}]),
    )
    assert json.loads(result.output) == [
        {"foo": "bar", "bar": 5},
        {"foo": "baz", "bar": 5},
    ]
    assert (
        result.stderr.strip()
        == textwrap.dedent(
            """
    Item count: 2
    count_of_single_item_lists
    {
        "foo": 2
    }
    count_of_present_keys
    {
        "foo": 2,
        "bar": 2
    }
    keys_to_reformat:
    - foo
    """
        ).strip()
    )


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")
