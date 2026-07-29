from datetime import datetime

from models.bdc_request import BDCRequest


def generate_ticket():
    """
    Generate a ticket number in the format:

    YYYYMMDD-000001

    Example:
    20260711-000001
    """

    today = datetime.now().strftime("%Y%m%d")

    latest = (
        BDCRequest.query
        .filter(BDCRequest.ticket_number.like(f"{today}-%"))
        .order_by(BDCRequest.ticket_number.desc())
        .first()
    )

    if latest:
        last_number = int(latest.ticket_number.split("-")[1])
        next_number = last_number + 1
    else:
        next_number = 1

    return f"{today}-{next_number:06d}"