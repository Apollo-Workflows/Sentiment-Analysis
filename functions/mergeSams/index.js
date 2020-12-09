exports.handler = (event, context) => {
  context.succeed({
    mergedSamPath: "/merged/sam/path"
  })
}