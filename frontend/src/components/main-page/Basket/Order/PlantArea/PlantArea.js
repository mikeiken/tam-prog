import React, { useEffect, useState } from 'react';
import Instance from '../../../../api/instance';
import './plant-area.css';

function Plant({ plant, onClick }) {
    return (
        <button className="plant-container" onClick={onClick}>
            <div className="plant-image-wrapper">
                <img
                    className="plant-image"
                    src="https://avatars.mds.yandex.net/i?id=2a34509a5eef3f1568fc5bcd184dfa1b_l-9290726-images-thumbs&n=13"
                    alt="Plant"
                />
            </div>
            <div>{plant.name}</div>
        </button>
    );
}

export default function PlantArea({ onPlantSelect }) {
    const [data, setData] = useState([]);
    const [filteredData, setFilteredData] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await Instance.get("/plant/?format=json");
                setData(response.data);
                setFilteredData(response.data); // Изначально показываем все данные
            } catch (err) {
                console.error(err);
            }
        };

        fetchData();
    }, []);

    const handleSearchChange = (e) => {
        const term = e.target.value.toLowerCase();
        setSearchTerm(term);

        const filtered = data.filter((plant) =>
            plant.name.toLowerCase().includes(term)
        );
        setFilteredData(filtered);
    };

    return (
        <div>
            <div className="plant-search-area">
                <input
                    placeholder="Введите название..."
                    value={searchTerm}
                    onChange={handleSearchChange}
                />
                <button>
                    <img alt="search" />
                </button>
            </div>
            <div className="plant-area">
                {filteredData.map((item) => (
                    <Plant
                        plant={item}
                        key={item.id}
                        onClick={() => onPlantSelect(item)} // Передаем выбранное растение
                    />
                ))}
            </div>
        </div>
    );
}