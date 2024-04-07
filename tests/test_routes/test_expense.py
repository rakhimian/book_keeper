from app.schemas import expense as expense_schema


# json_data = {
#     "category": 0,
#     "amount": 0,
#     "comment": "string",
#     "expense_date": "2024-04-07T17:55:48.678743"
# }


# def test_create_expense(authorized_client):
#     res = authorized_client.post(
#         "/expenses/", json=json_data)
#     new_expense = expense_schema.ExpenseOut(**res.json())
#     assert res.status_code == 200

def test_get_all_expenses(authorized_client):
    res = authorized_client.get("/expenses/")
    assert res.status_code == 200
