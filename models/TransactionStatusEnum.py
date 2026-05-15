from enum import Enum

class StatusEnum(str,Enum):
    PENDING='PENDING'
    APPROVED ='APPROVED'
    REJECT = 'REJECTED'
    CHARGEBACK ='CHARGEBACK'
    