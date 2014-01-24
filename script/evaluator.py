import re,os,glob

class Data:
    version = 0.1
    
class Task:
    def __init__(self, filename):
        mode = 0
        maxscore_re = re.compile("^maxscore\s*=\s*([\d]+)$",re.IGNORECASE)
        positives_re = re.compile("^#\s*positives:\s*$",re.IGNORECASE)
        negatives_re = re.compile("^#\s*negatives:\s*$",re.IGNORECASE)
        name_re = re.compile("^.*/(.*)\.txt$")
        m = name_re.match(filename)
        self.positive = []
        self.negative = []
        self.maxscore = 100
        self.name = m.group(1)
        f = open(filename,"r")
        for l in f:
            l = l.strip()
            if mode == 0:
                m = maxscore_re.match(l)
                if None != m:
                    mode = 1
                    self.maxscore = int(m.group(1))
            if mode == 1:
                m = positives_re.match(l)
                if None != m:
                    mode = 2
                continue

            if mode == 2:
                m = negatives_re.match(l)
                if None != m:
                    mode = 3
                else:
                    self.positive.append(l)
                continue

            if mode == 3:
                self.negative.append(l)
        f.close()
        self.dump()

    def dump(self):
        print("Maximum score: " + str(self.maxscore))
        print("Positives:")
        for p in self.positive:
            print(p)
        print("Negatives:")
        for p in self.negative:
            print(p)

def evaluate(task, solution):
    print("Not yet implemented")

def get_solutions(tasks):
    comment_re = re.compile("^#.*$")
    proposal_re = re.compile("^([^:]+):(.*)$")
    name_re = re.compile("^.*/(.*)\.txt$")
    ret={}
    solutions = glob.glob("solutions/*.txt")
    for fn in solutions:
        m = name_re.match(fn)
        name = m.group(1)
        ret[name]={}
        f = open(fn,"r")
        index = 0
        for l in f:
            index = index + 1
            l = l.strip()
            m = comment_re.match(l)
            if None!=m:
                continue
            m = proposal_re.match(l)
            if None!=m:
                if tasks[m.group(1)] == None:
                    print("Solution found, missing a problem in line " + str(index) + l)
                ret[name][m.group(1)] = m.group(2)
            else:
                print("In file " + fn + ": Undigestible line " + str(index) + l) 
        f.close()
    return ret

def get_tasks():
    ret={}
    tasks = glob.glob("tasks/*.txt")
    for task in tasks:
        t = Task(task)
        ret[t.name] = t
    return ret

def dump():
    for t in Data.tasks.keys():
        print("Task " + t)
    for p in Data.solutions.keys():
        print("Participant " + p)

def main():
    Data.tasks = get_tasks()
    Data.solutions = get_solutions(Data.tasks)    
    dump()
    

main()
