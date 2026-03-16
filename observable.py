class Observable:
    def __init__(self,subscribe_fn=None): self._fn=subscribe_fn
    def subscribe(self,on_next=None,on_error=None,on_complete=None):
        observer={'next':on_next or (lambda x:None),'error':on_error or (lambda e:None),'complete':on_complete or (lambda:None),'closed':False}
        def unsub(): observer['closed']=True
        if self._fn: self._fn(observer)
        return unsub
    def map(self,fn):
        src=self
        def sub(observer):
            src.subscribe(lambda x: observer['next'](fn(x)) if not observer['closed'] else None,observer['error'],observer['complete'])
        return Observable(sub)
    def filter(self,fn):
        src=self
        def sub(observer):
            src.subscribe(lambda x: observer['next'](x) if fn(x) and not observer['closed'] else None,observer['error'],observer['complete'])
        return Observable(sub)
    @staticmethod
    def of(*items):
        def sub(observer):
            for item in items:
                if observer['closed']: break
                observer['next'](item)
            observer['complete']()
        return Observable(sub)
if __name__=="__main__":
    results=[]
    Observable.of(1,2,3,4,5).filter(lambda x:x%2==0).map(lambda x:x*10).subscribe(lambda x:results.append(x))
    assert results==[20,40]
    print(f"Observable: {results}")
    print("All tests passed!")
