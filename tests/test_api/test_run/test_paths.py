from svst import api


def test_run_single_file(tmp_path):
    file_path = tmp_path / "module.py"
    file_path.write_text("a = 1\n")

    assert list(api.run([str(file_path)])) == [
        f'{file_path}:1: error: Variable "a" is missing a standalone variable type '
        f'annotation in the scope "global"  [no-untyped-var]'
    ]


def test_run_directory(tmp_path):
    (tmp_path / "module.py").write_text("a = 1\n")
    (tmp_path / "notes.txt").write_text("a = 1\n")

    assert len(list(api.run([str(tmp_path)]))) == 1


def test_run_syntax_error(tmp_path):
    file_path = tmp_path / "broken.py"
    file_path.write_text("def (\n")

    (error,) = api.run([str(file_path)])

    assert error.startswith(f"{file_path}:1: error: ")
    assert error.endswith("  [syntax]")
