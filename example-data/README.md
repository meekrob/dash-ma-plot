## Example expression data

This example dataset represents a table stored in MariaDB.  It is a subset of the data published in [Williams et al. 2023](https://pubmed.ncbi.nlm.nih.gov/37183501/).

## Format

A file of comma-separated values with log2fold change in expression, base mean, gene ID, and other values associated with the statistical tests performed in DESeq2.

## Size and composition

It is 8700 lines (including header). A random subsample of the non-significantly differentially expressed genes is included from the original to reduce the file size.

Significantly depleted, equivalent within a range of fold change (see publication), or differentially expressed, are labelled as depleted, equal, and enriched, respectively in the data table.

```
(dash-ma-plot) % gzip -dc subset.data-for-MA-plot-app.csv.gz | grep -c depleted
121
(dash-ma-plot) % gzip -dc subset.data-for-MA-plot-app.csv.gz | grep -c equal
2145
(dash-ma-plot) % gzip -dc subset.data-for-MA-plot-app.csv.gz | grep -c enriched
2086
```
