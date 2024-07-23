#!/bin/bash

set -x
set -e

TIME=${TIME:-30}

FOLDER=results/$(date --iso-8601=seconds)
for model in passthrough monet mosaic edges; do
  F=${FOLDER}/${model}
  mkdir -p $F
  python3 bench.py --time $TIME --transform  $model
  python3 plot_single.py
  mv *.csv *.pdf $F
done
