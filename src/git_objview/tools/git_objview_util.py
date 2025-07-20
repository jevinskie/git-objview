import argparse

from path import Path

from git_objview.app import GitObjViewApp


def real_main(args: argparse.Namespace):
    print(f"args.repo: {args.repo}")
    app = GitObjViewApp(git_repo_path=args.repo)
    app.run()


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="git-objview")
    parser.add_argument(
        "-C",
        "--repo",
        type=Path,
        default=".",
        metavar="GIT_REPO_PATH",
        help="Path to git repo to view",
    )
    return parser


def main():
    real_main(get_arg_parser().parse_args())


if __name__ == "__main__":
    main()
