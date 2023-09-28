FROM fedora:39 as builder

RUN dnf install \
        --disablerepo='*' \
        --enablerepo='fedora,updates' \
        --setopt install_weak_deps=0 \
        --assumeyes \
        'dnf-command(builddep)' \
        rpkg

WORKDIR /usr/src

RUN rpkg spec --outdir /outdir

RUN dnf builddep -y /outdir/*.spec

FROM builder as build

RUN rpkg local --outdir /outdir
