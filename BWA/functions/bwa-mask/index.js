process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash, split, putS3 } = require('./utils.js')
const { execSync } = require('child_process')
const fsp = require('fs').promises
const path = require('path')

exports.handler = async ({ s3bucket, files, numSplits }, context) => {
  // fetch required files                // notion of prefix does not exist before splitting
  const localfiles = await fetch(s3bucket, files)

  // split reference genome
  const splitpaths = await split(localfiles['reference'], numSplits)

  let retnamedfiles = {}

  const prefixes = [...Array(splitpaths.length)].map(() => `${Math.ceil(Math.random() * 1000000)}/`)

  // stash each with individual s3 prefix
  for (let i = 0; i < splitpaths.length; i += 1) {
    const prefix = prefixes[i]
    const retnamedfile = await stash({ [`reference${i}`]: splitpaths[i] }, s3bucket, prefix)
    retnamedfiles = { 
      ...retnamedfiles,
      ...retnamedfile
    }
  }

  const s3splitkeys = Object.values(retnamedfiles)

  context.succeed({
    s3bucket: s3bucket,
    s3splitkeys: s3splitkeys,
    files: files,
    s3prefixes: prefixes,
  })

}
