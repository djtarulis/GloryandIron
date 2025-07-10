# Glory and Iron

**Glory and Iron** is an open-source browser-based MMO inspired by classic games like War2-Glory. The goal is to recreate and modernize the experience of building cities, managing resources, and engaging in strategic warfare with other players.

---

## Project Overview

This project is a full-stack MMO game server and API, built with:

- **FastAPI** (Python) for the backend API
- **PostgreSQL** for persistent data storage
- **SQLAlchemy** for ORM/database models
- **Docker Compose** for easy development and deployment

The frontend (to be developed) will connect to this API to provide a rich, interactive game experience.

---

## Current Progress

- **User Authentication:**  
  - Registration and login with JWT-based authentication.
- **Player Model:**  
  - Securely stores player credentials.
- **City Model:**  
  - Cities are linked to players.
  - Each city tracks resources (steel, oil, rubber, food, gold) and their production rates.
  - Cities have coordinates on a world map.
- **Resource System:**  
  - Cities generate resources over time.
  - Players can collect resources via an API endpoint.
- **API Endpoints:**  
  - Register, login, create city, list cities, collect resources, and view city resources.
- **Database Integration:**  
  - All data is stored in PostgreSQL and managed via SQLAlchemy models.
- **Dockerized Development:**  
  - Easy setup with Docker Compose for both backend and database.

---

## Roadmap

### Short-Term

- [ ] **Resource Spending:**  
  Allow players to spend resources on buildings, units, and upgrades.
- [ ] **Buildings System:**  
  Add models and endpoints for city buildings and upgrades.
- [ ] **Troops System:**  
  Add models and endpoints for training and managing troops.
- [ ] **Map/World View:**  
  Endpoints to view all cities on the world map.
- [ ] **Basic Frontend:**  
  Start a simple web frontend for player interaction.

### Medium-Term

- [ ] **Combat System:**  
  Implement attacking, defending, and battle resolution.
- [ ] **Alliance/Clan System:**  
  Allow players to form alliances and cooperate.
- [ ] **Resource Trading:**  
  Enable trading between players or cities.
- [ ] **Timed Events:**  
  Add background tasks for events, quests, and world updates.

### Long-Term

- [ ] **Advanced Frontend:**  
  Full-featured browser client with real-time updates.
- [ ] **Chat and Messaging:**  
  In-game communication between players.
- [ ] **Admin Tools:**  
  Tools for moderation and game balancing.
- [ ] **Performance and Scaling:**  
  Optimize for large numbers of concurrent players.

---

## Contributing

Please open issues or pull requests for features, bugfixes, or suggestions.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

Inspired by War2-Glory and other classic browser
