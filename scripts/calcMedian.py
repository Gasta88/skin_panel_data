#!/usr/bin/python

import csv
import statistics

# handle GTEx no sun exposed file
 
fields = ['ENS_ID', 'GeneName', 'GTEx_NoSunExp_Skin_MEDIAN']
with open ("./GTEx_gene_count_NoSun.csv", 'r') as GTExfile:
    with open ("./GTEx_gene_count_NoSun_MEDIAN.csv", 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fields)
        for line in GTExfile:
            ens_id = line.split(',')[0]
            ens_id = ens_id.split('.')[0]
            gene_name = line.split(',')[1]
            gene_counts = line.split(',')[2:]
            if ens_id != "Name":
                gene_counts.sort()
                row=[ens_id, gene_name, str(statistics.median(list(map(int, gene_counts))))]
                writer.writerow(row)

# handle GTEx sun exposed file
            
fields=['ENS_ID', 'GeneName', 'GTEx_SunExp_Skin_MEDIAN']
with open ("./GTEx_gene_count_Sun.csv", 'r') as GTExfile:
    with open ("./GTEx_gene_count_Sun_MEDIAN.csv", 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fields)
        for line in GTExfile:
            ens_id = line.split(',')[0]
            ens_id = ens_id.split('.')[0]
            gene_name = line.split(',')[1]
            gene_counts = line.split(',')[2:]
            if ens_id != "Name":
                gene_counts.sort()
                row=[ens_id, gene_name, str(statistics.median(list(map(int,gene_counts))))]
                writer.writerow(row)

# handle eczema file

fields=['ENS_ID', 'GeneName', 'Median', 'Ctrl_Median']
with open ("./eczemaSkinData.txt", 'r') as EZfile:
    with open ("./eczemaSkinData_MEDIAN.csv", 'w',newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fields)
        for line in EZfile:
            ens_id = line.split('\t')[0]
            ens_id = ens_id.split('.')[0]
            gene_name = line.split('\t')[1]
            gene_counts_ctrl = line.split('\t')[2:11]
            gene_counts = line.split('\t')[12:]            
            if ens_id != "GeneID":
                gene_counts_ctrl.sort()
                gene_counts.sort()
                row=[ens_id, gene_name,str(statistics.median(list(map(int,gene_counts)))), str(statistics.median(list(map(int,gene_counts_ctrl))))]
                writer.writerow(row)