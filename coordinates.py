import os

chromosomes = ['chr10.2bit', 'chr11.2bit', 'chr12.2bit', 'chr1.2bit', 'chr13.2bit', 'chr14.2bit', 'chr15.2bit',
               'chr16.2bit', 'chr17.2bit', 'chr18.2bit', 'chr19.2bit', 'chr20.2bit', 'chr21.2bit', 'chr22.2bit',
               'chr2.2bit', 'chr3.2bit', 'chr4.2bit', 'chr5.2bit', 'chr6.2bit', 'chr7.2bit', 'chr8.2bit', 'chr9.2bit',
               'chrX.2bit', 'chrY.2bit']

for chr in chromosomes:
    os.system("/opt/kentools/isPcr -out=psl /media/genomicdata/ucsc_hg19_by_chr/2bit_chr/%s primer.txt %s.tmp.psl" %
              \
              (chr, chr[:-5]))

    chrfile = "%s.tmp.psl" % chr[:-5]

    if os.path.getsize(chrfile) != 0:
        os.system("/opt/kentools/pslToBed %s.tmp.psl %s.tmp.bed" % (chr[:-5], chr[:-5]))
    else:
        os.system("rm %s.tmp.psl" % chr[:-5])
