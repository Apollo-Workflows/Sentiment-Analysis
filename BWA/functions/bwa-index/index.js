process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

/*
  {
  "s3bucket": "jak-bwa-bucket",
  "s3splitkeys": [
    "344918/NC_000913.3-hipA7.fasta-0.fasta",
    "541209/NC_000913.3-hipA7.fasta-1.fasta",
    "114713/NC_000913.3-hipA7.fasta-2.fasta",
    "25995/NC_000913.3-hipA7.fasta-3.fasta"
  ],
  "files": {
    "reference": "input/NC_000913.3-hipA7.fasta",
    "r1": "input/reads/hipa7_reads_R1.fastq",
    "r2": "input/reads/hipa7_reads_R2.fastq"
  },
  "s3prefixes": [
    "344918/",
    "541209/",
    "114713/",
    "25995/"
  ]
}

*/
exports.handler = async ({ s3bucket, s3splitkey, files, s3prefix }, context) => {

  const _files = { reference: s3splitkey }

  // fetch reference split
  const localfiles = await fetch(s3bucket, _files)

  // COMMAND
  execSync(`bwa index ${localfiles['reference']}`)

  // compute created file paths 
  let retnamedfiles = ['amb', 'ann', 'bwt', 'pac', 'sa']
    .map(suffix => ({ [suffix]: `${localfiles['reference']}.${suffix}` }))
    .reduce((acc, curr) => ({
      ...acc,
      ...curr
    }), {})


  retnamedfiles = await stash(retnamedfiles, s3bucket, s3prefix)

  retnamedfiles = {
    ...files,
    ..._files,
    ...retnamedfiles
  }

  context.succeed({
    s3bucket: s3bucket,
    files: retnamedfiles,
    s3prefix: s3prefix
  })
}