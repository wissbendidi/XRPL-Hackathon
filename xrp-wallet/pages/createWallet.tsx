import React, { useState } from 'react';
import { Client, ECDSA, Wallet } from 'xrpl';

const createWallet: React.FC = () => {
  const [wallet, setWallet] = useState<any>(null);
  const [accountInfo, setAccountInfo] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const createWallet = async () => {
    const client = new Client('wss://s.altnet.rippletest.net:51233');
    try {
      await client.connect();

      // Generate a new wallet
      const newWallet = Wallet.generate(ECDSA.secp256k1);
      setWallet(newWallet);
      console.log('Generated Wallet:', newWallet);
      setLoading(true);
      const response = await client.fundWallet(newWallet, { amount: "250" });
      console.log(response)
      setAccountInfo(response);
      console.log('Account Info:', response);
      await client.disconnect();
      const walletData = {
        address: newWallet.classicAddress,
        seed: newWallet.seed,
        publicKey: newWallet.publicKey,
        privateKey: newWallet.privateKey,
        balance: response.balance,
        email: 'taiaburbd@gmail.com'
      };

      const apiUrl = 'http://localhost:5000/api/wallet'; // Adjust to your Flask API URL
      const res = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(walletData),
      });

      if (res.ok) {
        const data = await res.json();
        console.log('Wallet stored:', data);
      } 
    } catch (err) {
      // setError('Failed to create wallet or fetch account info.');
      console.error(err);
    }finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Create Wallet</h1>
      <button onClick={createWallet} style={{ padding: '10px 20px', fontSize: '16px' }}>
        Create Wallet
      </button>

      {wallet && (
        <div style={{ marginTop: '20px' }}>
          <h2>Wallet Details</h2>
          <p>Address: {wallet.classicAddress}</p>
          <p>Seed: {wallet.seed}</p>
          <p>Public Key: {wallet.publicKey}</p>
          <p>Private Key: {wallet.privateKey}</p>
        </div>
      )}
      {loading && <p>Loading balance...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {accountInfo && (
        <div style={{ marginTop: '20px' }}>
          <p>Balance: {accountInfo.balance}</p>
          {/* <pre>{JSON.stringify(accountInfo.balance, null, 2)}</pre> */}
          <p>Successfully create wallet</p>
        </div>
      )}

      {error && (
        <div style={{ marginTop: '20px', color: 'red' }}>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
};

export default createWallet;
