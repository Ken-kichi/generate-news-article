from cli import CLI


def run() -> None:
    """Fire ベースの CLI エントリポイントを起動する。

    引数:
        なし

    戻り値:
        なし
    """
    import fire

    fire.Fire(CLI)


if __name__ == "__main__":
    run()
