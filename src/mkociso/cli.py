#!/usr/bin/env python3

from argparse import ArgumentParser
from logging import basicConfig, getLogger, INFO
from json import dumps
from os import getcwd, getenv
from shutil import move
from subprocess import run
from requests import get

import boto3

from mkociso.engine import OcisoEngine

basicConfig(
    level=getenv('MKOCISO_LOG', default=INFO),
    format="[%(asctime)s] %(name)s:%(levelname)s # %(message)s",
)

logger = getLogger("mkociso")


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-r",
        "--release",
        choices=[38, 39, 40],
        default=38,
        type=int,
        help="Fedora release",
    )
    arg_parser.add_argument(
        "-i",
        "--image",
        required=True,
        help="Container image to use for installation",
    )
    arg_parser.add_argument(
        "-a",
        "--arch",
        default="x86_64",
        help="Target architecture",
    )
    arg_parser.add_argument(
        "-o",
        "--output",
        help="Output directory",
        default=getcwd(),
    )
    arg_parser.add_argument(
        "-w",
        "--web",
        action="store_true",
        help="Use anaconda web installer [EXPERIMENTAL]",
    )
    arg_parser.add_argument(
        "-n",
        "--net",
        action="store_true",
        default=False,
        help="Create netinstaller with boot_menu.yml",
    )

    cli_args = arg_parser.parse_args()

    mkociso_engine = OcisoEngine()
    s3_client = boto3.client("s3")

    build_result = mkociso_engine.build_iso(
        cli_args.release,
        cli_args.image,
        cli_args.arch,
        cli_args.web,
        cli_args.net,
    )
    upload_result = None

    if cli_args.output.startswith("s3://"):
        bucket_name = cli_args.output.split("/")[2]
        object_key_prefix = "/".join(cli_args.output.split("/")[3:])
        object_key = f"{object_key_prefix}/{build_result.vol_id}.iso"

        logger.info("pushing output to S3 bucket {cli_args.output} key {object_key}")
        s3_client.upload_file(build_result.boot_iso, bucket_name, object_key)

    print(dumps({
        'build': build_result,
        'upload': upload_result,
    }))
