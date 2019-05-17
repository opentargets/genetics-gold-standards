GWAS Gold Standards
===================

WORK IN PROGRESS

Repository for GWAS variant to gene gold standards

Draft schema:
- https://docs.google.com/document/d/1qVc1Th67nmDmQLFuvPXuek1OmR-10R4bp_kgK-cICYw/edit

### Set up environment

```
conda env create -n goldstandards --file environment.yaml
conda activate gold_standards
```

### Usage

```
# Convert between json and yaml
python utils/json_yaml_converter.py --input file.yaml --output file.json
python utils/json_yaml_converter.py --input file.json --output file.yaml

# Validate schema
python validation/gs_validator.py --input test.single.json --schema validation/schema.v1.json 

```
