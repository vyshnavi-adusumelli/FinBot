from openai import OpenAI


class ChatGPT:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.context = "I want you to act as a text-based csv file writer. I will send a message to you and you will extract dollar spent (just the number), category (mapped to one of these categories: Food, Groceries, Utilities, Transport, Shopping, Miscellaneous), and date in mm-dd-yyyy format and write in a row of csv in following order - category, date, dollars_spent. You will only reply with csv.  Do not write explanations."



    def send_message(self, message):
        completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": self.context},
          {"role": "user", "content": message}
          ]
        )


        csv_content = completion.choices[0].message.content.split("\n")
        
        if len(csv_content)<1:
            return "Miscellaneous", "01-01-1970", "0"
        
        category, date, amount = csv_content[0].split(",")


        return category, date, amount
    


if __name__ == "__main__":
    chat = ChatGPT()
    print(chat.send_message("I spent 5$ yesterday on Transport"))