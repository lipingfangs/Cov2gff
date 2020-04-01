# Covmonkey2gff
Covmonkey2gff pipeline for annotation of Sars-cov-2 genomic

#You can operate this pipeline rely on the software Blast and Genewise

#It will generate a Blastx .gff file (xxx.gff), 11.fa files of 11 gene nucleotide sequence of sars-cov-2 base on Blastx .gff file, 11 genewise
.gff of 11 genes and the corresponding protein sequence(.pep) and cdna sequence (_cdna.fa), a genral genewise. GFF annotation file.
example in index goin/

#Use instruction:
python <your indir> <your path of blastx> <your path of genewise>
example:  python monkey3.py goin /home/lfp/newCov/scriptgo/Cov2gff/bin /home/lfp/rice/soft/wise2.4.1/src/bin

#Only one file can be entered in a directory; Error report for repeated execution
