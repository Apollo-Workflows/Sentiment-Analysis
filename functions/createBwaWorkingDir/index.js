exports.handler = (event, context) => {
  context.succeed({
    s3bucket: 'jak-bwa-bucket2',
    s3files: [
      'filepath1',
      'filepath2',
      'filepath3',
    ]
  })
}