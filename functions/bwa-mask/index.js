process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash, split, putS3 } = require('./utils.js')
const { execSync } = require('child_process')
const fsp = require('fs').promises
const path = require('path')

/*
  Expects inputs/reference.fasta, reads/r1.fastq, r2.fastq
*/

/* 
  files: {
    reference: s3key
  }
*/
exports.handler = async ({ s3bucket, files, numSplits }, context) => {

  // fetch required files
  // TODO: fetch: return
  const localfiles = await fetch(s3bucket, files,)

  // create splits of reference genome
  const splitpaths = await split(refgenomepath, numSplits)
  const prefixes = [...Array(numSplits)].map(() => `${Math.ceil(Math.random() * 1000000)}/`)
 
  const s3splitkeys = await Promise.all(
    splitpaths.map(async (splp,idx) => {
      const prefix = prefixes[idx] // trailing slash for s3 foldering
      const name = splp.split('/').slice(-1)[0]
      const key = prefix + name
      const contents = await fsp.readFile(splp)
      await putS3(s3bucket, key, contents)
      return key
    })
  )

  context.succeed({
    s3bucket: s3bucket,
    s3splitkeys: s3splitkeys,
    s3prefixes: prefixes
  })
}
