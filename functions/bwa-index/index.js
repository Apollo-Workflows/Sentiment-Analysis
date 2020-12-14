process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

exports.handler = async ({ s3bucket, s3splitkey, s3prefix }, context) => {

  // fetch required files
  const [refgenomesplitpath] = await fetch(s3bucket, [s3splitkey], '/tmp')

  const beforefpaths = fs.readdirSync('/tmp')
    .map(fn => path.join('/tmp', fn))

  const refgenomefilename = refgenomesplitpath.split('/').slice(-1)[0]

  // COMMAND
  execSync(`cd /tmp; bwa index ${refgenomefilename}`)

  const afterfpaths = fs.readdirSync('/tmp')
    .map(fn => path.join('/tmp', fn))
  
  // stash all new files with prefix
  const outkeys = await stash(
    afterfpaths 
      .filter(fn => beforefpaths.includes(fn) === false),
    s3bucket,
    s3prefix
  )

  context.succeed({
    s3bucket: s3bucket,
    s3keys: outkeys,
    s3prefix: s3prefix
  })
}