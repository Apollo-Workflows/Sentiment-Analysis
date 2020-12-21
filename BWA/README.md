
### BWA

#### Get the code

```
git clone https://github.com/ApolloCEC/workflows
cd workflows/BWA
```

#### Get input dataset

##### Escherichia Coli

Escherichia Coli is a gram-negative bacterium that can cause food poisoning. The Assembly used is ASM584v2.

Bucket | Keys
----|----
`jak-bwa-bucket` | `input/NC_000913.3-hipA7.fasta`
`jak-bwa-bucket` | `input/reads/hipa7_reads_R1.fastq`
`jak-bwa-bucket` | `input/reads/hipa7_reads_R2.fastq`

##### Trypanosoma brucei

Trypanosoma brucei is a single-cell organism that causes sleeping sickness in humans. The Assembly used is ASM244v1.

Bucket | Keys
----|----
`jak-bwa-bucket` | `t-brucei/ASM244v1.fasta`
`jak-bwa-bucket` | `t-brucei/reads/asm_reads_R1.fastq`
`jak-bwa-bucket` | `t-brucei/reads/asm_reads_R2.fastq`

---

Put one data set into a bucket of yours, ideally in the same region as the Lambdas will be in.
Update `input.json` with the bucket and keys of your DNA samples, and the desired parallelism:

```
{
  "s3bucket": "YOUR_BUCKET",
  "files": {
    "reference": "YOUR_KEY_OF_REFERENCE_GENOME.fasta",
    "r1": "YOUR_KEY_OF_reads_R1.fastq",
    "r2": "YOUR_KEY_OF_reads_R2.fastq"
  },
  "numSplits": 3
}
```


#### Deploy the Lambdas

The Lambdas are in `functions`.
You can run [`npx deply`](https://www.npmjs.com/package/deply) if you don't want to deploy them by hand. Just update `deploy.json` beforehand. 
Alternatively, deploy them by hand to Amazon.

#### Run the workflow


```
$ cd BWA
$ java -jar YOUR_PATH_TO_xAFCL.jar ./workflow.yaml ./input.json
```

