# Reimbursement API (Mock)

This project provides a simple Flask API that simulates healthcare reimbursement logic for use with a Custom GPT agent. It uses CSV files for lookup and returns results via a POST API.

## How to Run

```bash
pip install -r requirements.txt
python mock_reimbursement_api.py
```

## Folder Structure

```
project-root/
├── data/                    # Upload reimbursement .csv files here
├── mock_reimbursement_api.py
├── requirements.txt
└── README.md
```

## Example Request

```json
POST /check_reimbursement
{
  "country": "australia",
  "service": "hearing aid"
}
```

## Deploy with Render or Fly.io
- Add a `render.yaml` or `fly.toml` to deploy with a single command.
