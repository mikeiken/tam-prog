import React, { useState, useEffect } from "react";
import "../garden.css";
import SearchCard from "../SearchCard/SearchCard";
import Instance from "../../../api/instance";

export default function SearchBlock({ onSelectItem }) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        setLoading(true);
        Instance.get("/field/?format=json")
            .then((response) => {
                setData(response.data);
            })
            .finally(() => setLoading(false))
            .catch((err) => {
                setError(err);
            });
    }, []);

    const filteredData = data.filter((item) =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleCardClick = (item) => {
        onSelectItem(item);
    };

    const handleSearchChange = (e) => {
        setSearchTerm(e.target.value);
    };

    return (
        <div className="box1">
            <div className="search-block">
                <input
                    className="search-input"
                    placeholder="Название объекта"
                    value={searchTerm}
                    onChange={handleSearchChange}
                />
                <img
                    src={process.env.PUBLIC_URL + "/search.png"}
                    alt="Search Icon"
                    className="search-icon"
                />
            </div>
            {loading ? (
                <div className="loading-container">
                    <div className="spinner"></div>
                </div>
            ) : error ? (
                <div className="error-container">
                    <p className="text-color" style={{ "--font-size": "30px" }}>
                        Error: {error.message}
                    </p>
                </div>
            ) : filteredData.length === 0 ? (
                <div
                    className="empty-container text-color"
                    style={{ "--font-size": "30px" }}
                >
                    <p>Пусто</p>
                </div>
            ) : (
                <div className="scrolled-content">
                    {filteredData.map((item) => (
                        <SearchCard
                            key={item.id}
                            item={item}
                            onClick={() => handleCardClick(item)}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}
