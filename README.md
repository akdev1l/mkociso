# mkociso: make bootable ISOs ready to deploy OSTree Native Containers

This is a tool meant to simplify the process of generating a bootable ISO ready to deploy an OSTree Native Container system.

This tool is currently in active development and subject to change.

## Development Workflow

We use poetry to manage our dependencies and we follow standard pyproject conventions. If you have poetry installed you can run the
project by doing:

```
poetry install
poetry run mkociso --help
```

### Container builder

We also capture the build environment in a Containerfile to avoid depending on a specific user environment. There are provided just targets
that allow to simplify the workflow of quickly creating an RPM package by calling `just make-rpm`. The `Containerfile.builder` contains the definition
of our build environment for this and it fetches the packages based on the rpkg template.

The container builder is only needed if you don't have the dependencies installed on your host system. Otherwise you can simply call `rpkg local` to create 
a new rpm package.

#### Application Container

As the primary use case for this tool will be GitHub Actions we also provide a container image that can be quickly pulled for use in the action. This actually
speeds up the setup as we don't need to install dependencies every time.

NOTE: ON a local system the application container must run as root because `lorax` requires root to operate. The `justfile` provided does not make an attempt for this to work
and you need to call `sudo podman build` to get this functionality.

### Testing

The easiest way to test `mkociso` is by install poetry and running `sudo poetry run mkociso`. A sample invocation looks like this:

```
sudo poetry run mkociso --image ghcr.io/ublue-os/silverblue-main:38
```

## Command Line Interface

`mkociso` is powered by Python's argparse library and we try to provide documentation with each flag added. Please try `--help` if you have any doubts.

Example:

```
usage: mkociso [-h] [-d] [-r {38,39,40}] -i IMAGE [-a ARCH] [-o OUTPUT] [-w]
               [-n] [-p PACKAGE] [-s SOURCE]

options:
  -h, --help            show this help message and exit
  -d, --dry-run
  -r {38,39,40}, --release {38,39,40}
                        Fedora release
  -i IMAGE, --image IMAGE
                        Container image to use for installation
  -a ARCH, --arch ARCH  Target architecture
  -o OUTPUT, --output OUTPUT
                        Output directory
  -w, --web             Use anaconda web installer [EXPERIMENTAL]
  -n, --net             Create netinstaller with boot_menu.yml
  -p PACKAGE, --package PACKAGE
                        Packages to install in installation runtime
  -s SOURCE, --source SOURCE
                        Repository to add as source during compose
```

**THE COMMAND LINE INTERFACE IS SUBJECT TO CHANGE**
