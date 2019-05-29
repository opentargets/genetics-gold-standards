GWAS Gold Standards
===================

WORK IN PROGRESS

Repository for GWAS variant to gene gold standards

Draft schema:
- https://docs.google.com/document/d/1qVc1Th67nmDmQLFuvPXuek1OmR-10R4bp_kgK-cICYw/edit


### How to submit a new gold standard

Todo

- positions must be from gnomad

### Validate and process new gold standards

The sections contains instructions for validating and processing newly submitted gold standards.

```
# Set up environment
conda env create -n goldstandards --file environment.yaml
conda activate gold_standards

# Validate against schema (input can be json or yaml)
python validation/validator.py \
  --input temp/progem/progem.190517.yaml \
  --schema validation/goldstandard_schema.v1.2.json

# Convert to json
python utils/json_yaml_converter.py \
  --input temp/progem/progem.190517.yaml \
  --output temp/progem/progem.190517.json

# Add to `gold_standards/unprocessed_validated`
mv temp/progem/progem.190517.json \
  gold_standards/unprocessed_validated/progem.190517.json

# Process all gold standards in `gold_standards/unprocessed_validated`
nano processing/process_and_convert_formats.sh # Edit Args
bash processing/process_and_convert_formats.sh
```