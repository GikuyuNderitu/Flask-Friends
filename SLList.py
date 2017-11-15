class UserNode(object):
    def __init__(self, user):
        self.user = user
        self.next = None


class SLList(object):
    def __init__(self):
        self.head = None
        self.tail = None
    
    def fastInsert(self, user):
        newNode = UserNode(user)
        if self.head == None:
            self.head = newNode
            return self
        
        if self.head.next == None:
            self.tail = newNode
            self.head.next = self.tail
            return self

        self.tail.next = newNode
        self.tail = newNode

    def extractById(self, id):
        runnerIsHead = True
        runner = self.head
        users = []

        while runnerIsHead and runner != None:
            if runner.user['user_id'] == id:
                users.append(runner.user)
                self.head = runner.next
                runner = self.head
            else:
                runner = runner.next
                runnerIsHead = False
        
        prev = self.head

        while runner != None:
            nextNode = runner.next

            if runner.user['user_id'] == id:
                users.append(runner.user)
                prev.next = nextNode
                runner = nextNode

            else:
                prev = runner
                runner = nextNode
        
        return users
    

        
