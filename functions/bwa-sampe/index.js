process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash, filterUnmapped  } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

exports.handler = async ({ s3bucket, s3files }, context) => {

  // fetch required files
  await fetch(s3bucket, s3files, '/tmp')

  const beforefpaths = fs.readdirSync('/tmp')
    .map(fn => path.join('/tmp', fn))

  // COMMAND
  execSync('cd /tmp; bwa sampe NC_000913.3-hipA7.fasta aln_sa1.sai aln_sa2.sai hipa7_reads_R1.fastq hipa7_reads_R2.fastq > NC_000913.3.sam')
  // filter unmapped reads
  await filterUnmapped('/tmp/NC_000913.3.sam', '/tmp/NC_000913.3filtered.sam')
  fs.unlinkSync('/tmp/NC_000913.3.sam')

  const afterfpaths = fs.readdirSync('/tmp')
    .map(fn => path.join('/tmp', fn))
  
  // stash all new files
  const outkeys = await stash(
    afterfpaths 
      .filter(fn => beforefpaths.includes(fn) === false),
    s3bucket
  )

  context.succeed({
    s3bucket: s3bucket,
    s3files: outkeys
  })
}