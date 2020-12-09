exports.handler = ({ s3WorkingDir }, context) => {
  context.succeed({
    s3WorkingDir: s3WorkingDir
  })
}