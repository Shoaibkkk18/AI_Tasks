from app.agents.user_chatbot_agent import (
    chatbot_response
)


def main():

    print("\n" + "="*60)

    print(
        " SMART PARKING AI ASSISTANT "
    )

    print("="*60)

    print(
        "\nType 'exit' to quit.\n"
    )

    while True:

        user_input = input(
            "You: "
        )

        if user_input.lower() == "exit":

            print("\nGoodbye!\n")

            break

        response = chatbot_response(
            user_input
        )

        print(f"\nBot: {response}\n")


if __name__ == "__main__":

    main()