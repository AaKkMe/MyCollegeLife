1. # MyCollegeLife Dashboard

This project is a backend server for the MyCollegeLife application, designed to manage classes, assignments, and study logs.

---

## How to Run This Project (Setup Instructions)

Follow these steps to get the backend server running on your local machine.

### 1. Clone the Repository
First, download the project from GitHub.
```bash
git clone https://github.com/AaKkMe/MyCollegeLife.git
cd MyCollegeLife

2.
# For Windows
python -m venv .venv
.venv\Scripts\activate

# For Mac/Linux
python3 -m venv .venv
source .venv/bin/activate

3. pip install -r requirements.txt

4. flask shell
from app import db
db.create_all()
exit()

5. flask run