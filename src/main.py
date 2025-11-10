"""Entry point for the multimodal assistant CLI."""

from .assistant import run_cli_loop


def main() -> None:
    run_cli_loop()


if __name__ == "__main__":
    main()
