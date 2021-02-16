const path = require('path')
const fs = require('fs')

console.log("This script compares workflow outputs, to ensure the workflow produces identical results irrespective of Parallelization.")

if(argv.length !== 4) {
  console.log("Usage: node index.js PATH_TO_FIRST_WORKFLOW_OUTPUT PATH_TO_SECOND_WORKFLOW_OUTPUT")
  process.exit(1)
}

const p1 = path.join(process.cwd(), argv[3])
const p2 = path.join(process.cwd(), argv[4])

const c1 = JSON.parse(fs.readFileSync(p1, { encoding: 'utf-8'}))
const c2 = JSON.parse(fs.readFileSync(p2, { encoding: 'utf-8'}))

// See https://stackoverflow.com/a/16788517
function objectEquals(x, y) {
  if (x === null || x === undefined || y === null || y === undefined) { return x === y; }
  // after this just checking type of one would be enough
  if (x.constructor !== y.constructor) { return false; }
  // if they are functions, they should exactly refer to same one (because of closures)
  if (x instanceof Function) { return x === y; }
  // if they are regexps, they should exactly refer to same one (it is hard to better equality check on current ES)
  if (x instanceof RegExp) { return x === y; }
  if (x === y || x.valueOf() === y.valueOf()) { return true; }
  if (Array.isArray(x) && x.length !== y.length) { return false; }

  // if they are dates, they must had equal valueOf
  if (x instanceof Date) { return false; }

  // if they are strictly equal, they both need to be object at least
  if (!(x instanceof Object)) { return false; }
  if (!(y instanceof Object)) { return false; }

  // recursive object equality check
  var p = Object.keys(x);
  return Object.keys(y).every(function (i) { return p.indexOf(i) !== -1; }) &&
      p.every(function (i) { return objectEquals(x[i], y[i]); });
}

const eq = objectEquals(c1, c2)
if(eq === true) {
  console.log(`Files ${argv[3]} and ${argv[4]} contain identical JSON.`)
} else {
  console.log(`Files ${argv[3]} and ${argv[4]} do not contain identical JSON`)
}