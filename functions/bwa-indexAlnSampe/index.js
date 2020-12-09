process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')

exports.handler = async ({ s3bucket, s3files }, context) => {

  await fetch(s3bucket, s3files, '/tmp')
  execSync('cd /tmp; bwa index NC_000913.3-hipA7.fasta')
  execSync('cd /tmp; bwa aln NC_000913.3-hipA7.fasta hipa7_reads_R1.fastq > aln_sa1.sai')
  execSync('cd /tmp; bwa aln NC_000913.3-hipA7.fasta hipa7_reads_R2.fastq > aln_sa2.sai')
  execSync('cd /tmp; bwa sampe NC_000913.3-hipA7.fasta aln_sa1.sai aln_sa2.sai hipa7_reads_R1.fastq hipa7_reads_R2.fastq > NC_000913.3.sam')
  execSync('cd /tmp; samtools view -b -F 4 NC_000913.3.sam > NC_000913.3slim.sam')

  // store back slim sam
  await stash(
    [
      'NC_000913.3slim.sam'
    ],
    'jak-bwa-bucket2'
  )
}