GWAS Gold Standards
===================

WORK IN PROGRESS

Repository for GWAS variant to gene gold standards

Draft schema:
- https://docs.google.com/document/d/1qVc1Th67nmDmQLFuvPXuek1OmR-10R4bp_kgK-cICYw/edit


## How to submit a new gold standard

Todo

- positions must be from gnomad

## Process new gold standards

The sections contains instructions for validating new gold standards and processing them

### Set up environment

```
conda env create -n goldstandards --file environment.yaml
conda activate gold_standards
```

### Other useful commands

```
# Convert between json and yaml
python utils/json_yaml_converter.py --input file.yaml --output file.json
python utils/json_yaml_converter.py --input file.json --output file.yaml

# Validate schema
python validation/validator.py --input test.single.json --schema validation/goldstandard_schema.v1.1.json
```
