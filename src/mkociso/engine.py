from argparse import ArgumentParser
from logging import basicConfig, getLogger, INFO
from os import getcwd, getenv, path
from importlib import resources
from shutil import move
from subprocess import run
from requests import get

import boto3
import mkociso.lorax_templates as lorax_templates

logger = getLogger(__name__)


class OcisoImageBuildOutput(object):
    def __init__(self, boot_iso, checksum, vol_id):
        self.vol_id = vol_id
        self.checksum = checksum
        self.boot_iso = boot_iso

class OcisoEngine(object):
    # f"--mirrorlist=https://mirrors.rpmfusion.org/mirrorlist?repo=nonfree-fedora-{cli_args.release}&arch={cli_args.arch}",
    def __init__(self):
        pass

    def build_iso(self, release, image, arch, sources, packages):
        logger.info(f"building image f{release}/{arch}/{image}")

        image_name = image.split("/")[-1]
        image_name_untagged = image_name.split(":")[0]
        brand_image_name = image_name_untagged.split("-")[0]
        brand_image_variant = "-".join(image_name_untagged.split("-")[1:])

        PWD = getcwd()
        nvidia = "nvidia" in image
        github_workspace = getenv("GITHUB_WORKSPACE", PWD)
        logger.info(f"building image variant {brand_image_variant}")
        logger.info(f"nvidia variant = {nvidia}")
        logger.info(f"using github workspace = {github_workspace}")

        lorax_output_dir = path.join(github_workspace, "build", f"offline.{image_name}")
        vol_id = f"UBlue-{image_name_untagged}-{release}-{arch}"
        mirror = self._select_mirror(arch, release)
        logger.info(f"selected mirror {mirror}")

        with resources.path(lorax_templates, "lorax-configure-repo.tmpl") as lorax_configure_repo, resources.path(lorax_templates, "lorax-embed-repo.tmpl") as lorax_embed_repo:
            lorax_cmd = [
                "sudo",
                "lorax",
                "--product=Fedora",
                f"--version={release}",
                f"--release={release}",
                f"--source={mirror}",
                "--nomacboot",
                f"--volid={vol_id[:31]}",
                "--rootfs-size",
                "8",
                "--force",
                "--add-template-var",
                f"ostree_oci_ref={image}",
                "--add-template-var",
                "ostree_osname=default",
                "--add-template",
                str(lorax_configure_repo),
                "--add-template",
                str(lorax_embed_repo),
                "--installpkgs",
                "glibc-langpack-*",
                "--installpkgs",
                "langpacks-*",
            ]
            
            for source in sources:
                lorax_cmd.append("-s")
                lorax_cmd.append(source)

            for package in packages:
                lorax_cmd.append("-i")
                lorax_cmd.append(package)
            
            lorax_cmd.append(lorax_output_dir)

        logger.debug(f"executing lorax command {' '.join(lorax_cmd)}")
        logger.info("starting lorax compose, it may take a while")
        lorax_process = run(lorax_cmd, capture_output=True)

        if lorax_process.returncode == 0:
            boot_iso = path.join(lorax_output_dir, "images", "boot.iso")
            logger.info(f"lorax command succeeded proceding to create CHECKSUM file")
            checksum_cmd = ["sha256sum", "--tag", boot_iso]
            checksum_result = run(checksum_cmd, capture_output=True)
            checksum_output = checksum_result.stdout.decode("utf-8").splitlines()[0]
            checksum_hash = checksum_output.split(" ")[-1]

            if checksum_result.returncode == 0:
                logger.info("successfully created CHECKSUM file")

                return OcisoImageBuildOutput(
                    boot_iso,
                    checksum_hash,
                    vol_id,
                )
            else:
                raise Exception(
                    f"there was an error generating CHECKSUM: {checksum_result.stderr.decode('utf-8')}"
                )
        else:
            raise Exception(
                f"lorax process failed: {lorax_process.stderr.decode('utf-8')}"
            )

    def _select_mirror(self, arch, release):
        mirror_list = get(
            f"https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-{release}&arch={arch}"
        )

        return mirror_list.text.split("\n")[1]
