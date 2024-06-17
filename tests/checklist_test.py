#region ------- IMPORTS -------------------------------------------------------------------------------------

import json
from typing import List
import pytest
from fastapi.testclient import TestClient
from app import main
from app.model import schemas, models
from app.db import database
from sqlalchemy.orm import Session
#endregion ---- IMPORTS -------------------------------------------------------------------------------------

#region ------- INIT ----------------------------------------------------------------------------------------

client = TestClient(main.app)

@pytest.fixture(scope="function")
def db():
    database.Base.metadata.create_all(bind=database.engine)  # Creiamo il database e le tabelle
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
#endregion ---- INIT ----------------------------------------------------------------------------------------

#region ------- CONSTANTS -----------------------------------------------------------------------------------

CHECKLIST_JSON = '''
{
  "title": "My Special Test Checklist",
  "sections": [
    {
      "title": "Section 1",
      "checks": [
        {
          "text": "Check 1",
          "parent_id": null
        },
        {
          "text": "Check 1.1",
          "parent_id": 0
        }
      ]
    },
    {
      "title": "Section 2",
      "checks": [
        {
          "text": "Check 2",
          "parent_id": null
        },
        {
          "text": "Check 2.1",
          "parent_id": 0
        },
        {
          "text": "Check 2.1.1",
          "parent_id": 0
        }
      ]
    }
  ]
}
'''

CHECKLIST_JSON_NO_SECTION_TITLE = '''
{
  "title": "My Special Test Checklist",
  "sections": [
    {
      "checks": [
        {
          "text": "Check 1",
          "parent_id": null
        },
        {
          "text": "Check 1.1",
          "parent_id": 0
        }
      ]
    },
    {
      "title": "Section 2",
      "checks": [
        {
          "text": "Check 2",
          "parent_id": null
        },
        {
          "text": "Check 2.1",
          "parent_id": 0
        },
        {
          "text": "Check 2.1.1",
          "parent_id": 0
        }
      ]
    }
  ]
}
'''

CHECKLIST_JSON_NO_PARENT_ID = '''
{
  "title": "My Special Test Checklist",
  "sections": [
    {
      "title": "Section 1",
      "checks": [
        {
          "text": "Check 1",
          "parent_id": null
        },
        {
          "text": "Check 1.1",
          "parent_id": 0
        }
      ]
    },
    {
      "title": "Section 2",
      "checks": [
        {
          "text": "Check 2",
          "parent_id": null
        },
        {
          "text": "Check 2.1",
          "parent_id": 0
        },
        {
          "text": "Check 2.1.1",
          "parent_id": 0
        }
      ]
    }
  ]
}
'''

#endregion ---- CONSTANTS -----------------------------------------------------------------------------------

#region ------- TESTS ---------------------------------------------------------------------------------------

# Test POST /checklists endpoint to add a new complete checklist
def test_add_checklist(db: Session):
    data = json.loads(CHECKLIST_JSON)
    checklist = schemas.Checklist(**data)

    response = client.post("/checklists/", json=data)

    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"

    response_data = response.json()

    try:
        checklist_response = schemas.Checklist(**response_data)
    except Exception as e:
        print("Error creating Checklist schema:", str(e))
        assert False, "Failed to create Checklist schema"

    assert checklist_response.title == checklist.title, f"Error in data correctness - Expected checklist title {checklist.title}, got {checklist_response.title}"
    assert len(checklist_response.sections) == len(checklist.sections), f"Error in data correctness - Expected {len(checklist.sections)} sections, got {len(checklist_response.sections)}"

    assert checklist_response.sections[0].title == checklist.sections[0].title
    assert len(checklist_response.sections[0].checks) == len(checklist.sections[0].checks)
    assert checklist_response.sections[0].checks[0].text == checklist.sections[0].checks[0].text
    assert checklist_response.sections[0].checks[0].parent_id == checklist.sections[0].checks[0].parent_id

    assert checklist_response.sections[1].title == checklist.sections[1].title
    assert len(checklist_response.sections[1].checks) == len(checklist.sections[1].checks)
    assert checklist_response.sections[1].checks[0].text == checklist.sections[1].checks[0].text
    assert checklist_response.sections[1].checks[1].text == checklist.sections[1].checks[1].text
    assert checklist_response.sections[1].checks[2].text == checklist.sections[1].checks[2].text

    db_checklist = db.query(models.Checklist).filter(models.Checklist.id == checklist_response.id).first()
    assert db_checklist is not None, "Checklist not found in the database"
    assert db_checklist.title == checklist.title

    db_sections = db.query(models.Section).filter(models.Section.checklist_id == db_checklist.id).all()
    assert len(db_sections) == len(checklist.sections), f"Expected {len(checklist.sections)} sections, found {len(db_sections)} in the database"

    db_checks = db.query(models.Check).filter(models.Check.section_id.in_([section.id for section in db_sections])).all()
    expected_checks_count = sum(len(section.checks) for section in checklist.sections)
    assert len(db_checks) == expected_checks_count, f"Expected {expected_checks_count} checks, found {len(db_checks)} in the database"

# Test POST /checklists endpoint to add a checklist with missing values
def test_add_checklist_missingFields():
    data = json.loads(CHECKLIST_JSON_NO_SECTION_TITLE)

    response = client.post("/checklists/", json=data)

    assert response.status_code == 422, f"Error in fetching data - Expected 422, got {response.status_code}"

# Test GET /checklists/{id} endpoint to get a specific checklist given its id
def test_get_single_checklists():
    data = json.loads(CHECKLIST_JSON)
    checklist = schemas.Checklist(**data)

    response = client.post("/checklists/", json=data)
    
    response_data = response.json()

    try:
        checklist_response = schemas.Checklist(**response_data)
    except Exception as e:
        print("Error creating Checklist schema:", str(e))
        assert False, "Failed to create Checklist schema"

    response = client.get(f"/checklists/{checklist_response.id}")

    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"

    assert checklist_response.title == checklist.title, f"Error in data correctness - Expected checklist title {checklist.title}, got {checklist_response.title}"
    assert len(checklist_response.sections) == len(checklist.sections), f"Error in data correctness - Expected {len(checklist.sections)} sections, got {len(checklist_response.sections)}"

    assert checklist_response.sections[0].title == checklist.sections[0].title
    assert len(checklist_response.sections[0].checks) == len(checklist.sections[0].checks)
    assert checklist_response.sections[0].checks[0].text == checklist.sections[0].checks[0].text
    assert checklist_response.sections[0].checks[0].parent_id == checklist.sections[0].checks[0].parent_id

    assert checklist_response.sections[1].title == checklist.sections[1].title
    assert len(checklist_response.sections[1].checks) == len(checklist.sections[1].checks)
    assert checklist_response.sections[1].checks[0].text == checklist.sections[1].checks[0].text
    assert checklist_response.sections[1].checks[1].text == checklist.sections[1].checks[1].text
    assert checklist_response.sections[1].checks[2].text == checklist.sections[1].checks[2].text

# Test GET /checklists endpoint to get various checklists with pagination
def test_get_multiple_checklists(db: Session):
    response = client.get("/checklists/?skip=0&limit=2")

    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"

    response_data = response.json()

    values = db.query(models.Checklist).order_by(models.Checklist.id).limit(2).all()
    assert len(response_data) == len(values), f"Expected max 2 checklists, but got {len(values)}"

    assert response_data[0]['id'] == values[0].id
    assert response_data[1]['id']== values[1].id

    response = client.get("/checklists/?skip=10&limit=5")
    response_data = response.json()

    values = db.query(models.Checklist).order_by(models.Checklist.id).offset(10).limit(5).all()

    assert response.status_code == 200, f"Error in fetching data - Expected 200, got {response.status_code}"
    assert len(response_data) == len(values), f"Expected max 5 checklists, but got {len(response_data)}"

    for i in range(0,len(response_data)):
        assert response_data[i]['id']== values[i].id


#endregion ---- TESTS ---------------------------------------------------------------------------------------