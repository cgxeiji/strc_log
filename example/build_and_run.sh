#!/bin/sh

python3 ../libs/strc/tools/make_strc.py --lib-path="../libs/strc" && build/example_logger | python3 ../tools/parse_log.py --database="./strc.json" -l 0 -s
