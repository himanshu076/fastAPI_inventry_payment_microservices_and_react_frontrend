import React, { useEffect, useState } from 'react'

const Orders = () => {
  const [id, setId] = useState('');
  const [quantity, setQuantity] = useState('');
  const [message, setMessage] = useState('Buy your favorite product');

  useEffect( () => {
    const fetchData = async () => {
      try {
        if (id) {
          const response = await fetch(`http://127.0.0.1:8000/products/${id}`)
          const content = await response.json();
          const price = parseFloat(content.price) * 1.2;
          setMessage(`Your product price is $${price}`);
        }
      } catch (e) {
        setMessage('Buy your favorite product');
      }
    }

    fetchData();
  }, [id]);

  const handelSubmit = async (e) => {
    e.preventDefault();
    debugger;
    await fetch('http://localhost:8001/orders', {
      method: 'POST',
      headres: {'Content-Type': 'application/json'},
      body: JSON.stringify({id, quantity})
    });

    setMessage('Thank you for your order!');
  }
  return (
    <div className='container'>
      <main>
        <div className='py-5 text-center'>
          <h2>Checkout form</h2>
          <p className='lead'>{message}</p>
        </div>

        <form onSubmit={handelSubmit}>
          <div className='row g-3'>
            <div className='col-sm-6'>
              <label className='form-label'>Product</label>
              <input className='form-control' onChange={(e) => setId(e.target.value)}/>
            </div>

            <div className='col-sm-6'>
              <label className='form-label'>Quantity</label>
              <input type='number' className='form-control' onChange={(e) => setQuantity(e.target.value)}/>
            </div>
          </div>
          <hr className='my-4'/>
          <button className='w-100 btn btn-primary btn-lg' type='submit'>Buy</button>
        </form>
      </main>
    </div>
  )
}

export default Orders