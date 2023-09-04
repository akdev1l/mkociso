FROM fedora:38 as app

COPY --from=mkociso:build /outdir/noarch/ /tmp

RUN dnf install -y /tmp/*.rpm

ENTRYPOINT ["/usr/bin/mkociso"]
