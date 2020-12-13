const aws = require('aws-sdk');
const fsp = require('fs').promises
const path = require('path')
const os = require('os')

const s3 = new aws.S3();

function getS3(bucket, key) {
  const params = {
    Bucket: bucket,
    Key: key,
  };
  return s3.getObject(params)
    .promise()
    .then((s3obj) => s3obj.Body && Buffer.from(s3obj.Body));
}

function putS3(bucket, key, data) {
  const params = {
    Bucket: bucket,
    Key: key,
    Body: data,
  };
  return s3.putObject(params)
    .promise();
}

const extractBucket = (filearn) => filearn.match(/(?!^(\d{1,3}\.){3}\d{1,3}$)(^[a-z0-9]([a-z0-9-]*(\.[a-z0-9])?)*$)/)

function fetch(bucket, keys, localdir) {
  return Promise.all(
    keys.map(async key => {
      const content = await getS3(bucket, key)
      const filename = key.split('/').slice(-1)[0]
      await fsp.writeFile(
        path.join(localdir, filename),
        content
      )
      console.log(`Fetched ${key} to ${path.join(localdir, filename)}`)
    })
  )
}

function stash(filepaths, bucket) {
  return Promise.all(
    filepaths.map(async filepath => {
      const content = await fsp.readFile(filepath)
      const filename = path.basename(filepath)
      await putS3(bucket, filename, content)
      console.log(`Stashed ${filename} to ${bucket}`)
      return filename
    })
  )
}

async function filterUnmapped(infilepath, outfilepath) {
  const samcontent = await fsp.readFile(infilepath, { encoding: 'utf-8' })

  const filteredsamcontent = samcontent
    .split('\n')
    .filter((l, idx) => {
      let els = l.split('\t') // sam columns are tab-delimited
      // Discard lines that have a zero in the fourth column
      // (means that the read could not be mapped, and thus is not interesting to us)
      if (
        els.length >= 4
        && els[3] != null
        && isNaN(parseInt(els[3])) === false
        && parseInt(els[3]) === 0
      ) {
        return false
      }
      return true
    })
    .join('\n')

  console.log(infilepath + " = filtered unmapped reads => " + outfilepath)
  console.log(samcontent.split('\n').length + " lines => " + filteredsamcontent.split('\n').length + " lines")

  await fsp.writeFile(outfilepath, filteredsamcontent, { encoding: 'utf-8' })
}


/**
 * @returns {string[]} paths of generated splits
 * @param {*} infastapath 
 * @param {*} n 
 */
async function split(infastapath, n) {
  let fasta = await fsp.readFile(infastapath, { encoding: 'utf-8' })

  function mask(lines) {
    return lines.map(l => {
      if (/>/.test(l) === true) {
        return l
      }
      else {
        return l.replace(/./g, 'N')
      }
    })
  }

  let ls = fasta
    .split('\n')

  let outpaths = []

  for (let i = 0; i < n; i += 1) {
    // our window that isn't masked with N
    const startl = Math.floor((ls.length * i) / n)
    const endl = Math.floor((ls.length * (i + 1)) / n)

    const maskedExcept = [
      ...mask(ls.slice(0, startl)),
      ...ls.slice(startl, endl),
      ...mask(ls.slice(endl))
    ].join('\n')

    const outpath = path.join(path.dirname(infastapath), `${path.basename(infastapath)}-${i}.fasta`) // place splits alongside with input fasta

    await fsp.writeFile( // place splits alongside with input fasta
      outpath,
      maskedExcept,
      { encoding: 'utf-8' }
    )

    outpaths.push(outpath)
  }

  return outpaths


}


module.exports = {
  getS3,
  putS3,
  fetch,
  stash,
  filterUnmapped,
  split
};



