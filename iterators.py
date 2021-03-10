class PopIterator:
    def __init__(self, popable, index=0):
        self.popable = popable
        self.index = index  # index to pop
        self.rest = self.total = len(popable)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.popable) > 0:
            ret = self.popable.pop(self.index)
            self.rest -= 1
            return ret
        else:
            raise StopIteration


class PandasIterator:
    def __init__(self, pandas_obj, batch_size, start_index=0):
        self.pandas_obj = pandas_obj
        self.batch_size = batch_size
        self.start_index = start_index
        self.current_position = self.start_index
        assert start_index < len(self), f"start_index should be less than {len(self)}"

    def __len__(self):
        return ceil(len(self.pandas_obj) / self.batch_size)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self) > self.current_position:
            start = self.current_position * self.batch_size
            end = (self.current_position + 1) * self.batch_size
            ret = self.pandas_obj.iloc[start:end]
            self.current_position += 1
            return ret
        
        else:
            self.current_position = self.start_index
            raise StopIteration
