# Transcript-ChromosomeNumber

This is a web-based application for genomic annotation. It allows users to input a transcript ID, cDNA position, and optionally, reference and alternate alleles, to determine the chromosomal location and amino acid changes. The application supports both GRCh37 and GRCh38 genome builds.

## Features

- **Transcript Annotation**: Fetches transcript and gene information using NCBI Entrez.
- **cDNA to Genomic Mapping**: Maps cDNA positions to genomic coordinates.
- **Amino Acid Change Calculation**: Dynamically determines amino acid changes based on mutations.
- **Genome Build Support**: Allows users to select between GRCh37 and GRCh38.
- **Optional Allele Inputs**: Supports optional input for reference and alternate alleles.
- **Modern UI**: A clean and user-friendly web interface built with Bootstrap.

## Example Outputs

### Input:
- **Transcript ID**: `NM_001297778.1`
- **cDNA Position**: `c.769`
- **Genome Build**: `GRCh37`
- **Reference Allele**: `G` (optional)
- **Alternate Allele**: `A` (optional)

### Output:
SETD1A (NM_014712.3):c.769 (p.Glu257Lys), Chr1(GRCh37):g.10042688G>A


## Tech Stack

- **Backend**: Python, Flask, Biopython
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **APIs**: NCBI Entrez

## Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- Pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jaannawaz/Transcript-ChromosomeNo.git
   cd Transcript-ChromosomeNo

pip install -r requirements.txt

python app.py


http://127.0.0.1:5000
