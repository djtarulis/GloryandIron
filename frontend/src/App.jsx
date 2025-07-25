import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import CityGrid from "./components/city/CityGrid";

const API_BASE = "http://localhost:8000";

function App() {
  const [cities, setCities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [selectedCityId, setSelectedCityId] = useState(null);

  // Handle login
  const handleLogin = async (e) => {
    e.preventDefault();
    setAuthError("");
    try {
      const form = new FormData();
      form.append("username", username);
      form.append("password", password);
      const res = await axios.post(`${API_BASE}/auth/token`, form);
      setToken(res.data.access_token);
      setLoggedIn(true);
    } catch (err) {
      setAuthError("Login failed");
      setLoggedIn(false);
    }
  };

  // Fetch cities after login
  useEffect(() => {
    if (!token) return;
    setLoading(true);
    axios
      .get(`${API_BASE}/city/list`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setCities(res.data.cities || []);
      })
      .catch(() => setCities([]))
      .finally(() => setLoading(false));
  }, [token]);

  // Render login form if not logged in
  if (!loggedIn) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-4">Glory and Iron</h1>
        <form onSubmit={handleLogin} className="mb-6 flex flex-col gap-2">
          <input
            type="text"
            placeholder="Username"
            className="border p-2"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            className="border p-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="bg-blue-600 text-white p-2 rounded">
            Login
          </button>
          {authError && <div className="text-red-500">{authError}</div>}
        </form>
      </div>
    );
  }

  // If a city is selected, show the city grid
  if (selectedCityId) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <button
          className="mb-4 px-3 py-1 bg-gray-300 rounded"
          onClick={() => setSelectedCityId(null)}
        >
          &larr; Back to City List
        </button>
        <CityGrid cityId={selectedCityId} token={token} />
      </div>
    );
  }

  // Otherwise, show the city list
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">Glory and Iron</h1>
      {loading ? (
        <div>Loading cities...</div>
      ) : cities.length === 0 ? (
        <div>No cities found.</div>
      ) : (
        <div>
          <h2 className="text-xl font-semibold mb-2">Your Cities</h2>
          <ul className="space-y-2">
            {cities.map((city) => (
              <li
                key={city.id}
                className="border p-2 rounded cursor-pointer hover:bg-blue-100"
                onClick={() => setSelectedCityId(city.id)}
              >
                <strong>{city.name}</strong> (x: {city.x}, y: {city.y})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
