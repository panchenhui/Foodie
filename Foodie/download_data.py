from firebase import firebase

class download(object):
    def __init__(self):
        self.firebase1 = firebase.FirebaseApplication('https://inf552-69068.firebaseio.com', None)
        self.data = self.firebase1.get('/business', None)
