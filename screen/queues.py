class Queue(object):
    def __init__(self):

        self.queue = []

    def append(self, elem):
        self.queue.append(elem)

    def getFirst(self):
        if len(self.queue) > 0:
            return self.queue[0]
        return None

    def getQueue(self):
        return self.queue

    def pop(self):
        return self.queue.pop(0)

    def remove(self, elem):
        if self.exists(elem):
            return self.queue.remove(elem)
            return True
        return False

    def clear(self):
        self.queue.clear()

    def exists(self, elem):
        for e in self.queue:
            if e == elem:
                return True
        return False

    def size(self):
        return len(self.queue)

    def getQueue(self):
        return self.queue

    def getIndex(self, name):
        i = 0
        for q in self.queue:
            if q == name:
                return i
            i = i+1
        return -1
