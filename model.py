import openai

cv_prompt = """\
Your job is to rate the CV out of 10, provide
areas of improvement for the CV. The CV is below

---
{input}
---
"""

career_prompt = """\
You are a friendly career counselor AI, the user will ask you questions in areas relating
to their career, education or personal improvement. 
Include emoticons when appropriate.
According to the information that the user has provided, respond with
detailed suggestions for possible career paths or options available.
Arrange your data in lists and structure your replies into paragraphs.
Reply in the same language as the question. Format of the reply should be 
in markdown language, NO HTML TAGS.
You can ask questions to further clarify the prompt.
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

    def model_prediction(self, input, api_key, cv=False):
        """
        wrapper for the API to save the prompt and the result
        """
        # Setting the OpenAI API key got from the OpenAI dashboard
        set_openai_key(api_key)

        if cv:
            output = self.query(cv_prompt.format(input=input))
        else:
            output = self.query(career_prompt.format(input=input))

        return output
