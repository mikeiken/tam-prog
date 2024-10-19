import React, { useState, useEffect } from 'react'
import Instance from '../../../api/instance'
import Card from '../../../card/Card';

export default function PlotInfo() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await Instance.get('/plant/?format=json');
                setData(response.data);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);
    return (
        <div className='box2'>
            {loading ? (
                <div className='centered-spinner'>
                    <div className="spinner"></div>
                </div>
            ) : error ? (
                <p
                    className='centered-spinner text-color'
                    style={{ '--font-size': '5em' }}
                >
                    Error: {error.message}
                </p>

            ) : data.length === 0 ? (
                <p>Пусто</p>
            ) : (
                data.map(item => (
                    <Card key={item.id} label={item.name} description={item.nutrients} />
                ))
            )}
        </div>
    )
}
