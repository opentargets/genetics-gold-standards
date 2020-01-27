#!/usr/bin/env bash
#

set -euo pipefail
set -f # No glob

# Args
in_glob='../gold_standards/unprocessed_validated/*.json'
out_prefix='../gold_standards/processed/gwas_gold_standards.191108'

# Get this working directory
work_dir=$(dirname "$0")

# Process
python $work_dir/process_validated.py \
  --input_pattern $work_dir/$in_glob \
  --output $work_dir/$out_prefix.json \
  --grch37_to_38 $work_dir/GRCh37_to_GRCh38.chain.gz \
  --grch38_to_37 $work_dir/GRCh38_to_GRCh37.chain.gz

# Convert to json lines
python $work_dir/../utils/json_to_jsonl.py \
  --input $work_dir/$out_prefix.json \
  --output $work_dir/$out_prefix.jsonl

# Convert to yaml
python $work_dir/../utils/json_yaml_converter.py \
  --input $work_dir/$out_prefix.json \
  --output $work_dir/$out_prefix.yaml

# Convert to tsv
python $work_dir/../utils/json_to_tsv.py \
  --input $work_dir/$out_prefix.json \
  --output $work_dir/$out_prefix.tsv

echo COMPLETE
