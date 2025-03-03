
## **📌 1. `README.md` (Project Documentation)**
```md
# 🚀 FastAPI Event Management API

## 📌 Overview
This is a **FastAPI-based Event Management API** with the following features:
- **User Authentication** (Signup/Login) using JWT
- **Event Management** (Create, List, Update, Auto-Complete Past Events)
- **Attendee Management** (Register, Check-in)
- **Database:** SQLite (can be extended to PostgreSQL)
- **Containerized with Docker**
- **Tested with Pytest**

## 📌 Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/fastapi-event-management.git
cd fastapi-event-management
```

### **2️⃣ Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file:
```sh
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./sqlite3.db
```

### **5️⃣ Run the Application**
```sh
uvicorn main:app --reload
```
The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📌 Running with Docker
```sh
docker-compose up --build -d
docker-compose -f docker-compose.yml up -d 
```

## 📌 Running Tests
```sh
pytest tests/
```


## 📌 API Documentation 

The API Documentation will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## 📌 API Endpoints

### **User Authentication**
| Method | Endpoint            | Description             |
|--------|---------------------|-------------------------|
| `POST` | `/user/signup/`    | User Signup            |
| `POST` | `/user/login/`     | User Login             |

### **Event Management**
| Method | Endpoint              | Description             |
|--------|-----------------------|-------------------------|
| `POST` | `/event/create/`      | Create an Event        |
| `GET`  | `/event/{id}`         | Get an Event           |
| `PATCH`| `/event/{id}`         | Update Event Details   |
| `GET`  | `/event/`             | List Events            |

### **Attendee Management**
| Method | Endpoint                     | Description             |
|--------|------------------------------|-------------------------|
| `POST` | `/attendees/{event_id}/register/` | Register Attendee |
| `PUT`  | `/attendees/{attendee_id}/check-in/` | Check-in Attendee |


