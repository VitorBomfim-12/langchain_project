from datetime import date

def isOver18(birth_date: date) -> bool:
    
    today = date.today()
    
    try:
        deadline_date = today.replace(year=today.year - 18)
    except ValueError:
       
        deadline_date = today.replace(year=today.year - 18, day=today.day - 1)
        
    
    return birth_date <= deadline_date

