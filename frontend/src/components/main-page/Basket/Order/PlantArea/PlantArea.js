import React, { useEffect, useState } from "react";
import Instance from "../../../../api/instance";
import "./plant-area.css";

function Plant({ plant, onClick }) {
  return (
    <button className="plant-container" onClick={onClick}>
      <div className="plant-image-wrapper">
        <img className="plant-image" src={plant.url} alt="Plant" />
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
        <div className={"plant-search-input-wrapper"}>
          <input
            placeholder="Введите название..."
            value={searchTerm}
            onChange={handleSearchChange}
            className={"plant-area-input"}
          />
          <button className={"plant-search-button"}>
            <img src={process.env.PUBLIC_URL + "/search.svg"} alt="search" />
          </button>
        </div>
      </div>
      <div className="plant-area">
        {filteredData.map((item) => (
          <Plant
            plant={item}
            key={item.id}
            onClick={() => onPlantSelect(item)} // Передаем объект растения
          />
        ))}
      </div>
    </div>
  );
}
