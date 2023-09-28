make-builder:
    podman build \
        -f Containerfile.builder \
        -v $PWD/build:/outdir \
        -v $PWD:/usr/src \
        --security-opt label=disable \
        --target builder \
        -t mkociso:builder \
        .

exec-builder:
    podman run \
        --rm \
        -it \
        -v "$PWD:$PWD" \
        -w "$PWD" \
        --security-opt label=disable \
        mkociso:builder

make-rpm:
    podman run \
        --rm \
        -it \
        -v "$PWD:$PWD" \
        -w "$PWD" \
        --security-opt label=disable \
        mkociso:builder \
        bash -c 'rpkg local --outdir /tmp && rm -rf $PWD/build/noarch && mv -v /tmp/noarch $PWD/build'

make-app-container: make-builder && make-rpm
    podman build \
        -t mkociso:latest \
        -t "mkociso:$(date +'%Y-%m-%d')" \
        .

exec-app-container:
    podman run \
        --rm \
        -it \
        -v "$PWD:$PWD" \
        -w "$PWD" \
        --entrypoint /bin/bash \
        --security-opt label=disable \
        mkociso:latest

mkociso *args:
    podman run \
        --rm \
        -it \
        -v "$PWD:$PWD" \
        -w "$PWD" \
        --security-opt label=disable \
        mkociso:latest {{args}}

clean:
    rm -rf build
