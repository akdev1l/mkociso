make-builder:
    podman build \
        -v $PWD/build:/outdir \
        --target builder \
        -t mkociso:builder \
        -f Containerfile.builder \
        .

make-rpm:
    podman build \
        -v $PWD/build:/outdir \
        --target build \
        -t mkociso:rpm \
        .

make-container:
    podman build \
        --target app \
        -t mkociso:latest \
        -t "mkociso:$(date +'%Y-%m-%d')" \
        .

test-container:
    podman run \
        --rm \
        -it \
        mkociso:latest \
            --image ghcr.io/ublue-os/silverblue-main:38 \
            --release 38

clean:
    rm -rf build
