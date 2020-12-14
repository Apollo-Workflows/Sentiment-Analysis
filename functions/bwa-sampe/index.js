process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash, filterUnmapped } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

exports.handler = async ({ s3bucket, files, s3prefix }, context) => {

  // fetch required files
  const localfiles = await fetch(s3bucket, files, s3prefix)

  let retnamedfiles = {
    sam: `${localfiles['reference']}.sam`
  }

  execSync(`bwa sampe ${localfiles['reference']} ${localfiles['sai1']} ${localfiles['sai2']} ${localfiles['r1']}  ${localfiles['r2']} > ${retnamedfiles['sam']}`)
  await filterUnmapped(retnamedfiles['sam'], retnamedfiles['sam'])

  // stash sam file
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