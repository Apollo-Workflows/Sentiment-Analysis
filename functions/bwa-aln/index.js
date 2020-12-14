process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

exports.handler = async ({ s3bucket, s3files, s3splitkey, s3R1key, s3R2key, s3prefix }, context) => {

  // fetch primary files
  const [
    refgenomesplitpath, 
    r1path, 
    r2path
  ] = await fetch(s3bucket, [
    s3splitkey,
    s3R1key,
    s3R2key
  ], '/tmp')

  // fetch other files
  await fetch(s3bucket, s3files, '/tmp')

  const refgenomesplitname = refgenomesplitpath.split('/').slice(-1)[0]
  const r1name = r1path.split('/').slice(-1)[0]
  const r2name = r2path.split('/').slice(-1)[0]

  const beforefpaths = fs.readdirSync('/tmp')
    .map(fn => path.join('/tmp', fn))

    // TODO see if we can omit cd and just call bwa with paths, and this places in tmp
  // COMMAND
  execSync(`cd /tmp; bwa aln ${refgenomesplitname} ${r1name} > aln_sa1.sai`)
  execSync(`cd /tmp; bwa aln ${refgenomesplitname} ${r2name} > aln_sa2.sai`)

  const afterfpaths = fs.readdirSync('/tmp')
    .map(fn => path.join('/tmp', fn))
    
    console.log("Beforepaths:" + JSON.stringify(beforefpaths)) 
  
   console.log("AFterfpaths:" + JSON.stringify(afterfpaths)) 
  // stash all new files
  const outkeys = await stash(
    afterfpaths 
      .filter(fn => beforefpaths.includes(fn) === false),
    s3bucket,
    s3prefix
  )

  context.succeed({
    s3bucket: s3bucket,
    s3files: outkeys,
    s3prefix: s3prefix
  })
}