exports.handler = (event, context) => {
  context.succeed({
    samPath: "sam/path/to/sam"
  })
}