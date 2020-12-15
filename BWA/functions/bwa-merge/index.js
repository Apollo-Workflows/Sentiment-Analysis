process.env['PATH'] = process.env['PATH'] + ':' + process.env['LAMBDA_TASK_ROOT']
const { fetch, stash, filterUnmapped } = require('./utils.js')
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')


exports.handler = async ({ s3bucket, s3samkeys, s3prefix }, context) => {

  const s3keys = s3samkeys
    .map((k, idx) => ({ [`sam${idx}`]: k}))
    .reduce((acc, curr) => ({ ...acc, ...curr }), {})
    
  // fetch required files
  const localfiles = await fetch(s3bucket, s3keys, s3prefix)

  let retnamedfiles = { 'mergedsam': '/tmp/merged.sam' }

  // read first sam file and get its header
  const samheader = fs.readFileSync(Object.values(localfiles)[0], { encoding: 'utf-8'} )
    .split('\n')
    .filter(l => /^@/.test(l) === true)
    .join('\n')

  

  // write header
  fs.appendFileSync('/tmp/merged.sam', samheader, { encoding: 'utf-8' })
  fs.appendFileSync('/tmp/merged.sam', '\n', { encoding: 'utf-8' })
  
  // merge them
  // append other sam files' contents
  const localsampaths = Object.values(localfiles)

  for(let i = 0; i < localsampaths.length; i+=1 ) {
    const localsampath = localsampaths[i]
    const contents = fs.readFileSync(localsampath, { encoding: 'utf-8'})
      .split('\n')
      .filter(l => /^@/.test(l) === false)
      .join('\n')
    fs.appendFileSync('/tmp/merged.sam', contents, { encoding: 'utf-8'})
    // newline only between concats, not at the end
    if(i < localsampaths.length - 1) { 
      fs.appendFileSync('/tmp/merged.sam', '\n', { encoding: 'utf-8' })
    }
  }

  // stash merged sam file


  retnamedfiles = await stash(retnamedfiles, s3bucket, s3prefix)

  context.succeed({
    s3bucket: s3bucket,
    mergedsamkey: retnamedfiles['mergedsam'],
    s3prefix: s3prefix
  })

}