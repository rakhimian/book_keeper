from app.schemas import budget as budget_schema

# json_data = {
#   "term": "2024-04-07T17:14:48.130Z",
#   "category": 1,
#   "amount": 178
# }


def test_get_all_budgets(authorized_client):
    res = authorized_client.get("/budgets/")
    assert res.status_code == 200

#
# def test_create_budget(authorized_client):
#     res = authorized_client.post(
#         "/budgets/", json=json_data)
#     print(res.json())
#     # new_budget = budget_schema.BudgetOut(**res.json())
#     assert res.status_code == 201
