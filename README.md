GWAS Gold Standards
===================

WORK IN PROGRESS

Repository for GWAS variant to gene gold standards.

`gold_standards/processed` contains the latest set of gold standards in a variety of formats. Note, the TSV file has arrays concatenated together using '|' as a seporator.

Todo:
- Update readme with details of the gold standards contained in the repository
- Scripts to produce descriptive statistics for each gold standard set
- Derive new gold standards based on drug and rare disease data

### Gold standard schema

The gold standard schema consists of 5 sections:

- `sentinel_variant`: Information about the sentinel/lead GWAS variant
- `trait_info`: Information about the GWAS trait or disease
- `association_info`: Evidence linking the sentinel variant to the trait through GWAS
- `gold_standard_info`: Evidence linking the GWAS signal (variant, trait, association) to a gene
- `metadata`: Additional information

#### Example schema in yaml format

```yaml
# Sentinel variant information, alleles must match gnomAD
sentinel_variant:
  # Locus chrom and position on either GRCh37 or GRCh38 are required
  locus_GRCh37:
    chromosome: '16'
    position: 81264597
  locus_GRCh38:
    chromosome: '16'
    position: 81230992
  # Alleles are required
  alleles:
    alternative: G
    reference: T
  # rsID is optional
  rsid: rs6564851

# Trait/disease information
trait_info:
  # List of ontology codes for the trait, should be EFO if possible
  ontology:
  - HMDB0000561
  # Trait reported by the author and standardised trait name (from ontology)
  reported_trait_name: Carotenoid and tocopherol levels (beta-carotene)
  standard_trait_name: B-Carotene

# Association evidence
association_info:
  # List of ancestries in which the association was detected
  ancestry:
  - EUR
  # GWAS Catalog study ID if available
  gwas_catalog_id: GCST000324
  # Open Targets Genetics study ID if available
  otg_id: GCST000324
  # Negative log p-value (optional)
  neg_log_pval: 23.699
  # Pubmed ID or doi
  pubmed_id: '19185284'
  doi: '10.1101/592238'

# Gold standard evidence
gold_standard_info:
  # Ensembl gene ID
  gene_id: ENSG00000135697
  # List of evidences support link with gene
  evidence:
  # Item 1 in list
  - class: expert curated # See below for evidence classes
    # Confidence should be "High" or "Low"
    confidence: High
    # Evidence curator
    curated_by: EF
    # Description of evidence
    description: BCO1 (previously referred to as BCMO1) encodes beta-carotene oxygenase
      1 which uses a molecule of oxygen to produce two molecules of retinol from
      beta-carotene.  Enzyme deficiency results in accumulation of beta-carotene.
    # Pubmed ID or source
    pubmed_id: '11401432'
    source: ChEMBL drug data

# Metadata
metadata:
  date_added: '2019-05-17'
  reviewed_by: EM
  # Name given to the group of gold standards
  set_label: ProGeM
  submitted_by: EF
  # Additional tags that may be useful for analysis
  tags:
  - metabolite
  - mQTL
  comments: 'No comments'
```

#### Possible evidence classes

1. "expert curated": association curated by an expert
2. "functional experimental": association inferred from experimental alteration (intervention), e.g. CRISPR editing
3. "functional observational": association inferred from observational evidence, e.g. correlation with quantitative trait such as eQTL or pQTL
4. "drug": association inferred from known drug target-indication pairs

### How to submit a new gold standard

1. Download the template yaml from [here](gold_standards/templates/single_gold_standard.v1.2.yaml) if submitting a single gold standard or [here](gold_standards/templates/multi_gold_standard.v1.2.yaml) if submitting multiple at once
2. Fill in the yaml file
3. [Create a new issue](https://github.com/opentargets/genetics-gold-standards/issues) including the completed yaml file

We will then review the submission and add it to the repository.

### Validate and process new gold standards

The sections contains instructions for validating and processing newly submitted gold standards. Submitters are not required to validate and process new gold stnadards.

```bash
# Set up environment
conda env create -n goldstandards --file environment.yaml
conda activate gold_standards

# Validate against schema (input can be json or yaml)
python validation/validator.py \
  --input temp/progem/progem.190517.yaml \
  --schema validation/goldstandard_schema.v1.4.json

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