class ItsmConnector:
    def validate_ticket(self, provider, ticket_number, environment):
        return {"valid": bool(ticket_number and ticket_number.upper().startswith(("CHG","CHANGE"))), "provider": provider, "ticket_number": ticket_number}
