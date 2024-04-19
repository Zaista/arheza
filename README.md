<!-- This is the markdown template for the final project of the Building AI course, 
created by Reaktor Innovations and University of Helsinki, adjusted to fit the purpose here. -->

# Arheza

Created out of passion for programming, AI, and creativity.

Used as a final project for the Building AI course.

## Summary

Arheza is the user-tailored ever-growing role-playing epic-fantasy world for gamers who enjoy Choose-Your-Own-Advanture (CYOA) type of games.


## Background

Arheza is created for fun, to give users the opportunity to immerse themselves in the world of quests, advanture and magic, with a spin: users doing meaningful actions, such as quest completion, failures, eliminations, etc., would cause the baseline of the world to change. So if they, or any other players find themselves in the same situation, they will pick up where previous players left. As of the writing, we're not aware of any other plaform that supports this.

This leaves us with the following:
* Learn how to create a standard CYOA game using OpenAI
* Figure out a way how to update the world baseline based on player's progress


## How is it used?

It is used for fun, like any other game.

Enjoy this random image from the internet we found to kick off the project

<img src="https://github.com/Zaista/arheza/blob/master/static/background.jpg" width="300">

This is how you create code examples:
```python
 def generate_output():
  completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a ..."},
          {"role": "user", "content": "Describe a starting point for a hero going on his first quest."}
      ],
      stream=True
  )
  for chunk in completion:
      yield f"data: {chunk.choices[0].delta.content}\n\n".encode('utf-8')
```


## Data sources and AI methods

Baseline data for the world will be created by ourselves (with the help of the ChatGTP naturally).

## Challenges

* How to progresively update the world baseline, that it actually makes sense for the game and other players.
* How to limit the harming content that players might maliciously add to the game.

## What next?

Let's see...


## Acknowledgments

TBA

## Don't forget
```
python -m venv venv
venv\Scripts\activate
pip install --upgrade openai
```
