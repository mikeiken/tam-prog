import React, { useState, useEffect } from 'react';
import Header from '../header/Header';
import Card from '../card/Card';
import AddItemButton from '../add-item/AddItemButton';
import './style.css';
import axios from 'axios';

export default function MainPage() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await axios.get('http://homelab.kerasi.ru/api/v1/plant/?format=json');
                setData(response.data);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };
 
        fetchData();

        return () => {
            console.log(data);
        };
    }, []);

    return (
        <div className='max-height'>
            <Header />
            <div className='h-container'>
                <div className='box1'>

                </div>
                <div className='box2'>
                    {loading ? (
                        <div className='centered-spinner'>
                            <div className="spinner"></div>
                        </div>
                    ) : error ? (
                        <p className='centered-spinner'>Error: {error.message}</p>
                    ) : data.length === 0 ? (
                        <p>Пусто</p>
                    ) : (
                        data.map(item => (
                            <Card key={item.id} label={item.name} description={item.nutrients} />
                        ))
                    )}
                    {/* <AddItemButton onAdd={''} /> */}
                </div>

            </div>
        </div>
    );
}
