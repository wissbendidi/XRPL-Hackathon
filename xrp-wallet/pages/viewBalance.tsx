// pages/view-balance.tsx
import React, { useState } from 'react';
import { Client } from 'xrpl';

const ViewBalance: React.FC = () => {
  const [address, setAddress] = useState<string>('');
  const [balance, setBalance] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchBalance = async () => {
    setLoading(true);
    setError(null);
    setBalance(null);

    const client = new Client('wss://s.altnet.rippletest.net:51233'); // Testnet connection

    try {
      await client.connect();

      const response = await client.request({
        command: 'account_info',
        account: address,
        ledger_index: 'validated',
      });

      setBalance(response.result.account_data.Balance);
      await client.disconnect();
    } catch (err) {
      setError('Failed to retrieve balance. Please check the address.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>View XRP Wallet Balance</h1>
      <input
        type="text"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
        placeholder="Enter XRP Wallet Address"
        style={{ padding: '10px', width: '300px', marginRight: '10px' }}
      />
      <button onClick={fetchBalance} style={{ padding: '10px 20px', fontSize: '16px' }}>
        Check Balance
      </button>

      {loading && <p>Loading balance...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {balance && (
        <div style={{ marginTop: '20px' }}>
          <h2>Balance</h2>
          <p>{balance} drops</p> {/* 1 XRP = 1,000,000 drops */}
        </div>
      )}
    </div>
  );
};

export default ViewBalance;
