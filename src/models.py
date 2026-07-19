"""
This file holds the core data structures for my step-level diagnostic tool!

A problem is stored not as a text-answer pair, but as an explicit
solution plan: an ordered sequence of Steps, where each Step is an
operation on operands that may reference the result of an earlier Step.

This is what lets my tool compute "ground truth", and later, 
what a specific error would have produced instead.
"""

from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction 
from typing import Union

class ErrorCategory(str, Enum):
    """ The 4 stages of the Error Analysis, as adapted for this tool"""

    # make these uppercase, since they're constants: defined then don't change
    COMPREHENSION = "comprehension" # what's the question asking?
    TRANSFORMATION = "transformation" # translating words into math
    PROCESS = "process" # doing the math
    ENCODING = "encoding" # writing the answer correctly (like units)

class Op(str, Enum):
    """ Arithmetic operations a single Step can perform """

    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

    # an operand is either 1. a literal number pulled from problem text
    # OR 2. reference to an earlier step's result

Operand = Union[Fraction, "StepRef"]

@dataclass(frozen=True)
class StepRef:
    """ A reference to the result of a previous Step, used as an operand """
    step_id: str 

@dataclass
class Step:
    """
    A single operation within the solution plan. Here's an example:
    
    Example (widget problem, dad's rate): 
        Step(id="dad_rate", op=Op.DIVIDE,
             operands=[Fraction(30), Fraction(3)],
             description="dad's widgets per hour")

     Example referencing an earlier step (combined rate):
        Step(id="combined_rate", op=Op.ADD,
             operands=[StepRef("my_rate"), StepRef("dad_rate")],
             description="combined widgets per hour")
    """

    id:str
    op: Op
    operands: list[Operand]
    description: str = ""

@dataclass
class Problem:
    """
    A word problem stored as "ground truth": the text a student sees,
    and the ordered plan that produces the correct answer
    """

    id: str
    text: str
    plan: list[Step]
    final_step_id: str          # which Step's result is the final answer
    units: str = ""              # EX "widgets per hour"
    grade_level: int = 5
    tags: list[str] = field(default_factory=list)  # e.g. ["rates", "multi-step"]