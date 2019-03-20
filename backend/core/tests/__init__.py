from typing import List

import attr


@attr.s(slots=True, auto_attribs=True)
class FakeGraphqlResult:
    data: dict = None
    errors: List[Exception] = None

    def to_dict(self):
        if self.data:
            return {"data": self.data}
        return {"errors": [str(e) for e in self.errors]}
