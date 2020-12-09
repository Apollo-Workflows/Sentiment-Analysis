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

// function listS3(bucket, prefix) {
//   const params = {
//     Bucket: bucket,
//     Prefix: prefix
//   }
//   return s3.listObjects(params)
//     .promise()
//     .then(res => res.Contents.map(c => c.Key))
// }

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
      if(/\//.test(key) === true) {
        throw new Error("Cannot fetch files that aren't at the root of a bucket: " + key)
      }
      const content = await getS3(bucket, key)
      await fsp.writeFile(
        path.join(localdir, key),
        content
      )
      console.log(`Fetched ${key} to ${path.join(localdir, key)}`)
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
    })
  )
}


// // 1 level
// // flattens all in s3workingdir
// function withFiles(localWorkingDir, s3bucket, s3WorkingDir, callback) {
//   if(!s3WorkingDir || s3WorkingDir.slice(-1)[0] !== '/') {
//     throw new Error("withFiles: third argument (s3WorkingDir) must have trailing slash (/)")
//   }
//   listS3(s3bucket, s3WorkingDir)
//     .then(s3paths => {
//       console.log(s3paths)
//       return Promise.all(
//         s3paths.map(async s3path => {
//           const filecontent = await getS3(s3bucket, s3path)
//           const filename = s3path.split('/').slice(-1)[0]
//           if (filename) {
//             const wpath = path.join(localWorkingDir, filename)

//             await fsp.writeFile(
//               wpath,
//               filecontent,
//             )

//             console.log(`Fetched ${s3path} to ${wpath}`)
//           }
//         })
//       )
//     })
//     .then(() => {
//       return callback()
//     })
//     // stash all files back to s3
//     .then(async callbackres => {
//       const filenames = await fsp.readdir(localWorkingDir)
//       await Promise.all(
//         filenames.map(async filename => {
//           const filepath = path.join(localWorkingDir, filename)
//           const filecontent = await fsp.readFile(filepath)
//           await putS3(s3bucket, s3WorkingDir + '/' + filename, filecontent)
//           console.log(`Stored ${filepath} to ${s3WorkingDir + filename}`)
//         })
//       )

//       return callbackres
//     })
// }


module.exports = {
  getS3,
  putS3,
  fetch,
  stash
};
