from datetime import datetime, timedelta

def get_last_month_date_range():
    today = datetime.today()
    first_day_of_current_month = datetime(2024, 10, 1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_last_month = datetime(last_day_of_last_month.year, last_day_of_last_month.month, 1)
    return first_day_of_last_month.strftime('%d-%b-%Y'), last_day_of_last_month.strftime('%d-%b-%Y')

def get_transaction_type(entity: str):
    if not entity:
        raise ValueError("Entity is empty")
    trans_name = entity.lower()
    if "pending" in trans_name:
        return "Descartada"
    if "pendiente" in trans_name:
        return "Descartada"
    if "didi" in trans_name:
        if "food" in trans_name:
            return "Comida"
        else:
            return "Transporte"
    if "bbva" in trans_name:
        return "Credito BBVA"
    if "notariado" in trans_name:
        return "Arriendo"
    if "boacompra" in trans_name:
        return "Juegos"
    if "uber" in trans_name:
        return "Transporte"
    if "google" in trans_name:
        return "Subscripcion"
    if "nu colombia" in trans_name:
        return "Credito Nu"
    if "icetex" in trans_name:
        return "Deuda ICETEX"
    if "tiendas ara" in trans_name:
        return "Comida o trago"
    if "rappi" in trans_name:
        return "Comida"
    if "tembici" in trans_name:
        return "Subscripcion"
    if "oxxo" in trans_name:
        return "Comida o trago"
    if "pizza" in trans_name:
        return "Comida"
    if "olimpica" in trans_name:
        return "Comida"
    return ""
    
