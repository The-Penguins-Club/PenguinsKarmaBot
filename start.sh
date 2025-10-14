#!/bin/bash
set -m  # enable job control

python -m Karma &
python -m bot &

wait -n  # wait for one to exit
exit $?  # exit with its status
