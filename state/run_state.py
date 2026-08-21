from dataclasses import dataclass,field
@dataclass
class RunState:
    phase:str="specimen"
    artifacts:dict=field(default_factory=dict)
