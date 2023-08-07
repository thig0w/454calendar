tox.ini:
	@printf "[tox]\n\
envlist =\n\
    #skipsdist = False\n\
    py310\n\
\n\
[testenv]\n\
deps =\n\
    -r requirements.txt\n\
    httpx\n\
    black\n\
    ruff\n\
    pydocstyle\n\
    pytest\n\
    pytest-clarity\n\
    pytest-dotenv\n\
\n\
commands = pytest\n\
    " > tox.ini

.pre-commit-config.yaml:
	@printf "repos:\n\
  - repo: https://github.com/pre-commit/pre-commit-hooks\n\
    rev: v2.3.0\n\
    hooks:\n\
    - id: check-yaml\n\
    - id: end-of-file-fixer\n\
    - id: trailing-whitespace\n\
    - id: fix-encoding-pragma\n\
    - id: requirements-txt-fixer\n\
    - id: mixed-line-ending\n\
  - repo: https://github.com/psf/black\n\
    rev: 22.10.0\n\
    hooks:\n\
    - id: black\n\
  - repo: https://github.com/charliermarsh/ruff-pre-commit\n\
    rev: 'v0.0.241'\n\
    hooks:\n\
    - id: ruff\n\
  - repo: https://github.com/pycqa/isort\n\
    rev: 5.12.0\n\
    hooks:\n\
    - id: isort\n\
      name: isort (python)\n\n\
  - repo: https://github.com/sourcery-ai/sourcery\n\
    rev: v1.6.0\n\
    hooks:\n\
    - id: sourcery\n\
      # The best way to use Sourcery in a pre-commit hook:\n\
      # * review only changed lines:\n\
      # * omit the summary\n\
      args: [--diff=git diff HEAD, --no-summary]\n\
    " > .pre-commit-config.yaml

pytest.ini:
	@printf "[pytest]\n\
addopts =\n\
    # generate report with details of all (non-pass) test results\n\
    -ra\n\
    # show local variables in tracebacks\n\
    --showlocals\n\
    # verbose output\n\
    --verbose\n\
norecursedirs =\n\
    .git\n\
    .pytest_cache\n\
    .idea\n\
    migrations\n\
    .venv\n\
filterwarnings =\n\
    error\n\
    ignore::UserWarning\n\
    ignore:function ham\(\) is deprecated:DeprecationWarning\n\
    " > pytest.ini
