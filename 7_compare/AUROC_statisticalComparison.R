
### AUROC Violin plot

AUROC <- read.table("AUROC_table.txt", header = T, sep = "\t")
dim(AUROC)
AUROC

colnames(AUROC) <-  c("Organism", "Operon-mapper", "Rockhopper", "Operon Finder", "OperonSEQer", "OpDetect")

library(ggplot2)

AUROC_stack <- stack(AUROC[,2:6])
AUROC_stack[,"ind"] <- as.factor(AUROC_stack[,"ind"])
colnames(AUROC_stack) <- c("AUROC", "Method")

p <- ggplot(AUROC_stack, aes(x=Method, y=AUROC, color = Method)) + 
  geom_violin(trim=T, na.rm = TRUE)  + coord_cartesian(ylim = c(0, 1))
  
p + stat_summary(fun=median, geom="point", size=2, color="red", na.rm= T) + scale_color_brewer(palette="Dark2") + theme(legend.position="none") + geom_hline(yintercept = 0.5, linetype = 2)


#### Statistical analysis

#Get a table of rankings
rTablePerClassifier <- t((apply(AUROC[,2:6], 1, rank, ties.method = "max", na.last =FALSE)- 6) *-1)

row.names(rTablePerClassifier) <- AUROC$Organism
#Fix rank operon-mapper so that NAs have the same rank
rTablePerClassifier["C. elegans","Operon-mapper"] <- 4

### Friedman test
require("PMCMRplus")

friedman.test(rTablePerClassifier)


#Pair-wise post hoc tests
frdAllPairsNemenyiTest(y=rTablePerClassifier)

frdAllPairsMillerTest(y=rTablePerClassifier)

frdAllPairsSiegelTest(y=rTablePerClassifier)

quadeAllPairsTest(rTablePerClassifier)


######
# Generate CD plot
library("scmamp")
plotCD(rTablePerClassifier, alpha = 0.05)


### Document versions
sessionInfo()

#R version 4.4.2 (2024-10-31)
#Platform: aarch64-apple-darwin20
#Running under: macOS Ventura 13.7.4

#Matrix products: default
#BLAS:   /Library/Frameworks/R.framework/Versions/4.4-arm64/Resources/lib/libRblas.0.dylib 
#LAPACK: /Library/Frameworks/R.framework/Versions/4.4-arm64/Resources/lib/libRlapack.dylib;  LAPACK version 3.12.0

#attached base packages:
#[1] stats     graphics  grDevices utils     datasets  methods   base     

#other attached packages:
#[1] scmamp_0.3.2     PMCMRplus_1.9.12 ggplot2_3.5.1   

#loaded via a namespace (and not attached):
# [1] gtable_0.3.6        Rmpfr_1.0-0         dplyr_1.1.4         compiler_4.4.2     
# [5] crayon_1.5.3        tidyselect_1.2.1    Rcpp_1.0.14         stringr_1.5.1      
# [9] scales_1.3.0        multcompView_0.1-10 fastmap_1.2.0       R6_2.6.1           
#[13] plyr_1.8.9          kSamples_1.2-10     labeling_0.4.3      generics_0.1.3     
#[17] MASS_7.3-65         tibble_3.2.1        munsell_0.5.1       pillar_1.10.1      
#[21] RColorBrewer_1.1-3  SuppDists_1.1-9.8   rlang_1.1.5         stringi_1.8.4      
#[25] cachem_1.1.0        memoise_2.0.1       cli_3.6.4           withr_3.0.2        
#[29] magrittr_2.0.3      BWStest_0.2.3       grid_4.4.2          mvtnorm_1.3-3      
#[33] gmp_0.7-5           lifecycle_1.0.4     vctrs_0.6.5         glue_1.8.0         
#[37] farver_2.1.2        colorspace_2.1-1    reshape2_1.4.4      tools_4.4.2        
#[41] pkgconfig_2.0.3    






