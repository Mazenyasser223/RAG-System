from graph import app

def run_rag_system():
    print("\n" + "="*50)
    print("Welcome to Tech Giants Strategic Assistant (RAG)")
    print("Type 'q' to exit the system.")
    print("="*50)

    while True:
    
        user_input = input("\nUser Question: ")
        
        if user_input.lower() == 'q':
            print("Exiting... Good luck with your project!")
            break

        print("Thinking...")
        inputs = {"question": user_input}

        result = app.invoke(inputs)

        print("\n" + "-"*30)
        print("ASSISTANT RESPONSE:")
        print(result["generation"])
        print("-"*30)

if __name__ == "__main__":
    run_rag_system()