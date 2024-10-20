import React, { useState, useEffect } from 'react';
import '../garden.css';
import SearchCard from '../SearchCard/SearchCard';
import Instance from '../../../api/instance'

const testData = [
    { id: 1, name: "Объект 1", description: "Описание объекта 1" },
    { id: 2, name: "Объект 2", description: "Описание объекта 2" },
    { id: 3, name: "Объект 3", description: "Описание объекта 3" },
    { id: 4, name: "Объект 4", description: "Описание объекта 4" },
    // { id: 5, name: "Объект 5", description: "Описание объекта 5" },
    // { id: 6, name: "Объект 6", description: "Описание объекта 6" },
    // { id: 7, name: "Объект 7", description: "Описание объекта 7" },
];

export default function SearchBlock({ onSelectItem }) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await Instance.get('/garden/?format=json')
                setData(response.data);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleCardClick = (item) => {
        onSelectItem(item);
    };

    return (
        <div className='box1 '>
            <div className='search-block'>
                <input className='search-input' placeholder='Название объекта' />
                <img src={process.env.PUBLIC_URL + '/search.png'} alt='Search Icon' className='search-icon' />
            </div>
                {loading ? (
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
                    <div className='empty-container text-color' style={{ '--font-size': '30px' }}>
                        <p>Пусто</p>
                    </div>
                ) : (
                    <div className='scrolled-content'>
                        {data.map((item) => (
                            <SearchCard key={item.id} item={item} onClick={() => handleCardClick(item)} />
                        ))}
                    </div>
                )}
        </div>
    );
}