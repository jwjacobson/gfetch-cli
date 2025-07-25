# Default recipe - list available commands
default SESSION_NAME="gfetch-cli":
    @just --list

# Run app
run:
    uv run gfetch

# Run tests
test *args:
    uv run pytest {{ args }}
