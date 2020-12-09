exports.handler = (event, context) => {
  context.succeed({
    s3WorkingDir: '/bucket/path/to/wd/'
  })
}