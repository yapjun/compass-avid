import openai


user_prompt = """\
You are a friendly AI acting as an education and career counselor. 
Include emojis in your reply if necessary. 
Assume that the user doesn't know what they want to pursue. 
Respond with detailed suggestions for possible career and education paths.
Arrange data in tables if possible.
Reply in markdown language and in the native language of the question. 
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
            "temperature": 0.95,
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

    def model_prediction(self, input, api_key):
        """
        wrapper for the API to save the prompt and the result
        """
        # Setting the OpenAI API key got from the OpenAI dashboard
        set_openai_key(api_key)
        output = self.query(user_prompt.format(input=input))
        return output

    # def append_inputlist(self, input):
    #     if self.inputList is None:
    #         inputlist = {input}
    #     return inputlist


