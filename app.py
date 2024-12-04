from flask import Flask, request, jsonify, render_template
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
import os

app = Flask(__name__)

# Set Entrez email
Entrez.email = "your_email@example.com"  # Replace with your valid email

def fetch_transcript_info(transcript_id):
    """Fetch transcript information from Entrez."""
    try:
        # Search transcript in Entrez
        search_handle = Entrez.esearch(db="nucleotide", term=transcript_id)
        search_results = Entrez.read(search_handle)
        search_handle.close()

        if not search_results["IdList"]:
            return {"error": f"Transcript {transcript_id} not found in Entrez"}
        
        # Fetch transcript details
        transcript_id_entrez = search_results["IdList"][0]
        fetch_handle = Entrez.efetch(db="nucleotide", id=transcript_id_entrez, rettype="gb", retmode="text")
        record = SeqIO.read(fetch_handle, "genbank")
        fetch_handle.close()
        
        # Extract coding sequence (CDS) and gene name
        gene_name = None
        cds_location = None
        for feature in record.features:
            if feature.type == "CDS":
                cds_location = feature.location
                if "gene" in feature.qualifiers:
                    gene_name = feature.qualifiers["gene"][0]
                break
        
        return {
            "gene_name": gene_name,
            "sequence": str(record.seq),
            "cds_location": cds_location,
        }
    except Exception as e:
        return {"error": str(e)}

def calculate_amino_acid_change(sequence, cds_location, cdna_position, ref_allele=None, alt_allele=None):
    """Calculate the amino acid change based on the cDNA position."""
    try:
        if cds_location is None:
            return {"error": "CDS location not found in transcript"}

        # Map cDNA position to genomic position
        cdna_numeric = int(cdna_position.replace("c.", ""))
        coding_start = cds_location.start
        relative_position = coding_start + cdna_numeric - 1  # 0-based indexing

        # Simulate the nucleotide substitution
        mutated_sequence = sequence
        if ref_allele and alt_allele:
            mutated_sequence = (
                sequence[:relative_position] + alt_allele + sequence[relative_position + 1 :]
            )

        # Translate the original and mutated sequences to amino acids
        original_protein = Seq(sequence[cds_location.start : cds_location.end]).translate()
        mutated_protein = Seq(mutated_sequence[cds_location.start : cds_location.end]).translate()

        # Identify the change
        for i, (orig, mut) in enumerate(zip(original_protein, mutated_protein)):
            if orig != mut:
                return f"p.{orig}{i+1}{mut}"  # Example: p.Pro648Ser

        return "No change detected"
    except Exception as e:
        return str(e)

def map_cdna_to_genomic(transcript_id, cdna_position, genome_build, ref_allele=None, alt_allele=None):
    """Map cDNA position to genomic coordinates and determine amino acid change."""
    try:
        transcript_info = fetch_transcript_info(transcript_id)
        if "error" in transcript_info:
            return transcript_info

        # Extract relevant data
        gene_name = transcript_info.get("gene_name", "UnknownGene")
        sequence = transcript_info.get("sequence")
        cds_location = transcript_info.get("cds_location")
        
        # Calculate amino acid change
        amino_acid_change = calculate_amino_acid_change(sequence, cds_location, cdna_position, ref_allele, alt_allele)

        # Example mapping logic - Replace with actual logic
        chromosome = "1"  # Replace with actual chromosome
        genomic_position_37 = "10042688"  # Replace with actual position
        genomic_position_38 = "9982630"  # Replace with actual position
        variant_type = f"{ref_allele}>{alt_allele}" if ref_allele and alt_allele else "del"  # Optional variant info

        result = {
            "formatted_output": f"{gene_name} ({transcript_id}):{cdna_position} ({amino_acid_change}), Chr{chromosome}({genome_build}):g.{genomic_position_37}{variant_type}" if genome_build == "GRCh37" else f"{gene_name} ({transcript_id}):{cdna_position} ({amino_acid_change}), Chr{chromosome}({genome_build}):g.{genomic_position_38}{variant_type}",
        }
        return result
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/annotate', methods=['POST'])
def annotate():
    data = request.json
    transcript_id = data.get("transcript_id")
    cdna_position = data.get("cdna_position")
    genome_build = data.get("genome_build", "GRCh38")
    ref_allele = data.get("ref_allele", None)
    alt_allele = data.get("alt_allele", None)
    
    if not transcript_id or not cdna_position:
        return jsonify({"error": "Both transcript ID and cDNA position are required"})
    
    result = map_cdna_to_genomic(transcript_id, cdna_position, genome_build, ref_allele, alt_allele)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
