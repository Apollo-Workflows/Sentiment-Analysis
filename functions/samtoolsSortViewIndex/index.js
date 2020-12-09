exports.handler = (event, context) => {
  context.succeed({
    bamPath: "bam/path",
    bambaiPath: "bambai/path"
  })
}