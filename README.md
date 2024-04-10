# dataset-fr-keystrokes
Keystroke logging dataset from "Investigating how changes in students’ revising behavior relate to the evolution of essay content quality"

We collected writings and keystroke loggings from students of 10th grade in France from four different classes in different schools.
Each student participated between 1 and 3 times. 
Each file available corresponds to a session.
The exercise proposed to the student was to complete an argumentative text for which the introduction and the conclusion are given.

In the data, you will be able to find these different fields : 
  - timestamp (of submission)
  - all_texts (list of strings, composed of : the introduction, the student's answer, the conclusion)
  - text_type (string, defining the type of text : always argumentative here)
  - student_id (uuid, allow you to identify the student through the sessions)
  - exercise_id (uuid, allow you to identify the exercise answered)
  - keystrokes (string, encoded keystrokes)

A decoding script is available. However, here is the encoding strategy chosen for the keystrokes:
  - \u001f : separator within a stroke
  - \u001d : separator between strokes

  For each stroke, we are encoding if it was a deletion (\u0000), an insertion (\u0002) or simply a character at the end (no marker).
  Then we add in case of addition or insertion, the character added. When it is a deletion or insertion we also add the position of the cursor for the action that was made.
  We also keep the difference of time between that stroke and the previous one (in milliseconds).

  
