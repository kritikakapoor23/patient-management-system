# 🏥 Patient Management System
A FastAPI-based healthcare management system for storing and managing patient records digitally.

## 🚀 Features
- View all patient records
- Create new patient records with BMI auto-calculation
- Update existing patient information
- Delete patient records
- Input validation with Pydantic
- Sortable patient data by height, weight, or BMI
- Interactive API documentation with Swagger UI

## 🛠 Tech Stack
- FastAPI
- Python
- Pydantic
- JSON
- Git & GitHub

## 📌 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/about` | About the API |
| GET | `/view` | View all patients |
| GET | `/patient/{patient_id}` | Get a specific patient |
| GET | `/sort` | Sort patients by field |
| POST | `/post` | Create a new patient |
| PUT | `/edit/{patient_id}` | Update patient info |
| DELETE | `/delete/{patient_id}` | Delete a patient |

## ⚙️ Run Locally
```bash
git clone https://github.com/kritikakapoor23/patient-management-system.git
cd patient-management-system
python -m venv myenv
myenv\Scripts\activate
pip install fastapi uvicorn
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## 🔮 Upcoming Features
- ReactJS frontend
- Authentication & authorization
