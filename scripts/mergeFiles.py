#!/usr/bin/python

import csv

fields = ['ENS_ID', 'GeneName', 'GTEx_NoSunExp_Skin_MEDIAN', 'GTEx_SunExp_Skin_MEDIAN', 'ProtAtl_GC_TPM_skin1_keratinocytes', 'ProtAtl_GC_TPM_skin1_melanocytes', 'ProtAtl_GC_TPM_skin1_fibroblasts', 'ProtAtl_GC_TPM_skin1_Langerhans', 'ProtAtl_GC_TPM_skin2_epidermalCells', 'Eczema_MEDIAN', 'Eczema_CTRL_MEDIAN']

d={}
with open ("./ProtAtl_data.csv", 'r') as inFile:
    for line in inFile:
        data = line.split(',')
        if data[0] != "Gene":
            if data[0] in d:
                if data[2] == "skin1":
                    if data[3] == "keratinocytes":
                        d[data[0]][4] = data[6][:-2]
                    elif data[3] == "melanocytes":
                        d[data[0]][5] = data[6][:-2]
                    elif data[3] == "fibroblasts":
                        d[data[0]][6] = data[6][:-2]
                    else:
                        d[data[0]][7] = data[6][:-2]
                else:
                    d[data[0]][8] = data[6][:-2]
            else: 
                if data[2] == "skin1":
                    if data[3] == "keratinocytes":
                        d[data[0]] = [data[1], 0, 0, 0, data[6][:-2], 0, 0, 0, 0, 0]
                    elif data[3] == "melanocytes":
                        d[data[0]] = [data[1], 0, 0, 0, 0, data[6][:-2], 0, 0, 0, 0]
                    elif data[3] == "fibroblasts":
                        d[data[0]] = [data[1], 0, 0, 0, 0, 0, data[6][:-2], 0, 0, 0]
                    else:
                        d[data[0]] = [data[1], 0, 0, 0, 0, 0, 0, data[6][:-2], 0, 0]
                else:
                    d[data[0]] = [data[1], 0, 0, 0, 0, 0, 0, 0, data[6][:-2], 0]

            
with open ("./GTEx_gene_count_Sun_MEDIAN.csv", 'r') as inFile:
    for line in inFile:
        data = line.split(',')
        if data[0] != "ENS_ID":
            if data[0] in d:
                d[data[0]][2] = data[2][:-1]
            else:
                d[data[0]] = [data[1], 0, 0, data[2][:-1], 0, 0, 0, 0, 0, 0]
    
with open ("./GTEx_gene_count_NoSun_MEDIAN.csv", 'r') as inFile:
    for line in inFile:
        data = line.split(',')
        if data[0] != "ENS_ID":
            if data[0] in d :
                d[data[0]][1] = data[2][:-1]
            else:
                d[data[0]] = [data[1], data[2][:-1], 0, 0, 0, 0, 0, 0, 0, 0]
                

with open ("./eczemaSkinData_MEDIAN.csv", 'r') as inFile:
    for line in inFile:
        data = line.split(',')
        if data[0] != "ENS_ID":
            if data[0] in d:
                d[data[0]][8] = data[2]
                d[data[0]][9] = data[3][:-1]
            else:
                d[data[0]] = [data[1], 0, 0, 0, 0, 0, 0, 0, data[2], data[3][:-1]]
            
with open ("./Skin_flatfile.tsv", 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerow(fields)
        for k in d:
            row = [k] + d[k]
            writer.writerow(row)
