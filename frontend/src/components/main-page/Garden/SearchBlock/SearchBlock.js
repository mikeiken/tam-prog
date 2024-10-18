import React, { useState, useEffect } from 'react';
import '../garden.css';
import Instance from '../../../api/instance';
import SearchCard from '../SearchCard/SearchCard';

export default function SearchBlock() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await Instance.get('/garden/?format=json');
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
        <div className='box1'>
            <div className='search-block'>
                <input className='search-input' placeholder='Название объекта' />
                <img src={process.env.PUBLIC_URL + '/search.png'} alt='Search Icon' className='search-icon' />
            </div>
            <div>
                {/* {loading ? (
                    <div className='loading-container'>
                        <div className="spinner"></div>
                    </div>
                ) : error ? (
                    <div className='error-container'>
                        <p className='text-color' style={{ '--font-size': '30px' }}>
                            Error: {error.message}
                        </p>
                    </div>
                ) : data.length === 0 ? (
                    <div className='empty-container'>
                        <p>Пусто</p>
                    </div>
                ) : (
                    data.map(item => (
                        <SearchCard key={item.id}/>
                    ))
                )} */}
            </div>
        </div>
    );
}


