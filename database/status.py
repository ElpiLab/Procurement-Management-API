class RequestStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_MANAGER = "pending_manager"
    PENDING_PROCUREMENT = "pending_procurement"
    ORDER_PLACED = "order_placed"