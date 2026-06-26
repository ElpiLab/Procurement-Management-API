from models.purchase_request import PurchaseRequest

class OrderService:

    @staticmethod
    def send_to_supplier(request: PurchaseRequest):
        """Handles the BPMN 'Service Task' - Generate PO & Send to Supplier."""
        print(f"[ORDER SERVICE] Sending order {request.id} to supplier {request.supplier_id}...")
        
        # In a real app, this would be an HTTP call:
        # response = requests.post(f"https://api.supplier.com/orders", json={...})
        # if response.status_code != 200:
        #     raise Exception("Failed to send order to supplier")
        
        # For now, just simulate success.
        return True