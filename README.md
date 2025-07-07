# 🌐 Web-Based IP Address Management System

## 📌 Objective

This project aims to design and implement a secure, scalable, and user-friendly **Web-Based IP Address Management System (IPAM)**. It enables authenticated users to manage IP addresses with role-based access and tamper-proof auditing. The system is ideal for infrastructure teams needing centralized control over IP resource tracking.

---

## 🧩 Key Features

- 🔐 **Authentication & Authorization** with JWT tokens and role-based access control.
- 📝 **IP Address Management** for both IPv4 and IPv6, with labels and optional comments.
- 🧑‍💼 **Role-Based CRUD**: Regular users can manage only their records; Super Admins have full control.
- 📊 **Audit Logging**: Immutable and secure logs of all user actions.
- 📈 **Super Admin Dashboard** for auditing user and IP activity.

---

## 🏗️ System Architecture

The system follows a **Microservices Architecture** consisting of three key services:

1. **Gateway Service** - Single entry point for frontend and client interactions.
2. **Auth Service** - Manages user login, JWT generation, and token renewal.
3. **IP Management Service** - Handles all IP-related data operations and business logic.

> 💡 Each service has its own database for complete decoupling.

---

## 🔐 Authentication & Authorization

- Users authenticate via the **Auth Service**, receiving a **JWT token**.
- Tokens support **automatic renewal** to avoid session interruptions.
- Users are assigned roles (`User`, `Super Admin`) to control their access rights.

---

## 💾 IP Address Management

- Add both **IPv4** and **IPv6** addresses.
- Attach a **label** and optional **comment** to each IP.
- Modify labels (based on user roles):
  - Regular users: Edit only their own IP entries.
  - Super Admins: Edit or delete any IP entry.
- View all IP records across the system (read-only access).

---

## 🧾 Audit Logging

A robust, secure, and **tamper-proof audit system** includes:
- Logs all changes, login/logout events, and actions on IP records.
- Tracks:
  - Per-session activity.
  - Lifetime activity for both users and IP records.
- Audit logs are **immutable**—no user can delete them, not even Super Admins.
- 📊 **Audit Log Dashboard** available only to Super Admins for insights and oversight.
- Audit Service is being called directly per service using "x-internal-key"
  - Adds Unnecessary Latency
  - Security Risk
  - Failure Propagation
  - Avoids Unnecessary JWT Validation Overhead
  - Simpler and More Secure for Internal Traffic

---

## 🛠️ Recommended Tech Stack

| Layer        | Technology       |
|--------------|------------------|
| Backend      | Python 🐍 (FastAPI) |
| Frontend     | React ⚛️           |
| Database     | PostgrelSQL (per service) |
| Auth         | JWT (JSON Web Tokens) |
| Communication | Internal API Calls via Gateway |
| Testing      | SQLite

> 📡 All frontend requests go **only** through the Gateway Service.  
> 💬 Microservices communicate via internal HTTP API calls.

---

## ⚙️ Architecture Guidelines

- Each microservice should be **independently deployable**.
- Use **design patterns** as preferred (e.g., Repository, CQRS, etc.).
- **Frontend** must follow industry-standard best practices (componentization, state management, routing, etc.).
- Ensure **data integrity** across microservices while maintaining loose coupling.
- **Service databases must not be shared** between services.

---

## 📂 Project Structure (Suggested)

```bash
ip-address-management/
├── gateway-service-fastapi/
├── auth-service-fastapi/
├── ip-management-service-fastapi/
├── frontend/
└── README.md
```

📌 Use Case: Sr Back-End Developer Practical Test
This project is designed to test and demonstrate real-world backend development skills with an emphasis on:

Microservices architecture
Security best practices
Audit and compliance logging
API design and role-based access control
🚀 Getting Started (Instructions Placeholder)
🛠️ Installation and running instructions should be added here based on your environment setup.

📣 Contributions
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

🛡️ License
Distributed under the MIT License. See LICENSE for more information.

👦 Author
Nathanielle M. Romero - [Linkedin 🔗](https://www.linkedin.com/in/nathanielle-romero-a2580020a/)
