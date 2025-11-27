from app.tools.dataset_inspector import DatasetInspector

inspector = DatasetInspector()
result = inspector.inspect("examples/sample_dataset")

print(result)
