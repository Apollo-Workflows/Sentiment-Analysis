# Workflows

AFCL Workflows from various domains

### Summary

name | description |  draft | functions | orchestration | validity checks | metrics 
--- | ---- | ----- | ----- | ---- | ---- | ----
BWA  | BWA is a common life sciences task of performing DNA read alignment | ✅ | ✅ | ✅ | | 

### BWA

#### Get the code

```
git clone https://github.com/ApolloCEC/workflows
cd BWA
```

#### Get the Ecoli samples

bucket | key
---|----
`jak-bwa-bucket` | `input/NC_000913.3-hipA7.fasta`
`jak-bwa-bucket` | `input/reads/hipa7_reads_R1.fastq`
`jak-bwa-bucket` | `input/reads/hipa7_reads_R2.fastq`

Put them on a bucket of yours, ideally in the same region as the Lambdas will be in.

#### Deploy the Lambdas

The Lambdas are in `functions`.

You can run [`npx deply`](https://www.npmjs.com/package/deply) if you don't want to deploy them by hand. Just update `deploy.json` beforehand. Requires NodeJS 12 or greater.

Alternatively, deploy them by hand to Amazon.

#### Run the workflow

The AFCL workflow (`workflow.yaml`) and input (`input.json`) are placed in `BWA`.
Update `input.json` with the bucket and keys of your DNA samples, and the desired Parallelism (`numSplits`).

Then you can run: 

```
$ cd BWA
$ java -jar YOUR_PATH_TO_xAFCL.jar ./workflow.yaml ./input.json
```

---

### Pool

name | description | notes | expected t
---- | ---- | ---- | -----
Seismic | Seismic signal-processing | Jakob: From `https://github.com/rosafilgueira/dispel4py_workflows`. Fairly convoluted. | 1.5 weeks