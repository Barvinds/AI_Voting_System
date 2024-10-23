const express = require('express');
const app = express();
const Web3 = require('web3');

// Connect to Ethereum node
const web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));

// Contract ABI (you need to replace this with your actual ABI)
const contractABI = [...]; // Your contract ABI

// Contract address (you need to replace this with your actual contract address)
const contractAddress = '0x123...'; 

// Get contract instance
const contractInstance = new web3.eth.Contract(contractABI, contractAddress);

// Endpoint to handle vote increment
app.post('/vote', async (req, res) => {
    try {
        // Increment vote count in the blockchain
        await contractInstance.methods.incrementVote().send({ from: '0xsenderAddress' });
        res.json({ success: true, message: 'Vote counted successfully.' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ success: false, message: 'Failed to count vote.' });
    }
});

// Start the server
const port = 3000;
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
