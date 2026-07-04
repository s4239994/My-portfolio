from chatbot import SupportConversation
from persona import load_persona
from profiles import load_customers


def main() -> None:
    persona = load_persona()
    customers = load_customers()

    print(f"{persona['brand_name']} support (terminal channel). Type 'quit' to exit.\n")

    consent = input("Allow the assistant to look up your account? (y/n): ").strip().lower() == "y"
    customer = None
    if consent:
        print("Demo accounts:", ", ".join(customers.keys()))
        customer_id = input("Enter a customer ID: ").strip()
        customer = customers.get(customer_id)

    conversation = SupportConversation(persona, customer)
    print(f"\n{persona['brand_name']}: {persona['greeting']}\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue

        result = conversation.send(user_input)
        print(f"\n{persona['brand_name']}: {result['reply']}")
        print(f"   [sentiment: {result['sentiment']}]")
        if result["handoff_needed"]:
            print("   >> This conversation has been flagged for a human agent.")
        print()


if __name__ == "__main__":
    main()
