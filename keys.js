const crypto = require('crypto')

const keys1 = crypto.randomBytes(32).toString('hex')

console.log(keys1)