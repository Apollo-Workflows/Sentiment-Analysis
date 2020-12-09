exports.handler = ({ referenceGenomeArn, numSplits }, context) => {
  context.succeed({
    splitArns: [...Array(numSplits).keys()].map(i => `refsplitpath${i}`)
  })
}