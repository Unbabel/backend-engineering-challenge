#!/usr/bin/env bash

set -o errexit
set -o pipefail

main() {
    local -r data_folder="$1"

    pushd "$data_folder" >/dev/null
    for f in *.json ; do
        [ -f "$f" ] || break

        enki --input_file "$f" --window_size 10 > ${f%%.*}.out

        diff ${f%%.*}.expected ${f%%.*}.out
    done;
    popd >/dev/null
}

main "$@"
