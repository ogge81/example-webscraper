from app.cli import build_parser


def test_build_parser_parses_flags() -> None:
    parser = build_parser()
    args = parser.parse_args(
        ["https://example.com", "--pretty", "--links-only", "--internal-only"]
    )

    assert args.url == "https://example.com"
    assert args.pretty is True
    assert args.links_only is True
    assert args.internal_only is True