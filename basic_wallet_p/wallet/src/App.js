import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { Table } from 'react-bootstrap';
import NewTransaction from './components/newTransaction';

// set base URL
const api = axios.create({
  baseURL: 'http://localhost:5000/',
});

function App() {
  const [id, setId] = useState('');
  const [balance, setBalance] = useState('');
  const [chain, setChain] = useState([]);
  const [transactions, setTransactions] = useState([]);

  const viewChain = () => {
    api
      .get('/chain')
      .then(
        res => setChain(res.data.chain),
      )
      .catch(
        err => console.log(err)
      );
  };


  const newID = (e) => {
    setId(e.target.value);

    const allTransactions = chain.reduce((accumulator, block) => {
      return [...accumulator, ...block.transactions];
    }, []);

    const ourTransactions = allTransactions.filter(transaction =>
      transaction.recipient === e.target.value ||
      transaction.sender === e.target.value
    );

    setBalance(ourTransactions.reduce((total, transaction) => {
      const amount = transaction.recipient === e.target.value && transaction.amount || -transaction.amount;
      return total + amount;
    }, 0));

    setTransactions(ourTransactions);
  }

  useEffect(viewChain, []);


  return (
    <div className="App">
      <input placeholder= "New ID Here" value={id} onChange={newID} />
      <div className="balance">Current Balance: {balance}</div>
      <Table striped bordered hover size="sm">
        <thead>
          <tr>
            <th>Sender</th>
            <th>Recipient</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {
            transactions.map((transaction, index) => {
              return (
                <tr key={index}>
                  <td>{transaction.sender}</td>
                  <td>{transaction.recipient}</td>
                  <td>{transaction.amount}</td>
                </tr>
              )
            })
          }
        </tbody>
      </Table>
    </div>
  );
}

export default App;