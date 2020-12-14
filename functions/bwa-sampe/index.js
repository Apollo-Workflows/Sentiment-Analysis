process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash, filterUnmapped  } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

exports.handler = async ({ s3bucket, s3prefix, s3files, s3splitkey, s3R1key, s3R2key, s3sai1key, s3sai2key  }, context) => {

  // fetch primary files
  const [
    refgenomesplitpath, 
    r1path, 
    r2path,
    sai1path,
    sai2path
  ] = await fetch(s3bucket, [
    s3splitkey,
    s3R1key,
    s3R2key,
    s3sai1key,
    s3sai2key
  ], '/tmp')

  console.log("made it so far")


  // fetch other files
  await fetch(s3bucket, s3files, '/tmp')


  const refgenomesplitname = refgenomesplitpath.split('/').slice(-1)[0]
  const r1name = r1path.split('/').slice(-1)[0]
  const r2name = r2path.split('/').slice(-1)[0]
  const sai1name = sai1path.split('/').slice(-1)[0]
  const sai2name = sai2path.split('/').slice(-1)[0]
  
  const beforefpaths = fs.readdirSync('/tmp')
    .map(fn => path.join('/tmp', fn))

  const samname = `${refgenomesplitname}.sam`
  // COMMAND
  execSync(`cd /tmp; bwa sampe ${refgenomesplitname} ${sai1name} ${sai2name} ${r1name}  ${r2name} > ${samname}`)

  // filter unmapped reads
  // overwrite file directly
  await filterUnmapped(`/tmp/${samname}`, `/tmp/${samname}`)
 
  const afterfpaths = fs.readdirSync('/tmp')
    .map(fn => path.join('/tmp', fn))
  
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