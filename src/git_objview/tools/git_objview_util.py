import argparse
from typing import TYPE_CHECKING

from path import Path

from git_objview.app import GitObjViewApp
from git_objview.db import Repo

if not TYPE_CHECKING:
    from rich import print


def real_main(args: argparse.Namespace):
    print(f"args.repo: {args.repo}")
    if not args.dump:
        app = GitObjViewApp(git_repo_path=args.repo)
        app.run()
    else:
        repo = Repo(args.repo)
        print(repo)
        repo.dump()
        print("repo dump done")


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
    parser.add_argument("-d", "--dump", action="store_true", help="Dump git repo info")
    return parser


def main():
    real_main(get_arg_parser().parse_args())


if __name__ == "__main__":
    main()
