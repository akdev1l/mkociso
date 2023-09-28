FROM fedora:39

COPY build/noarch /tmp/noarch

RUN dnf install -y /tmp/noarch/*.rpm

ENTRYPOINT ["/usr/bin/mkociso"]
