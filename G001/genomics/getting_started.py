from Bio import SeqIO
from Bio import Align

# parse genbank file from S. peucetius ATCC27952 (wild-type)
record_WT = SeqIO.read("WT.gbk", "genbank")

# parse genbank file from G001 (industrial producer)
record_G001 = [0, 0]
count = 0
for seq_record in SeqIO.parse("G001.gbk", "genbank"):
    record_G001[count] = seq_record
    count += 1

record_G001_1 = record_G001[0]
record_G001_2 = record_G001[1]

# Sequencing alignment
seq1_record = SeqIO.read("WT_DXR.fasta", "fasta")
seq2_record = SeqIO.read("G001_DXR.fasta", "fasta")

aligner = Align.PairwiseAligner()

seq1 = seq1_record.seq
seq2 = seq2_record.seq

alignments = aligner.align(seq1, seq2)

print(alignments[0])
print(len(alignments[0]))
# for alignment in alignments:
#     print(alignment)
