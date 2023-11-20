from main_ingest import ingest
from main_chat import chat

try:
    choice = int(
        input("Do you want to Ingest or Chat:\n\n1. Ingest\n2. Chat\n\nYour Choice: ")
    )

    print()

    if choice == 1:
        ingest()
    elif choice == 2:
        result = chat()
        print(result)

except Exception as e:
    pass
