const HDWalletProvider = require('truffle-hdwallet-provider');
const fs = require('fs');
module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*"
    },
    cfkh5dcxconsortium: {
      network_id: "*",
      gas: 0,
      gasPrice: 0,
      provider: new HDWalletProvider(fs.readFileSync('d:\\codefundo\\dummy\\abhiram1.env', 'utf-8'), "https://cfkh5dcxblockchain.blockchain.azure.com:3200/u_gyXatBlahOZXaDopYlsjbt"),
      consortium_id: 1564685306103
    }
  },
  mocha: {},
  compilers: {
    solc: {
      version: "0.5.0"
    }
  }
};
