# Glory and Iron

Glory and Iron is an open-source browser-based MMO inspired by classic games like War2-Glory. The goal is to recreate and modernize the experience of building cities, managing resources, constructing buildings, training armies, and engaging in strategic warfare with other players.

---

## Project Overview

This project is a full-stack MMO game server and API, built with:

- **FastAPI (Python)** for the backend API
- **PostgreSQL** for persistent data storage
- **SQLAlchemy** for ORM/database models
- **Docker Compose** for easy development and deployment

The frontend (to be developed) will connect to this API to provide a rich, interactive game experience.

---

## Current Progress

- **User Authentication**
    - Registration and login with JWT-based authentication.
- **Player Model**
    - Securely stores player credentials.
- **City Model**
    - Cities are linked to players.
    - Each city tracks resources (steel, oil, rubber, food, gold) and their production rates.
    - Cities have coordinates on a world map.
    - Cities can have multiple buildings and units.
- **Resource System**
    - Cities generate resources over time.
    - Players can collect resources via an API endpoint.
    - Resource storage caps are determined by Warehouse buildings.
- **Buildings System**
    - Buildings are stored in a flexible table with a `type` and `level` (e.g., Warehouse, Barracks, etc.).
    - Warehouse increases max storage for each resource.
    - Barracks determines troop training capacity, speed, and unlocks new troop types.
- **Troops/Units System**
    - Units are not strictly bound to a city; they can move around the map.
    - Each unit tracks its type, quantity, current location, destination, and movement status.
    - Supports future features like marching, attacking, and returning.
- **API Endpoints**
    - Register, login, create city, list cities, collect resources, view city details, construct/upgrade buildings, train/manage units, and more.
- **Database Integration**
    - All data is stored in PostgreSQL and managed via SQLAlchemy models.
    - Alembic is used for database migrations.
- **Modular Codebase**
    - FastAPI routers are used to organize endpoints by domain (auth, city, etc.).
- **Dockerized Development**
    - Easy setup with Docker Compose for both backend and database.

---

## Roadmap

### Short-Term

- [ ] **Resource Spending:**  
  Allow players to spend resources on buildings, units, and upgrades.
- [ ] **Buildings System:**  
  Expand building types and effects (e.g., Research Center, Headquarters).
- [ ] **Troops System:**  
  Add endpoints for training, moving, and managing units.
- [ ] **Map/World View:**  
  Endpoints to view all cities and units on the world map.
- [ ] **Basic Frontend:**  
  Start a simple web frontend for player interaction.

### Medium-Term

- **Combat System:**  
  Implement attacking, defending, and battle resolution.
- **Alliance/Clan System:**  
  Allow players to form alliances and cooperate.
- **Resource Trading:**  
  Enable trading between players or cities.
- **Timed Events:**  
  Add background tasks for events, quests, and world updates.

### Long-Term

- **Advanced Frontend:**  
  Full-featured browser client with real-time updates.
- **Chat and Messaging:**  
  In-game communication between players.
- **Admin Tools:**  
  Tools for moderation and game balancing.
- **Performance and Scaling:**  
  Optimize for large numbers of concurrent players.

---

## Contributing

Please open issues or pull requests for features, bugfixes, or suggestions.

---

## License

This project is licensed under the MIT License.