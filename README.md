# skin_panel_data
This page is for documenting the process that I've used to prepare some data for a team inside the Drug Discovery Unit here at the University of Dundee.
While screening potential compounds to take forward for further development, along with testing for activity against a target, the compound is also tested against a known panel of problematic targets to avoid toxic effects. 
Many panels exist, but not one for gene express mainly in skin. The DGEM team needs some data mining help to start the search for suitable skin panel.

Raw Data
========
I started with a list of genes from the [Human Protein Atlas](http://www.proteinatlas.org) project, considering only skin (tagged as *skin1* and *skin2*).
The data is based on immunochemistry experiments using tissue micro arrays.
The comma-separated file includes:
* Ensembl gene id ("Gene")
* Tissue name ("Tissue")
* Annotated cell type ("Cell Type")
* Expression Value ("Level")
* Gene [reliability](http://www.proteinatlas.org/about/assays+annotation) of expression value ("Reliability")

The data is based on The Human Protein Atlas version 16.1 and Ensembl 83.38.

Data example:


|Gene             |Gene name  |Tissue   |Cell Type        |Level  |Reliability  |Value(TPM)|
|-----------------|-----------|---------|-----------------|-------|-------------|----------|
|ENSG00000000003  |TSPAN6     |skin1    |keratinocytes    |High   |Approved     |7.9       |
|ENSG00000000419  |DPM1       |skin1    |melanocytes      |High   |Approved     |40.6      |
|ENSG00000001461  |NIPAL3     |skin2    |epidermal cells  |High   |Approved     |15.3      |


Another repository used was [GTEx](https://gtexportal.org/home/). According to the documentation on the portal, the data is riginated via RNA-seq using the Illumia TrueSeq library constructon tool. 
This is a non-strand specific polyA+ selected library. The sequencing produced 76-bp paired ends reads.
Alignment to the HG19 human genome was performed using TopHatv1.4.1 assisted by the GENECODE v19 transcriptome definition. In a post-processing step, unaligned reads are reintroduced into the BAM file.
The final BAM file contains aligned and unaligned reads, the former marked as duplicates. It should be noted that TopHat produces multiple mappings for some reads, but in post-processing one read is flagged 
as the primary alignment.
The RPKM values that are downloadable have not been normalized or corrected for any covariates.
The entire set has been divided via [Pipeline Pilot](http://accelrys.com/products/collaborative-science/biovia-pipeline-pilot/) into two CSV files:
* one for sun exposed skin (*GTEx_gene_count_Sun*)
* one for non sun exposed skin (*GTEx_gene_count_noSun*)

Data example: 


|Name             |Description  |GTEX-111CU-1926-SM-5GZYZ  |GTEX-111FC-0126-SM-5N9DL |GTEX-111VG-2426-SM-5GZXD |...|
|-----------------|-------------|--------------------------|-------------------------|-------------------------|---|
|ENSG00000223972.4|DDX11L1      |0                         |0                        |0                        |...|  
|ENSG00000227232.4|WASH7P       |1650                      |1772                     |690                      |...|
|ENSG00000243485.2|MIR1302-11   |0                         |0                        |1                        |...|


The files have the following dimensions:

**GTEx_gene_count_Sun:** 49708 rows x 359 columns.

**GTEx_gene_count_NoSun:** 48844 rows x 252 columns.

Moreover, Chris C. provided a datasets of patients effected by eczema [link](http://europepmc.org/abstract/MED/24880632). 

Data Manipulation and Enrichment
================================

After the data has been downloaded, the MEDIAN has been calculate in all files beside the one generate for Protein Atlas.(ref to `scripts/calcMedian.py`). 

Later, I merged all the files into one tidy table with the following headers (ref to `scripts/mergeFiles.py`):

**'ENS_ID','GeneName','GTEx_NoSunExp_Skin_MEDIAN','GTEx_SunExp_Skin_MEDIAN','ProtAtl_GC_TPM_skin1_keratinocytes','ProtAtl_GC_TPM_skin1_melanocytes','ProtAtl_GC_TPM_skin1_fibroblasts','ProtAtl_GC_TPM_skin1_Langerhans','ProtAtl_GC_TPM_skin2_epidermalCells','Eczema_MEDIAN','Eczema_CTRL_MEDIAN'**


The final result looks like so:


|ENS_ID    |GeneName    |GTEx_NoSunExp_Skin_MEDIAN    |GTEx_SunExp_Skin_MEDIAN    |ProtAtl_GC_TPM    |Eczema_MEDIAN    |Eczema_CTRL_MEDIAN    |Tissue    |Cell_Type|
|----------|------------|-----------------------------|---------------------------|------------------|-----------------|----------------------|----------|---------|
|ENSG00000100890    |KIAA0391    |1274.5    |1266    |18.    |102.5    |179    |skin 2    |epidermal cells|
|ENSG00000205857    |NANOGNB    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000254644    |RP11-5A11.2    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000253764    |RP11-439C15.4    |6.0    |6    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000183486    |MX2    |565.5    |766    |0    |1169.0    |3141    |skin sun exposed    |NA|
|ENSG00000243593    |RP11-500K19.1    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000237439    |RP1-127L4.10    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000142513    |ACPT    |24.5    |19    |0    |0.0    |0    |skin sun exposed    |NA|
|ENSG00000261020    |RP11-744K17.1    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000185133    |INPP5J    |409.0    |469    |0    |7.0    |20    |skin sun exposed    |NA|
|ENSG00000164530    |PI16    |1319.0    |2484    |0    |1912.0    |3142    |skin sun exposed    |NA|
|ENSG00000112212    |TSPO2    |5.0    |6    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000259135    |RP11-671J11.4    |1.0    |1    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000221201    |AL031655.1    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000253934    |MRPL49P2    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000095981    |KCNK16    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000013375    |PGM3    |1128.0    |1140    |0    |39.0    |93    |skin sun exposed    |NA|
|ENSG00000244280    |ECEL1P2    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000215606    |KRT18P35    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000170950    |PGK2    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000066422    |ZBTB11    |1646.0    |1507    |0    |127.5    |217    |skin sun exposed    |NA|
|ENSG00000135220    |UGT2A3    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000230219    |FAM92A1P2    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|
|ENSG00000254083    |RP11-452N4.1    |0.0    |0    |0    |0.0    |0    |skin sun exposed    |NA|
|ENSG00000258665    |AC068831.12    |0.0    |0    |0    |0    |0    |skin sun exposed    |NA|

Under request, the datasets was enriched with information coming from [InterPro](https://www.ebi.ac.uk/interpro/), [PFAM](http://pfam.xfam.org) and a manually annotated list for bromodomains (ref to `scripts/enrich_skinpanel.R`).

Further Data Manipulation
=========================

The gene data has been ranked. This approach, even if feasible, didn't contribute to increase any information for the panel.
Personally, I think that the reason would be the presence of different repository. Each one of them collect samples under different conditions, making difficult a direct comparison. The calculation of a MEDIAN RANK does not carry more information than before.

Either way, the process is described in the .Rmd file associated in this repository.

