process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

/*


{
  "s3bucket": "jak-bwa-bucket",
  "files": {
    "reference": "224093/NC_000913.3-hipA7.fasta-2.fasta",
    "r1": "input/reads/hipa7_reads_R1.fastq",
    "r2": "input/reads/hipa7_reads_R2.fastq",
    "amb": "224093/NC_000913.3-hipA7.fasta-2.fasta.amb",
    "ann": "224093/NC_000913.3-hipA7.fasta-2.fasta.ann",
    "bwt": "224093/NC_000913.3-hipA7.fasta-2.fasta.bwt",
    "pac": "224093/NC_000913.3-hipA7.fasta-2.fasta.pac",
    "sa": "224093/NC_000913.3-hipA7.fasta-2.fasta.sa"
  },
  "s3prefix": "224093/"
}

*/

exports.handler = async ({ s3bucket, files, s3prefix }, context) => {

  // fetch required files
  const localfiles = await fetch(s3bucket, files)

  const sai1 = '/tmp/aln_sa1.sai'
  const sai2 = '/tmp/aln_sa2.sai'

  execSync(`bwa aln ${localfiles['reference']} ${localfiles['r1']} > ${sai1}`)
  execSync(`bwa aln ${localfiles['reference']} ${localfiles['r2']} > ${sai2}`)

  const newfiles = {
    sai1: sai1,
    sai2: sai2
  }

  let retnamedfiles = await stash(newfiles, s3bucket, s3prefix)

   retnamedfiles = {
    ...files,
    ...retnamedfiles
  }


  context.succeed({
    s3bucket: s3bucket,
    files: retnamedfiles,
    s3prefix: s3prefix
  })
}