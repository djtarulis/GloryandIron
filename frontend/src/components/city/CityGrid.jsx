import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

function CityGrid({ cityId, token }) {
  const [city, setCity] = useState(null);
  const [grid, setGrid] = useState([]);
  const [selectedCell, setSelectedCell] = useState(null);
  const [showBuildMenu, setShowBuildMenu] = useState(false);

  useEffect(() => {
    axios.get(`${API_BASE}/city/${cityId}/city_details`, {
      headers: { Authorization: `Bearer ${token}` },
    }).then(res => {
      setCity(res.data);
      setGrid(res.data.grid); // grid should be an array of arrays
    });
  }, [cityId, token]);

  const handleCellClick = (rowIdx, colIdx) => {
    setSelectedCell({ row: rowIdx, col: colIdx });
    setShowBuildMenu(true);
  };

  const handleBuild = (buildingType) => {
    axios.post(`${API_BASE}/city/${cityId}/build`, {
      building_type: buildingType,
      x: selectedCell.col,
      y: selectedCell.row,
    }, {
      headers: { Authorization: `Bearer ${token}` },
    }).then(() => {
      setShowBuildMenu(false);
      // Refetch city details to update grid
      axios.get(`${API_BASE}/city/${cityId}/city_details`, {
        headers: { Authorization: `Bearer ${token}` },
      }).then(res => {
        setCity(res.data);
        setGrid(res.data.grid);
      });
    });
  };

  if (!city) return <div>Loading city...</div>;

  return (
    <div>
      <h2>{city.name}</h2>
      <div style={{
        display: "grid",
        gridTemplateColumns: `repeat(${city.grid_size}, 50px)`,
        gap: "4px",
        margin: "20px 0"
      }}>
        {grid.map((row, rowIdx) =>
          row.map((cell, colIdx) => (
            <div
              key={`${rowIdx}-${colIdx}`}
              style={{
                width: "50px",
                height: "50px",
                border: "1px solid #888",
                background: cell.building ? "#bcd" : "#eee",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "0.8rem",
                cursor: !cell.building ? "pointer" : "default"
              }}
              onClick={() => !cell.building && handleCellClick(rowIdx, colIdx)}
            >
              {cell.building
                ? `${cell.building.name} (L${cell.building.level})`
                : "+"}
            </div>
          ))
        )}
      </div>
      {showBuildMenu && (
        <div style={{
          position: "absolute",
          background: "#fff",
          border: "1px solid #ccc",
          padding: "10px",
          zIndex: 10
        }}>
          <h3>Select Building</h3>
          <button onClick={() => handleBuild("Warehouse")}>Warehouse</button>
          <button onClick={() => handleBuild("Barracks")}>Barracks</button>
          <button onClick={() => setShowBuildMenu(false)}>Cancel</button>
        </div>
      )}
    </div>
  );
}

export default CityGrid;