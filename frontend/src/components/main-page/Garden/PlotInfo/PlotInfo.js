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
            
        </div>
    )
}
