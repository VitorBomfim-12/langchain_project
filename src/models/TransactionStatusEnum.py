from enum import Enum

class StatusEnum(str,Enum):
    PENDING='PENDING'
    APPROVED ='APPROVED'
    REJECTED = 'REJECTED'
    CHARGEBACK ='CHARGEBACK'
    