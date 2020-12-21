
### BWA

#### Get the code

```
git clone https://github.com/ApolloCEC/workflows
cd workflows/BWA
```

#### Get the Ecoli samples

bucket | key
---|----
`jak-bwa-bucket` | `input/NC_000913.3-hipA7.fasta`
`jak-bwa-bucket` | `input/reads/hipa7_reads_R1.fastq`
`jak-bwa-bucket` | `input/reads/hipa7_reads_R2.fastq`

Put them on a bucket of yours, ideally in the same region as the Lambdas will be in.
Update `input.json` with the bucket and keys of your DNA samples, and the desired parallelism:

```
{
  "s3bucket": "YOUR_BUCKET",
  "files": {
    "reference": "YOUR_KEY_OF_NC_000913.3-hipA7.fasta",
    "r1": "YOUR_KEY_OF_hipa7_reads_R1.fastq",
    "r2": "YOUR_KEY_OF_hipa7_reads_R2.fastq"
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

