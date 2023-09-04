FROM fedora:38 as builder

RUN dnf install \
        --disablerepo='*' \
        --enablerepo='fedora,updates' \
        --setopt install_weak_deps=0 \
        --assumeyes \
        'dnf-command(builddep)' \
        rpkg

COPY . /usr/src

WORKDIR /usr/src

RUN rpkg spec --outdir /tmp \
    && dnf builddep -y /tmp/*.spec

FROM builder as build

RUN rpkg local --outdir /outdir
