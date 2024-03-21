import pytest
class NotInRange(Exception):
    def __init__(self,message="value not in range"):
        #self.input_=input_
        self.message=message
        super().__init__(self.message)

## always test case  name needs to start with test_ and for running use pytest -v 
        ##pep 8 style guide for python

def test_generic():

    a=2
    with pytest.raises(NotInRange):
     if a  not in range(10,20):
        raise NotInRange
    
