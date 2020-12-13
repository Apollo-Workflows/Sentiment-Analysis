process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

exports.handler = async ({ s3bucket, s3files }, context) => {

  // fetch required files
  await fetch(s3bucket, s3files, '/tmp')

  const beforefpaths = fs.readdirSync('/tmp')
    .map(fn => path.join('/tmp', fn))

  // COMMAND
  execSync('cd /tmp; bwa index NC_000913.3-hipA7.fasta')

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