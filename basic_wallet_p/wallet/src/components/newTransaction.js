import React, { useState } from 'react';
import axios from "axios";
import '../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { InputGroup, FormControl, Button } from 'react-bootstrap';

// set base URL
const api = axios.create({
    baseURL: 'http://localhost:5000/',
  });

function NewTransaction() {
  const [newTransactions, setNewTransactions] = useState('');

  const newT = () => {
    api
      .post('/transaction/new')
      .then(
        res =>  setNewTransactions(res.data),
      )
      .catch(
        err => console.log(err)
      )
  }

  return (
    <div>
      <h3>New Transaction</h3>
      <form onSubmit={newT}>
        <InputGroup className="mb-3">
          <InputGroup.Prepend>
            <InputGroup.Text id="basic-addon1">Sender</InputGroup.Text>
          </InputGroup.Prepend>

          <FormControl
            placeholder="Enter Sender Information"
            aria-label="Sender"
            aria-describedby="basic-addon1"
            />
        </InputGroup>

        <InputGroup className="mb-3">
          <InputGroup.Prepend>
            <InputGroup.Text id="basic-addon1">Recipient</InputGroup.Text>
          </InputGroup.Prepend>

          <FormControl
            placeholder="Enter Recipient Information"
            aria-label="Recipient"
            aria-describedby="basic-addon1"
            />
        </InputGroup>

        <InputGroup className="mb-3">
          <InputGroup.Prepend>
            <InputGroup.Text>Amount</InputGroup.Text>
          </InputGroup.Prepend>
          <FormControl
            placeholder="Enter Amount"
            aria-label="Amount"
            />
        </InputGroup>
        <Button variant="outline-dark" size="sm" type="submit">Submit</Button>
      </form>
    </div>
  );
}

export default NewTransaction;