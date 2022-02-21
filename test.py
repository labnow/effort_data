t_json = {
    "revenue": {
        "filePath": "data4database/revenue.xlsx",
        "sheetName": "default",
        "dataStartFromRow": 3,
        "dataEndAtRow": 14,
        "dataStartFromColumn": 2,
        "dataEndAtColumn": 11,
        "tableHeaderRow": 2
    },
    "internal_cost": [
        "filePath": "data4database/internal_cost.xlsx",
        "sheetName": "default",
        "dataStartFromRow": 3,
        "dataEndAtRow": 14,
        "dataStartFromColumn": 2,
        "dataEndAtColumn": 11,
        "tableHeaderRow": 2
    ],
    "external_cost": {
        "filePath": "data4database/external_cost.xlsx",
        "sheetName": "default",
        "dataStartFromRow": 3,
        "dataEndAtRow": 14,
        "dataStartFromColumn": 2,
        "dataEndAtColumn": 11,
        "tableHeaderRow": 2
    }
}

def dosth():
    print(t_json["data"])

if __name__ == "__main__":
    dosth()