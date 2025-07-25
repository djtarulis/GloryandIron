import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = "http://localhost:5173"; // Update if using a different backend host

function App() {
  const [cities, setCities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

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
        console.log("Cities response:", res);
        setCities(res.data.cities || []);
      })
      .catch((err) => {
        console.error("Error fetching cities:", err.response?.data || err.message);
        setCities([]);
      })
      .finally(() => setLoading(false));
  }, [token]);

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">Glory and Iron</h1>
      {!loggedIn ? (
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
      ) : (
        <div>
          <h2 className="text-xl font-semibold mb-2">Your Cities</h2>
          {loading ? (
            <div>Loading cities...</div>
          ) : cities.length === 0 ? (
            <div>No cities found.</div>
          ) : (
            <ul className="space-y-2">
              {cities.map((city) => (
                <li key={city.id} className="border p-2 rounded">
                  <strong>{city.name}</strong> (x: {city.x}, y: {city.y})
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
