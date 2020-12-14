process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash, filterUnmapped } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')


exports.handler = async ({ s3bucket, filesarr, s3prefix }, context) => {

  const s3keys = filesarr
    .map((f, idx) => ({ [`sam${idx}`]: f.sam}))
    .reduce((acc, curr) => ({ ...acc, ...curr }), {})
    

  // fetch required files
  const localfiles = await fetch(s3bucket, s3keys, s3prefix)

  console.log(localfiles) // { sam0: '/tmp/NC_000913.3-hipA7.fasta-0.fasta.sam' }

  context.succeed({
    files: s3keys
  })

}