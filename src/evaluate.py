"""The file is basically the "ground truth engine" for the step-level diagnostic tool!

It walks through a Problem's solution plan in order, resolving each Step's operands
(literal Fractions or references to earlier steps' results) and performing
the arithmetic, until every step has a computed result. The Problem's
final_step_id determines which of those results counts as the answer.
"""

from dataclasses import dataclass
from fractions import Fraction
from src.models import Op, Problem, Step, StepRef

@dataclass
class EvaluationResult:
    """ This holds the outcome of walking a Problem's plan to completion """

    final_answer: Fraction
    intermediates: dict[str, Function] # every step's result, keyed by step id

def _resolve_operand(operand, intermediates: dict[str, Fraction]) -> Fraction:
    """ Turn a single operand into an actual Fraction: pass through a literal,
    or look up a StepRef's referenced step in what's already been computed """

    if isinstance(operand, StepRef):
        if operand.step_id not in intermediates:
            raise ValueError(
                f"Step references '{operand.step_id}', which hasn't been "
                f"computed yet. Check that steps are ordered correctly."
            )
        return intermediates[operand.step_id]
    return operand

def _apply_op(op: Op, values: list[Fraction]) -> Fraction:
    """Perform a Step's operation on its fully-resolved operand values."""
    if op == Op.ADD:
        result = Fraction(0)
        for v in values:
            result += v
        return result
    elif op == Op.SUBTRACT:
        result = values[0]
        for v in values[1:]:
            result -= v
        return result
    elif op == Op.MULTIPLY:
        result = Fraction(1)
        for v in values:
            result *= v
        return result
    elif op == Op.DIVIDE:
        result = values[0]
        for v in values[1:]:
            result /= v
        return result
    else:
        raise ValueError(f"Unknown operation: {op}")
    
def evaluate(problem: Problem) -> EvaluationResult:
    """Walk a Problem's plan step by step and return the final answer
    along with every intermediate result, keyed by step id."""
    intermediates: dict[str, Fraction] = {}

    for step in problem.plan:
        resolved = [_resolve_operand(o, intermediates) for o in step.operands]
        intermediates[step.id] = _apply_op(step.op, resolved)

    if problem.final_step_id not in intermediates:
        raise ValueError(
            f"final_step_id '{problem.final_step_id}' does not match any "
            f"step id in the plan."
        )

    return EvaluationResult(
        final_answer=intermediates[problem.final_step_id],
        intermediates=intermediates,
    )
