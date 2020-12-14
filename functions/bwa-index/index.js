process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

/*
  files = {
    reference: "some/s3/key"
  }
*/
exports.handler = async ({ s3bucket, files, s3prefix }, context) => {

  // fetch required files
  const localfiles = await fetch(s3bucket, files, s3prefix)

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
    ...retnamedfiles
  }

  context.succeed({
    s3bucket: s3bucket,
    files: retnamedfiles,
    s3prefix: s3prefix
  })
}