from dataclasses import dataclass,field
@dataclass
class PathologyContext:
    specimens:list=field(default_factory=list)
    metadata:dict=field(default_factory=dict)
    case:dict=field(default_factory=dict)
