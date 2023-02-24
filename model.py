import openai

edu_prompt = """\
You are a friendly AI acting as an education counselor. 
Include emojis in your reply if necessary. 
Assume that the user doesn't know what they want to pursue. 
According to the information that the user has provided, respond with
detailed suggestions for possible career paths and education paths 
such as possible degrees. Arrange the data in tables and in a way that is
readable.
Reply in the same language as the question. Format of the reply should be 
in markdown language, NO HTML TAGS.
If you are unable answer the question asked, say \"I don't know\"### 

I'm looking for advice.
---
{input}
---
 """

cv_prompt = """\
Your job is to rate the CV out of 10, provide
areas of improvement for the CV. The CV is below

---
{input}
---
"""

career_prompt = """\
You are a friendly AI acting as an career counselor. 
Include emojis in your reply if necessary. 
According to the information that the user has provided, respond with
detailed suggestions for possible career paths or options available.
Arrange the data in tables and in a way that is readable.
Reply in the same language as the question. Format of the reply should be 
in markdown language, NO HTML TAGS.
If you are unable answer the question asked, say \"I don't know\"### 

I'm looking for advice.
---
{input}
---
 """

pd_prompt = """\
You are a friendly AI acting as an behavioural and personal development counselor. 
Include emojis in your reply if necessary. 
According to the information that the user has provided, respond with
detailed/appropriate suggestions and courses of action.
If the user is sad, console them!!!!!
Reply in the same language as the question. Format of the reply should be 
in markdown language, NO HTML TAGS.
If you are unable answer the question asked, say \"I don't know\"### 

I'm looking for advice.
---
{input}
---
 """


def set_openai_key(key):
    """Sets OpenAI key."""
    openai.api_key = key


class GeneralModel:

    def __init__(self):
        print("Model Initialization--->")
        # set_openai_key(API_KEY)

    def query(self, prompt, myKwargs={}):
        """
        wrapper for the API to save the prompt and the result
        """

        # arguments to send the API
        kwargs = {
            "engine": "text-davinci-003",
            "temperature": 0.4,
            "max_tokens": 600,
            "best_of": 1,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": ["###"],
        }

        for kwarg in myKwargs:
            kwargs[kwarg] = myKwargs[kwarg]

        r = openai.Completion.create(prompt=prompt, **kwargs)["choices"][0][
            "text"
        ].strip()
        return r

    def model_prediction(self, input, api_key, cv=False, career=False,
                         edu=False, pd=False):
        """
        wrapper for the API to save the prompt and the result
        """
        # Setting the OpenAI API key got from the OpenAI dashboard
        set_openai_key(api_key)

        if cv:
            print("CV")
            output = self.query(cv_prompt.format(input=input))
        elif career:
            output = self.query(career_prompt.format(input=input))
        elif edu:
            output = self.query(edu_prompt.format(input=input))
        elif pd:
            output = self.query(pd_prompt.format(input=input))

        return output
