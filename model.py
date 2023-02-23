import openai

#prompt = f"Answer the question based on the context below, and if the
# question can't be answered based on the context, say \"I don't know\"\n\n
# Context: {context}\n\n---\n\nQuestion: {question}\nAnswer:",

user_prompt = """You are a friendly AI acting as an education and career counselor. 
Include emojis in your reply but don't force it. Assuming the user doesn't know what they 
want to pursue. Try to provide detailed responses and advice in a table.
If you are unable answer the question asked, say \"I don't know\"### 
I have the following background: 

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


