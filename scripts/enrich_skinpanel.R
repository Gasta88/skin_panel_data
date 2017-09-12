#get PFAM ids from ENS id in skin file

#source("https://bioconductor.org/biocLite.R")
#biocLite("biomaRt")
library(biomaRt)
library(data.table)

#listMarts()
ensembl<-useMart("ensembl")

#listDatasets(ensembl)
ensembl<-useDataset("hsapiens_gene_ensembl",mart=ensembl)
skindb<-fread('Z:/SkinPanel/Skin_flatfile.tsv')
res<-getBM(attributes=c("ensembl_gene_id","pfam"),values = skindb$ENS_ID,filters = 'ensembl_gene_id',mart=ensembl)

#PFAM aggregation

#biocLite("PFAM.db")
library(PFAM.db)
x<-PFAMDE
mapped_keys<-mappedkeys(x)
xx<-as.list(x[mapped_keys])
kinase_pfam<-xx[grep("(K|k)inase",xx)]
bromodomain_pfam<-xx[grep("(B|b)romodomain|(B|b)romo-domain|(B|b)romo domain",xx)]
kinase_df<-stack(kinase_pfam)
bromodomain_df<-stack(bromodomain_pfam)

resK<-merge(res,kinase_df,by.x="pfam",by.y="ind")
resK<-aggregate(values~ensembl_gene_id,resK,FUN=paste,collapse='|| ')

resB<-merge(res,bromodomain_df,by.x="pfam",by.y="ind")
resB<-aggregate(values~ensembl_gene_id,resB,FUN=paste,collapse='|| ')


skindb<-merge(skindb,resK,by.x="ENS_ID",by.y="ensembl_gene_id",all.x=TRUE)
colnames(skindb)[12]<-"kinases descr"
skindb<-merge(skindb,resB,by.x="ENS_ID",by.y="ensembl_gene_id",all.x=TRUE)
colnames(skindb)[13]<-"bromodomain descr"


#kinases curated list hasn't been updated since 2002
#add info from curated bromodomain list
curated_bromod_list<-fread('Z:/SkinPanel/BROMO_fl_cleaned.tsv')
resBc<-getBM(attributes=c("external_gene_name","ensembl_gene_id"),values = curated_bromod_list$gene_id,filters = 'external_gene_name',mart=ensembl)
colnames(res)[1]<-"curated_bromodomain_generef"
skindb<-merge(skindb,resBc,by.x="ENS_ID",by.y="ensembl_gene_id",all.x=TRUE)
colnames(skindb)[14]<-"curated bromodomain gene name"


#InterPro aggregation

resIP<-getBM(attributes=c("ensembl_gene_id","interpro","interpro_description"),values = skindb$ENS_ID,filters = 'ensembl_gene_id',mart=ensembl)
kinase_IP<-resIP[which(grepl("(K|k)inase",resIP$interpro_description)),]
kinase_IP<-aggregate(interpro_description~ensembl_gene_id,kinase_IP,FUN=paste,collapse='|| ')

bromodomain_IP<-resIP[which(grepl("(B|b)romodomain|(B|b)romo-domain|(B|b)romo domain",resIP$interpro_description)),]
bromodomain_IP<-aggregate(interpro_description~ensembl_gene_id,bromodomain_IP,FUN=paste,collapse='|| ')

skindb<-merge(skindb,kinase_IP,by.x="ENS_ID",by.y="ensembl_gene_id",all.x=TRUE)
colnames(skindb)[15]<-"InterPro kinases descr"
skindb<-merge(skindb,bromodomain_IP,by.x="ENS_ID",by.y="ensembl_gene_id",all.x=TRUE)
colnames(skindb)[16]<-"InterPro bromodomain descr"

write.table(skindb,file = "Z:/SkinPanel/Skin_flatfile_PFAM_enrich.tsv",sep="\t",quote=FALSE)