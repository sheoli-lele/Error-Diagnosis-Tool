# Step-Level Diagnostic Tool for Math

Students struggle with word problems that test their understanding of foundational math concepts. But what step -- out of the few it takes to get to the final answer -- is really at the core of each student's struggle? This tool is meant to tease out the failure point so teachers know how to help.

## Motivation 

I've worked as a tutor in many environments that range from helping friends with SAT math over FaceTime to working at a tutoring center. These environments all share a similarity: it is not sufficient for a student's improvement to simply be told that their answer is wrong, or how to get to the right one. Often, it's one specific step/skill within the longer process of obtaining a problem's correct answer that they struggle with. Identifying this step is the most difficult part of being a tutor. Why? Because a wrong answer to a problem is consistent with many different types of errors (it could be a careless mistake, difficulty understanding the problem itself, or anything else).

This tool was built to help with this difficulty. I've broken the process of solving a typical word problem into five steps based loosely on [Newman's Error Analysis Framework](https://compasstech.com.au/ARNOLD/PAGES/newman.htm):

1) Reading and comprehension (absorbing what the problem asks)
2) Transformation (converting the understoof problem into mathematical operations)
3) Process Skills (executing the calculations)
4) Encoding (expressing the final answer in acceptable form, right units and all)

For now, this tool is for diagnosing failure points for grades 4-6 math courses: multi-step operations and fractions/rates.

## How It Works

Let's say a student was given the following word problem, which they answered incorrectly:

" I build 15 widgets in 2 hours and my dad builds 30 in 3 -- how many can we build together in 1 hour?"

From start to finish, the tool goes through these stages: Input -> -? Solution Plan -> Error Signatures and Ground Truth -> Claude clasisifcatuon -> Diagnosis + Follow-ups

The input into the tool has three parts:

1) The text of the problem a student is struggling with 
2) The student's work as a sequenced of steps, typed
3) The student's final answer

My error taxonomy includes these four steps, explained using our earlier example:



The deterministic layer of the tool establishes the ground truth. The problem is stored not just as a text-answer pair, but as a solution plan: an ordered list of steps where each is an operation on operands that can reference earlier results. 

This layer generates what I'll call "error signatures". For each error category within my set of steps, the tool computes the wrong results the way a student who had made that error would. For example, if a student reports the final answer as "10 widgets" (which is the dad's hourly rate, an intermediate step that's not the final answer).

What happens when two errors (i.e. at two different stages) produce the SAME wrong answer? Built into it is a discriminating probe feature, which outputs a question that can be used to identify EXACTLY which step the error is located at.

The tool, after being given the question, the student's typed work, the correct plan, and the error siganture map, classified against the fixed taxnomoy then returns this structured output:

- Category of error
- Evidence step
- Plain-language explanation
- 1-2 follow-up problems that target the broken stage 

## Architecture/Design

## Worked example 

## Next Steps

This is a section where I keep a running list of shortcomings/inconsistencies/opportunities for growth, and translate them into concrete next tasks to add to the project. Here's the list:

- Technically, the Newman framework breaks the problem-solving process into FIVE steps (1 = reading; 2 = comprehension) but since the tool cannot diagnose problems with READING as it works now, I collapsted steps 1 and 2 into a single step. In the future, I could expand my tool to diagnose problems with reading (maybe) for younger students